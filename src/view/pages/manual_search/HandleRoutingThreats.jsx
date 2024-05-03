export function navigateToThreats(id, type) {
    let url;
    console.log(type);
    if((type && type === 'attack-pattern') || (id[0] === 'T' || id.substring(0,5)==='AML.T')) {
        url = '/attack';
    }
    else if((type && type.includes('vulnerability')) || id.substring(0,3)==='CVE') {
        url = '/vulnerability';
    }
    else if((type && type === 'campaign') || id[0] === 'C' || id.substring(0,6)==='AML.CS') {
        url = '/campaign';
    }
    else if((type && type === 'tool') || id[0] === 'S') {
        url = '/tool';
    }
    else if((type && type === 'malware') || id[0] === 'S') {
        url = '/malware';
    }
    else if((type && type === 'mitigation') || id[0] === 'M') {
        url = '/mitigation';
    }
    else if((type && type.includes('asset')) || id[0] === 'A') {
        url = '/asset';
    }

    if (url) {
        window.open(url + '?id=' + id, '_blank');
    }
}