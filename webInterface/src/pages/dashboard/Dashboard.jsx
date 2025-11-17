import { useState, useEffect } from 'react';
import axios from 'axios';
import ScoreGaugeCard from '../../components/ScoreGaugeCard';
import ScoreHistoryChart from '../../components/ScoreHistoryChart';
import ListDangerous from '../../components/ListDangerous';
import { Box, Skeleton } from "@mui/material";

const Dashboard = () => {
    // Get Bootstrap primary color from CSS variable
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--bs-secondary').trim();

    const [scores, setScores] = useState([
        { id: 0, title: "Base Score", subtitle: "(Simple Average)", value: 0, max: 10, color:'#0d6efd'},
        { id: 1, title: "Impact Score", subtitle: "(Weighted by Impact)", value: 0, max: 10, color:'#d32f2f' },
        { id: 2, title: "Exploitability", subtitle: "(Weighted by Exploitability)", value: 0, max: 10, color:'#f57c00' },
        { id: 3, title: "Severity", subtitle: "(Weighted by Severity)", value: 0, max: 10, color:'#fbc02d' },
        { id: 4, title: "CWE Count", subtitle: "(Weighted by Weaknesses)", value: 0, max: 10, color:'#388e3c' },
        { id: 5, title: "Asset Weight", subtitle: "(Weighted by Assets)", value: 0, max: 10, color:'#7b1fa2' },
    ]);

    const [scoreHistory, setScoreHistory] = useState([
        { timestamp: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), scores: [0, 0, 0, 0, 0, 0] },
        { timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), scores: [0, 0, 0, 0, 0, 0] },
        { timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), scores: [0, 0, 0, 0, 0, 0] },
        { timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), scores: [0, 0, 0, 0, 0, 0] },
        { timestamp: new Date(), scores: [0, 0, 0, 0, 0, 0] },
    ]);

    const [cveList, setCveList] = useState([]);
    const [loading, setLoading] = useState(true);

    const scoreLabels = ['Base Score', 'Impact', 'Exploitability', 'Severity', 'CWE Count', 'Asset Weight'];
    const scoreColors = ['#1976d2', '#d32f2f', '#f57c00', '#fbc02d', '#388e3c', '#7b1fa2'];

    const getTextColor = (value, max) => {
        if (value > max * 0.7) return '#d32f2f';
        if (value > max * 0.4) return '#f57c00';
        return '#388e3c';
    };

    const formatDateTimeLabel = (date) => {
        const options = { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit', 
            hour: '2-digit', 
            minute: '2-digit'
        };
        return new Intl.DateTimeFormat('it-IT', options).format(date);
    };

    const fetchScoreHistory = async () => {
        try {
            const response = await axios.get('/api/vuln_score_lite/score-history');
            if (response.data.success && response.data.history) {
                // Convert ISO timestamps to Date objects and map scores to array format
                const formattedHistory = response.data.history.map(entry => ({
                    timestamp: new Date(entry.timestamp),
                    scores: [
                        entry.scores[0] || 0,
                        entry.scores[1] || 0,
                        entry.scores[2] || 0,
                        entry.scores[3] || 0,
                        entry.scores[4] || 0,
                        entry.scores[5] || 0
                    ]
                }));
                return formattedHistory;
            }
            return null;
        } catch (error) {
            console.error('Error fetching score history:', error);
            return null;
        }
    };

    const addNewCVEInList = async() => {
        //TODO
    }

    const deleteCVEFromList = async(cveId) => {
        //TODO: Implement API call to remove CVE
        console.log('Deleting CVE:', cveId);
        // Remove from local state for now
        setCveList(prevList => prevList.filter(cve => cve.id !== cveId));
    }

    useEffect(() => {
        const loadDashboard = async () => {
            setLoading(true);
            try {
                // First, try to load the latest scores (without recalculating)
                const latestResponse = await axios.get('/api/vuln_score_lite/latest-scores');
                
                if (latestResponse.data.success) {
                    // Use existing scores
                    const existingScores = latestResponse.data.scores;
                    console.log('Loading existing scores:', existingScores);
                    
                    setScores(prevScores =>
                        prevScores.map((score, index) => ({
                            ...score,
                            value: existingScores[index] || 0
                        }))
                    );
                } else {
                    // No scores available, need to calculate for the first time
                    console.log('No existing scores found, calculating for the first time...');
                    await calculateAllScores();
                }

                // Load history for the chart
                const history = await fetchScoreHistory();
                if (history && history.length > 0) {
                    setScoreHistory(history);
                }

                // Load CVE list
                await loadCveList();

            } catch (error) {
                if (error.response && error.response.status === 404) {
                    // No scores yet, calculate them
                    console.log('No score history found, calculating initial scores...');
                    await calculateAllScores();
                    
                    // Load history after calculation
                    const history = await fetchScoreHistory();
                    if (history && history.length > 0) {
                        setScoreHistory(history);
                    }
                    
                    // Load CVE list
                    await loadCveList();
                } else {
                    console.error('Error loading dashboard:', error);
                }
            } finally {
                setLoading(false);
            }
        };

        const loadCveList = async () => {
            try {
                const response = await axios.get('/api/vuln_score_lite/getdashboard');
                if (response.data.cveList) {
                    // Sort by base score (descending)
                    const sortedCves = response.data.cveList.sort((a, b) => {
                        return (b.baseScore || 0) - (a.baseScore || 0);
                    });
                    setCveList(sortedCves);
                    console.log('Loaded CVE list:', sortedCves.length, 'CVEs');
                }
            } catch (error) {
                console.error('Error loading CVE list:', error);
            }
        };

        const calculateAllScores = async () => {
            const results = [];
            
            // Calculate all score modes (backend will auto-save when all 5 are calculated)
            for (let mode = 0; mode <= 5; mode++) {
                const response = await axios.post('/api/vuln_score_lite/updatedashboard', {
                    list: [],
                    mode: mode
                });
                results.push(response.data.newScore);
            }
            

            // Update scores with calculated values
            setScores(prevScores =>
                prevScores.map((score, index) => ({
                    ...score,
                    value: results[index] || 0
                }))
            );

            // Log values
            results.forEach((value, index) => {
                console.log(`Score ${index}: Value=${value.toFixed(2)}`);
            });
        };

        loadDashboard();
    }, []);

    return (
        <div className="container-fluid mt-5">
            <div className="px-4">
                <h1 className="fw-bolder text-primary pt-5 mb-4 text-center mb-4">Dashboard Scores</h1>
            </div>
            <div className="px-4">

                {/*Graphic for vulnerabilty score*/}
                <div className="row">
                    {scores.map((score) => (
                        <ScoreGaugeCard key={score.id} score={score} getTextColor={getTextColor} />
                    ))}
                </div>

                {/*Score History Chart*/}
                <div className='row justify-content-center mt-5'>
                    <div className="">
                        <ScoreHistoryChart 
                            scoreHistory={scoreHistory}
                            scoreLabels={scoreLabels}
                            scoreColors={scoreColors}
                            primaryColor={primaryColor}
                            formatDateTimeLabel={formatDateTimeLabel}
                        />
                    </div>
                </div>
                
                {/*CVE LIST*/}
                <ListDangerous 
                    cveList={cveList}
                    loading={loading}
                    onDeleteCve={deleteCVEFromList}
                />

                <div className="d-flex justify-content-center">
                    <button  className='btn btn-primary px-4 mt-3 mb-5' onClick={addNewCVEInList}>Add new CVE encountered</button>  
                </div>
            </div>
        </div>
    )
}

export default Dashboard;


