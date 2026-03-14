import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { Box } from '@mui/material';

const SEVERITY_ORDER = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1, NONE: 0 };

const SEVERITY_TEXT_CLASS = {
    CRITICAL: 'text-danger',
    HIGH: 'text-warning',
    MEDIUM: 'text-warning',
    LOW: 'text-success',
    NONE: 'text-secondary',
};

const ScoreGaugeCard = ({ score, getTextColor, cveList = [], cveAssetWeights = {} }) => {
    const getTopCves = () => {
        if (!cveList || cveList.length === 0) return [];
        let sorted = [];

        switch (score.id) {
            case 0:
                sorted = [...cveList].sort((a, b) => (b.baseScore || 0) - (a.baseScore || 0));
                break;
            case 1:
                sorted = [...cveList].sort((a, b) => (b.impactScore || 0) - (a.impactScore || 0));
                break;
            case 2:
                sorted = [...cveList].sort((a, b) => (b.exploitabilityScore || 0) - (a.exploitabilityScore || 0));
                break;
            case 3:
                sorted = [...cveList].sort(
                    (a, b) =>
                        (SEVERITY_ORDER[b.severity] ?? 0) - (SEVERITY_ORDER[a.severity] ?? 0) ||
                        (b.baseScore || 0) - (a.baseScore || 0)
                );
                break;
            case 4:
                sorted = [...cveList].sort(
                    (a, b) =>
                        (b.cwes?.length || 0) - (a.cwes?.length || 0) ||
                        (b.baseScore || 0) - (a.baseScore || 0)
                );
                break;
            case 5:
                sorted = [...cveList]
                    .filter(cve => cveAssetWeights[cve.id] != null)
                    .sort((a, b) => (cveAssetWeights[b.id] || 0) - (cveAssetWeights[a.id] || 0));
                break;
            default:
                sorted = [...cveList].sort((a, b) => (b.baseScore || 0) - (a.baseScore || 0));
        }

        return sorted.slice(0, 5);
    };

    const getSortValueLabel = (cve) => {
        switch (score.id) {
            case 0: return `Base: ${(cve.baseScore || 0).toFixed(1)}`;
            case 1: return `Impact: ${(cve.impactScore || 0).toFixed(1)}`;
            case 2: return `Exploit: ${(cve.exploitabilityScore || 0).toFixed(1)}`;
            case 3: return cve.severity || 'NONE';
            case 4: return `CWEs: ${cve.cwes?.length || 0}`;
            case 5: {
                const w = cveAssetWeights[cve.id];
                return w != null ? `Weight: ${w.toFixed(2)}` : 'No assets';
            }
            default: return `${(cve.baseScore || 0).toFixed(1)}`;
        }
    };

    const topCves = getTopCves();
    const scoreColor = getTextColor(score.value, score.max);

    return (
        <div className="col-md-2 col-lg-2 mb-5 text-center">
            <Box sx={{ width: 140, height: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '0 auto' }}>
                <Gauge
                    key={`gauge-${score.id}-${score.value}`}
                    value={score.value}
                    valueMax={score.max}
                    startAngle={-90}
                    endAngle={90}
                    sx={{
                        [`& .${gaugeClasses.valueText}`]: { display: 'none' },
                        [`& .${gaugeClasses.valueArc}`]: { fill: scoreColor },
                    }}
                    text={({ value }) => `${value.toFixed(2)}`}
                />
                <div style={{ color: scoreColor }} className="fs-5 fw-bold mt-n4">
                    {score.value.toFixed(2)}
                </div>
                <div className="text-secondary" style={{ fontSize: '10px' }}>
                    Min: 0 | Max: {score.max}
                </div>
            </Box>

            <h5 className="text-secondary mt-2" style={{ fontSize: '15px' }}>{score.title}</h5>
            <p className="text-secondary mb-0" style={{ fontSize: '12px' }}>{score.subtitle}</p>

            {topCves.length > 0 && (
                <div className="mt-2 text-center">
                    <ol className="d-inline-block text-start ps-3 mb-0">
                        {topCves.map((cve, index) => (
                            <li key={cve.id} className="mb-1">
                                <a
                                    href={`/vulnerability?id=${cve.id}`}
                                    className={`text-decoration-none fw-${index === 0 ? 'bold' : 'normal'} me-1`}
                                    style={{ fontSize: '15px', color: score.color }}
                                    title={cve.description || cve.id}
                                >
                                    {cve.id}
                                </a>
                                <span className={`${score.id === 3 ? (SEVERITY_TEXT_CLASS[cve.severity] || 'text-secondary') : 'text-secondary'} ${score.id === 3 ? 'fw-semibold' : ''}`}
                                    style={{ fontSize: '12px' }}>
                                    {getSortValueLabel(cve)}
                                </span>
                            </li>
                        ))}
                    </ol>
                </div>
            )}
        </div>
    );
};

export default ScoreGaugeCard;
