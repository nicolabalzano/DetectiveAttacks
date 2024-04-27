export function handleClickRowOfTable(id, type, navigate) {

        if(type === 'attack-pattern') {
            navigate('/attack', { state: { id: id }});
        }
        else if(type === 'campaign') {
            navigate('/campaign', { state: { id: id }});
        }
        else if(type === 'tool') {
            navigate('/tool', { state: { id: id }});
        }
        else if(type === 'malware') {
            navigate('/malware', { state: { id: id }});
        }
        else if(type === 'mitigation') {
            navigate('/mitigation', { state: { id: id }});
        }
        else if(type.includes('asset')) {
            navigate('/asset', { state: { id: id }});
        }
        else if(type.includes('vulnerability')) {
            navigate('/vulnerability', { state: { id: id }});
        }
    }