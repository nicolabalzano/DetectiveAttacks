import { useState, useEffect } from 'react';
import {
    addAttackPatternToMappingAPI,
    removeAttackPatternFromMappingAPI,
} from '../api/fetchAPI.jsx';

/**
 * Two-column AP management panel for a CVE vulnerability page.
 *
 * Props:
 *  - cveId          {string}  The CVE ID (e.g. "CVE-2017-0199")
 *  - linkedAps      {Array}   Initial list of linked APs: [{id, name}]
 *  - allAttackPatterns {Object} Grouped AP data: { phase: [{ID, Name}] }
 *  - onLinkedChange {Function} Called with updated [{id, name}] after every mutation
 */
const VulnApPanel = ({ cveId, linkedAps = [], allAttackPatterns = {}, onLinkedChange }) => {
    const [linked, setLinked] = useState(linkedAps);
    const [search, setSearch] = useState('');
    const [busyId, setBusyId] = useState(null); // AP id currently being mutated
    const [error, setError] = useState('');

    useEffect(() => {
        setLinked(linkedAps);
    }, [linkedAps]);

    const linkedIds = new Set(linked.map(a => a.id));

    const searchLower = search.trim().toLowerCase();
    const hasSearch = searchLower.length > 0;

    const filteredGrouped = Object.entries(allAttackPatterns).reduce((acc, [phase, patterns]) => {
        const matches = hasSearch
            ? patterns.filter(ap =>
                ap.Name.toLowerCase().includes(searchLower) ||
                ap.ID.toLowerCase().includes(searchLower))
            : patterns;
        if (matches.length > 0) acc[phase] = matches;
        return acc;
    }, {});

    const hasResults = Object.keys(filteredGrouped).length > 0;

    const handleAdd = async (ap) => {
        if (linkedIds.has(ap.ID) || busyId) return;
        setBusyId(ap.ID);
        setError('');
        try {
            await addAttackPatternToMappingAPI(cveId, ap.ID);
            window.location.reload();
        } catch {
            setError(`Failed to add ${ap.ID}.`);
            setBusyId(null);
        }
    };

    const handleRemove = async (ap) => {
        if (busyId) return;
        setBusyId(ap.id);
        setError('');
        try {
            await removeAttackPatternFromMappingAPI(cveId, ap.id);
            window.location.reload();
        } catch {
            setError(`Failed to remove ${ap.id}.`);
            setBusyId(null);
        }
    };

    const scrollStyle = {
        overflowY: 'scroll',
        maxHeight: '280px',
        scrollbarWidth: 'thin',
        scrollbarColor: 'var(--bs-secondary) transparent',
    };

    return (
        <div className="card shadow-sm border-0 rounded-3 mt-4 mb-5">
            <div className="card-body p-4">
                <h5 className="fw-semibold mb-3">
                    <i className="bi bi-diagram-3 me-2 text-primary" />
                    Attack Pattern Mapping
                </h5>

                {error && (
                    <div className="alert alert-danger py-2 px-3 small mb-3">{error}</div>
                )}

                <div className="d-flex gap-4 flex-column flex-md-row">

                    {/* ── Left: search + browse all APs ── */}
                    <div className="flex-grow-1">
                        <p className="small fw-semibold text-secondary mb-2">
                            <i className="bi bi-search me-1" />
                            Search attack patterns
                        </p>
                        <input
                            className="form-control form-control-sm mb-2"
                            placeholder="Filter by name or ID…"
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                        />
                        <div style={scrollStyle} className="border rounded p-2">
                            {!hasResults && !hasSearch ? (
                                <p className="text-secondary small text-center mt-3">Loading…</p>
                            ) : !hasResults ? (
                                <p className="text-secondary small text-center mt-3">No results</p>
                            ) : (
                                Object.entries(filteredGrouped).map(([phase, patterns]) => (
                                    <div key={phase}>
                                        <div className="bg-primary px-2 py-1 small fw-bold text-secondary text-uppercase sticky-top"
                                            style={{ fontSize: '0.72rem', backdropFilter: 'blur(4px)' }}>
                                            {phase.replace(/-/g, ' ')}
                                        </div>
                                        {patterns.map(ap => (
                                            <div key={ap.ID}
                                                className="d-flex justify-content-between align-items-center py-1 px-1 border-bottom">
                                                <div>
                                                    <span className="small fw-semibold">{ap.Name}</span>
                                                    <span className="text-secondary small ms-2 opacity-75">{ap.ID}</span>
                                                </div>
                                                <button
                                                    className="btn btn-sm btn-outline-primary py-0 px-2 ms-2 flex-shrink-0"
                                                    disabled={linkedIds.has(ap.ID) || busyId === ap.ID}
                                                    onClick={() => handleAdd(ap)}
                                                >
                                                    {busyId === ap.ID
                                                        ? <span className="spinner-border spinner-border-sm" />
                                                        : linkedIds.has(ap.ID)
                                                            ? <i className="bi bi-check" />
                                                            : <i className="bi bi-plus" />}
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* ── Divider ── */}
                    <div className="vr d-none d-md-block" />

                    {/* ── Right: linked APs ── */}
                    <div style={{ minWidth: '220px', maxWidth: '340px', width: '100%' }}>
                        <p className="small fw-semibold text-secondary mb-2">
                            <i className="bi bi-link-45deg me-1" />
                            Linked attack patterns
                            <span className="badge bg-primary ms-2">{linked.length}</span>
                        </p>
                        <div style={scrollStyle} className="border rounded p-2">
                            {linked.length === 0 ? (
                                <p className="text-secondary small text-center mt-3">
                                    No attack patterns linked yet
                                </p>
                            ) : (
                                linked.map(ap => (
                                    <div key={ap.id}
                                        className="d-flex justify-content-between align-items-center py-1 px-1 border-bottom">
                                        <div>
                                            <span className="small fw-semibold">{ap.name || ap.id}</span>
                                            <span className="text-secondary small ms-2 opacity-75">{ap.id}</span>
                                        </div>
                                        <button
                                            className="btn btn-sm btn-outline-danger py-0 px-2 ms-2 flex-shrink-0"
                                            disabled={busyId === ap.id}
                                            onClick={() => handleRemove(ap)}
                                        >
                                            {busyId === ap.id
                                                ? <span className="spinner-border spinner-border-sm" />
                                                : <i className="bi bi-x" />}
                                        </button>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default VulnApPanel;
