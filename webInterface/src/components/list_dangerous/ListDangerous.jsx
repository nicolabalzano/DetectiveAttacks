import { Box, Skeleton } from '@mui/material';

const ListDangerous = ({ cveList, loading, onDeleteCve }) => {
    
    const handleDeleteClick = (cveId) => {
        if (onDeleteCve) {
            onDeleteCve(cveId);
        }
    };

    return (
        <div className='mt-2'>
            <h3 className="text-center mb-4">CVE List - Unresolved Vulnerabilities</h3>
            
            {loading ? (
                <div className="text-center">
                    <Box sx={{ width: 1 }}>
                        <Skeleton key="loadingCveList" animation="wave" height="500px" />
                    </Box>
                </div>
            ) : cveList.length === 0 ? (
                <div className="alert alert-info text-center" role="alert">
                    No CVEs in history. Add CVEs to start tracking vulnerabilities.
                </div>
            ) : (
                <div className="table-responsive">
                    <table className="table table-hover table-sorting text-center mb-5">
                        <thead className="table-dark">
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">CVE ID</th>
                                <th scope="col">Description</th>
                                <th scope="col">Base Score</th>
                                <th scope="col">Severity</th>
                                <th scope="col">Published</th>
                                <th scope="col">CWEs</th>
                                <th scope="col">Delete</th>
                            </tr>
                        </thead>
                        <tbody className="table-group-divider">
                            {cveList.map((cve, index) => (
                                <tr key={cve.id} className="border-b border-secondary">
                                    <th scope="row">{index + 1}</th>
                                    <td>
                                        <a 
                                            href={`http://127.0.0.1:8080/vulnerability?id=${cve.id}`} 
                                            target="_blank" 
                                            rel="noopener noreferrer"
                                            className="text-decoration-none"
                                        >
                                            <strong>{cve.id}</strong>
                                        </a>
                                    </td>
                                    <td className="" style={{maxWidth: '300px'}} title={cve.description}>
                                        {cve.description || 'N/A'}
                                    </td>
                                    <td>
                                        <span className={`badge ${
                                            cve.baseScore >= 9.0 ? 'bg-danger' :
                                            cve.baseScore >= 7.0 ? 'bg-warning text-dark' :
                                            cve.baseScore >= 4.0 ? 'bg-info text-dark' :
                                            'bg-success'
                                        }`}>
                                            {cve.baseScore ? cve.baseScore.toFixed(1) : 'N/A'}
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`badge ${
                                            cve.severity === 'CRITICAL' ? 'bg-danger' :
                                            cve.severity === 'HIGH' ? 'bg-warning text-dark' :
                                            cve.severity === 'MEDIUM' ? 'bg-info text-dark' :
                                            cve.severity === 'LOW' ? 'bg-success' :
                                            'bg-secondary'
                                        }`}>
                                            {cve.severity || 'NONE'}
                                        </span>
                                    </td>
                                    <td>{cve.published ? new Date(cve.published).toLocaleDateString('it-IT') : 'N/A'}</td>
                                    <td>
                                        {cve.cwes && cve.cwes.length > 0 ? (
                                            <span className="badge bg-primary">{cve.cwes.length} CWE(s)</span>
                                        ) : (
                                            <span className="text-muted">None</span>
                                        )}
                                    </td>
                                    <td className=''> 
                                        <div 
                                            className="bi bi-trash fs-4 text-secondary" 
                                            data-toggle="tooltip" 
                                            data-placement="top" 
                                            title="Remove CVE"
                                            onClick={() => handleDeleteClick(cve.id)}
                                            onMouseEnter={(e) => e.currentTarget.classList.remove('text-secondary')}
                                            onMouseLeave={(e) => e.currentTarget.classList.add('text-secondary')}
                                            style={{cursor: 'pointer'}}>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default ListDangerous;
