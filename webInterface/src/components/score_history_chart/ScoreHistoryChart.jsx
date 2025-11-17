import { LineChart } from '@mui/x-charts/LineChart';
import { Box } from '@mui/material';

const ScoreHistoryChart = ({ scoreHistory, scoreLabels, scoreColors, primaryColor, formatDateTimeLabel }) => {
    return (
        <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {/* Custom Legend */}
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 3, mt: 2, flexWrap: 'wrap' }}>
                {scoreLabels.map((label, index) => (
                    <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Box
                            sx={{
                                width: 20,
                                height: 2,
                                backgroundColor: scoreColors[index],
                                borderRadius: '2px',
                            }}
                        />
                        <span className="text-secondary" style={{ fontSize: '14px' }}>{label}</span>
                    </Box>
                ))}
            </Box>

            <LineChart
                series={scoreLabels.map((label, index) => ({
                    label: label,
                    data: scoreHistory.map(entry => entry.scores[index]),
                    color: scoreColors[index],
                }))}
                xAxis={[{ 
                    scaleType: 'time',
                    data: scoreHistory.map(entry => entry.timestamp.getTime()),
                    valueFormatter: (value) => formatDateTimeLabel(new Date(value)),
                }]}
                width={1200}
                height={400}
                margin={{ top: 10, right: 10, bottom: 100, left: 50 }}
                slotProps={{
                    legend: { 
                        hidden: true,
                    },
                }}
                sx={{
                    '& .MuiChartsAxis-bottom .MuiChartsAxis-line': {
                        stroke: primaryColor || '#0dfdfdff',
                        strokeWidth: 2,
                    },
                    '& .MuiChartsAxis-left .MuiChartsAxis-line': {
                        stroke: primaryColor || '#0dfdfdff',
                        strokeWidth: 2,
                    },
                    '& .MuiChartsAxis-bottom .MuiChartsAxis-tick': {
                        stroke: primaryColor || '#0dfdfdff',
                    },
                    '& .MuiChartsAxis-left .MuiChartsAxis-tick': {
                        stroke: primaryColor || '#0dfdfdff',
                    },
                    '& .MuiChartsAxis-bottom text': {
                        fill: primaryColor || '#0dfdfdff',
                        fontSize: '11px',
                        dy: 4,
                    },
                    '& .MuiChartsAxis-left text': {
                        fill: primaryColor || '#0dfdfdff',
                        fontSize: '12px',
                    },
                    '& .MuiChartsAxis-bottom text[text-anchor="end"]': {
                        transform: 'rotate(-45deg)',
                        transformOrigin: 'right center',
                    },
                }}
            />
        </Box>
    );
};

export default ScoreHistoryChart;
