import axios from "axios";

const API_stix_vulnerability = "http://127.0.0.1:8080/api/stix_vulnerability"

// FETCH ALL THREATS
export const fetchDataAPI = async (searchTerm, selectedTypes, selectedDomains) => {
    // REQUEST TO FLASK API
    let params = {search: searchTerm, types: selectedTypes, domains: selectedDomains};
    let url = new URL(`${API_stix_vulnerability}/api/get_data`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
};

// FETCH FILTERS FOR RESEARCH
export const fetchFilterAPI = async () => {
    return await axios.get(`${API_stix_vulnerability}/api/get_filters`);
}

// FETCH PLATFORMS DATA
export const fetchDataPlatforms = async () => {
    return await axios.get(`${API_stix_vulnerability}/api/get_data/get_platforms`);
}

// FETCH DOMAINS DATA
export const fetchDataDomains = async () => {
    return await axios.get(`${API_stix_vulnerability}/api/get_data/get_domains`);
}

// GET GROUPS REPORT DATA
export const fetchDataReportGroupsAPI = async (idList) => {
    const params = { id_list: idList };
    const url = new URL(`${API_stix_vulnerability}/api/get_data/get_report_groups`);

    // Appending parameters to the URL
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

    try {
        const response = await axios.get(url.toString(), { responseType: 'blob' }); // Ensure you set responseType to 'blob'

        if (response.data.size > 0) {
            const downloadUrl = window.URL.createObjectURL(response.data);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            // Set the default filename for the download
            const now = new Date();
            a.download = 'report_groups_' + now.toISOString().replace(/:/g, '-') + '.pdf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
        } else {
            console.log('No file was returned from the server.');
        }
    } catch (error) {
        console.error('Error downloading the file:', error.response || error);
    }
}



// FETCH ATTACK PATTERNS DATA
export const fetchDataAttackAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_attack_pattern`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

// FETCH ATTACK PATTERNS GROUPED BY CKC PHASES
export const fetchDataAttackPatternsGroupedByPhaseAPI = async () => {
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_attack_patterns_grouped_by_CKCP`);
    return await axios.get(url.toString());
}

export const fetchDataCampaignAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_campaign`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataToolAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_tool_malware`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataMalwareAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_tool_malware`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataAssetAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_asset`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}


export const fetchDataIntrusionSetAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_intrusion_set`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}


export const fetchDataVulnerabilityAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${API_stix_vulnerability}/api/get_data/get_vulnerability`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}
