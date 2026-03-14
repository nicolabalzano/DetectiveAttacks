import { useState, useEffect } from 'react';
import axios from 'axios';
import ScoreGaugeCard from '../../components/score_gauge_card/ScoreGaugeCard';
import ScoreHistoryChart from '../../components/score_history_chart/ScoreHistoryChart';
import ListDangerous from '../../components/list_dangerous/ListDangerous';
import { Box, Skeleton } from "@mui/material";

const Dashboard = () => {
    // Get Bootstrap primary color from CSS variable
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--bs-secondary').trim();

    const [scores, setScores] = useState([
        { id: 0, title: "Base Score", subtitle: "(Simple Average)", value: 0, max: 10, color: '#1976d2' },
        { id: 1, title: "Impact Score", subtitle: "(Weighted by Impact)", value: 0, max: 10, color: '#d32f2f' },
        { id: 2, title: "Exploitability", subtitle: "(Weighted by Exploitability)", value: 0, max: 10, color: '#f57c00' },
        { id: 3, title: "Severity", subtitle: "(Weighted by Severity)", value: 0, max: 10, color: '#fbc02d' },
        { id: 4, title: "CWE Count", subtitle: "(Weighted by Weaknesses)", value: 0, max: 10, color: '#388e3c' },
        { id: 5, title: "Asset Weight", subtitle: "(Weighted by Assets Impact)", value: 0, max: 10, color: '#7b1fa2' },
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
    const [bulkCveInput, setBulkCveInput] = useState("");
    const [isAddingBulk, setIsAddingBulk] = useState(false);
    const [cveAssetWeights, setCveAssetWeights] = useState({});

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

    const addNewCVEInList = async () => {
        const cveId = prompt("Enter the CVE ID (e.g., CVE-2021-44228):");
        if (cveId) {
            try {
                const response = await axios.post('/api/vuln_score_lite/addNewCVEInList', { cveId: cveId.trim() });
                if (response.data.success) {
                    alert(`CVE ${cveId} added successfully!`);
                    // Refresh the list and dashboard
                    window.location.reload();
                } else {
                    alert(`Failed to add CVE: ${response.data.message || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error adding CVE:', error);
                alert(`Error adding CVE: ${error.response?.data?.error || error.message}`);
            }
        }
    }

    const addBulkCVEsFromInput = async () => {
        if (!bulkCveInput.trim()) return;

        const cveIds = bulkCveInput.split(/\s+/).filter(id => id.trim() !== "");
        if (cveIds.length === 0) return;

        setIsAddingBulk(true);
        try {
            const response = await axios.post('/api/vuln_score_lite/addBulkCVEs', { cveIds: cveIds });
            if (response.data.success) {
                const { added, failed, already_present } = response.data.results;
                let message = `Processed ${cveIds.length} CVEs.\n`;
                if (added.length > 0) message += `Added: ${added.join(", ")}\n`;
                if (already_present.length > 0) message += `Already present: ${already_present.join(", ")}\n`;
                if (failed.length > 0) {
                    message += `Failed: ${failed.map(f => `${f.cveId} (${f.error})`).join(", ")}`;
                }

                alert(message);
                setBulkCveInput("");
                window.location.reload();
            } else {
                alert(`Failed to add CVEs: ${response.data.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error adding bulk CVEs:', error);
            alert(`Error adding CVEs: ${error.response?.data?.error || error.message}`);
        } finally {
            setIsAddingBulk(false);
        }
    }

    const deleteCVEFromList = async (cveId) => {
        if (window.confirm(`Are you sure you want to remove ${cveId} from the list?`)) {
            try {
                const response = await axios.post('/api/vuln_score_lite/deleteCVEFromList', { cveId: cveId });
                if (response.data.success) {
                    // Remove from local state
                    setCveList(prevList => prevList.filter(cve => cve.id !== cveId));
                    // Optionally refresh dashboard scores if needed, but list update is immediate
                    // To fully sync scores, we might want to reload or re-fetch scores
                    // For now, let's just update the list UI
                } else {
                    alert(`Failed to remove CVE: ${response.data.message}`);
                }
            } catch (error) {
                console.error('Error removing CVE:', error);
                alert(`Error removing CVE: ${error.response?.data?.error || error.message}`);
            }
        }
    }

    const resetDashboard = async () => {
        if (window.confirm(`Are you sure you want to reset the entire dashboard and clear history?`)) {
            try {
                const response = await axios.post('/api/vuln_score_lite/resetdashboard');
                if (response.data.success) {
                    alert('Dashboard history cleared correctly!');
                    setScores(prevScores => prevScores.map(s => ({ ...s, value: 0 })));
                    setScoreHistory([]);
                    setCveList([]);
                    window.location.reload();
                } else {
                    alert(`Failed to reset: ${response.data.message}`);
                }
            } catch (error) {
                console.error('Error resetting dashboard:', error);
                alert(`Error resetting dashboard: ${error.response?.data?.error || error.message}`);
            }
        }
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

                    // Fetch asset weights for each CVE (for Asset Weight score card)
                    const weightEntries = await Promise.all(
                        sortedCves.map(async (cve) => {
                            try {
                                const r = await axios.get(
                                    `/api/stix_and_vulnerability/get_data/get_assets_and_impacts_for_cve`,
                                    { params: { cve_id: cve.id } }
                                );
                                const assets = Array.isArray(r.data) ? r.data : [];
                                const weight = assets.length > 0
                                    ? (assets.reduce((s, a) => s + (a.impact || 3), 0) / assets.length / 5.0)
                                    : null;
                                return [cve.id, weight];
                            } catch {
                                return [cve.id, null];
                            }
                        })
                    );
                    setCveAssetWeights(Object.fromEntries(weightEntries));
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
                        <ScoreGaugeCard key={score.id} score={score} getTextColor={getTextColor} cveList={cveList} cveAssetWeights={cveAssetWeights} />
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

                {/*Add CVEs*/}
                <div className="card shadow-sm border-0 rounded-3 mt-4">
                    <div className="card-body p-4">
                        <h5 className="card-title fw-bold">Bulk Add CVEs</h5>
                        <p className="text-hint small mb-3">Enter CVE IDs separated by spaces (e.g., CVE-2021-44228 CVE-2024-12345)</p>
                        <div className="input-group">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="CVE-2021-44228 CVE-2024-12345 ..."
                                value={bulkCveInput}
                                onChange={(e) => setBulkCveInput(e.target.value)}
                                disabled={isAddingBulk}
                            />
                            <button
                                className="btn btn-primary px-4"
                                onClick={addBulkCVEsFromInput}
                                disabled={isAddingBulk || !bulkCveInput.trim()}
                            >
                                {isAddingBulk ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                        Adding...
                                    </>
                                ) : (
                                    'Add CVEs'
                                )}
                            </button>
                        </div>
                    </div>
                </div>

                {/*CVE LIST*/}
                <ListDangerous
                    cveList={cveList}
                    loading={loading}
                    onDeleteCve={deleteCVEFromList}

                />

                {/*Add single CVE
                <div className="d-flex justify-content-center">
                    <button className='btn btn-outline-secondary px-4 mt-3 mb-5' onClick={addNewCVEInList}>
                        <i className="bi bi-plus-circle me-2"></i>
                        Add single CVE (Legacy)
                    </button>
                </div>*/}

                {/* Floating Reset Button */}
                <button
                    className='btn btn-primary px-4 py-2 position-fixed bottom-0 end-0 m-4 shadow z-3 rounded-pill'
                    onClick={resetDashboard}
                    title="Reset dashboard and clear all history"
                >
                    <i className="bi bi-arrow-counterclockwise me-2"></i>
                    Reset Dashboard
                </button>
            </div>
        </div>
    )
}

export default Dashboard;

