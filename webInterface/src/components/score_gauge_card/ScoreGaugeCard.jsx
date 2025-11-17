import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { Box } from '@mui/material';

const ScoreGaugeCard = ({ score, getTextColor }) => {
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
                        [`& .${gaugeClasses.valueText}`]: {
                            display: 'none',
                        },
                        [`& .${gaugeClasses.valueArc}`]: {
                            fill: getTextColor(score.value, score.max),
                        },
                    }}
                    text={({ value }) => `${value.toFixed(2)}`}
                />
                <div style={{ color: getTextColor(score.value, score.max), fontSize: '20px', fontWeight: 'bold', marginTop: '-35px' }}>
                    {score.value.toFixed(2)}
                </div>
                <div style={{ fontSize: '10px', color: '#666', marginTop: '2px' }}>
                    Min: 0 | Max: {score.max}
                </div>
            </Box>
            <h5 className="text-secondary mt-2" style={{ fontSize: '15px' }}>{score.title}</h5>
            <p className="text-secondary" style={{ fontSize: '12px', color: '#999', margin: '0' }}>{score.subtitle}</p>
        </div>
    );
};

export default ScoreGaugeCard;
