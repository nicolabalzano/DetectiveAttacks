import React, { useEffect, useState, useCallback } from 'react';
import './mapping_assets.scss';
import {
    fetchPersonalAssetsAPI,
    fetchAllMitreAssetsAPI,
    addPersonalAssetAPI,
    deletePersonalAssetAPI,
    updatePersonalAssetAttackPatternsAPI,
    updateAssetImpactAPI,
} from '../../components/api/fetchAPI.jsx';
import { fetchDataAttackPatternsGroupedByPhaseAPI } from '../../components/api/fetchAPI.jsx';
import { navigateToThreats } from '../../components/handle_routing_threats/HandleRoutingThreats.jsx';
import { Skeleton, Box } from '@mui/material';

const ROW_HEIGHT = 35; // Approx height of a row in px
const HEADER_HEIGHT = 30; // Approx height of the table header
const MAX_TOTAL_HEIGHT = 65; // Max allowed VH for both tables combined before overflowing page

const EMPTY_FORM = {
    name: '',
    description: '',
    x_mitre_platforms: '',
    x_mitre_sectors: '',
};

// ─── Attack Pattern Panel ────────────────────────────────────────────────────
const AttackPatternPanel = ({ asset, allAttackPatterns, onSave }) => {
    const [linked, setLinked] = useState(asset.attack_patterns || []);
    const [search, setSearch] = useState('');
    const [saving, setSaving] = useState(false);
    const [dirty, setDirty] = useState(false);

    const linkedIds = new Set(linked.map(a => a.id));

    const hasSearch = search.trim().length > 0;
    const searchLower = search.toLowerCase();

    const filteredGrouped = Object.entries(allAttackPatterns).reduce((acc, [phase, patterns]) => {
        const matchingPatterns = hasSearch
            ? patterns.filter(ap => ap.Name.toLowerCase().includes(searchLower) || ap.ID.toLowerCase().includes(searchLower))
            : patterns;

        if (matchingPatterns.length > 0) {
            acc[phase] = matchingPatterns;
        }
        return acc;
    }, {});

    const hasResults = Object.keys(filteredGrouped).length > 0;

    const addAP = (ap) => {
        if (linkedIds.has(ap.ID)) return;
        const updated = [...linked, { id: ap.ID, name: ap.Name }];
        setLinked(updated);
        setDirty(true);
    };

    const removeAP = (id) => {
        setLinked(prev => prev.filter(a => a.id !== id));
        setDirty(true);
    };

    const save = async () => {
        setSaving(true);
        try {
            const resp = await updatePersonalAssetAttackPatternsAPI(asset.id, linked);
            onSave(resp?.data || []);
            setDirty(false);
        } finally {
            setSaving(false);
        }
    };

    return (
        <tr className="ma-ap-panel-row">
            <td colSpan={6} className="p-0">
                <div className="ma-ap-panel">
                    <div className="ma-ap-panel-inner">

                        {/* Left: search + results */}
                        <div className="ma-ap-col">
                            <p className="small fw-semibold text-secondary mb-2">
                                <i className="bi bi-search me-1" />
                                Search attack patterns
                            </p>
                            <input
                                className="form-control form-control-sm ma-input mb-2"
                                placeholder="Filter by name or ID…"
                                value={search}
                                onChange={e => setSearch(e.target.value)}
                            />
                            <div className="ma-ap-list" style={{
                                overflowY: 'scroll',
                                maxHeight: '280px',
                                scrollbarWidth: 'thin',
                                scrollbarColor: 'white transparent',
                            }}>
                                {!hasResults && !hasSearch ? (
                                    <p className="text-secondary small text-center mt-3">Loading…</p>
                                ) : !hasResults ? (
                                    <p className="text-secondary small text-center mt-3">No results</p>
                                ) : Object.entries(filteredGrouped).map(([phase, patterns]) => (
                                    <div key={phase}>
                                        <div className="bg-primary px-2 py-1 small fw-bold text-secondary text-uppercase sticky-top" style={{ fontSize: '0.75rem', backdropFilter: 'blur(4px)' }}>
                                            {phase.replace(/-/g, ' ')}
                                        </div>
                                        {patterns.map(ap => (
                                            <div key={ap.ID} className="ma-ap-item d-flex justify-content-between align-items-center">
                                                <div>
                                                    <span className="small fw-semibold">{ap.Name}</span>
                                                    <span className="text-secondary small ms-2 opacity-75">{ap.ID}</span>
                                                </div>
                                                <button
                                                    className="btn btn-sm btn-outline-primary py-0 px-2"
                                                    disabled={linkedIds.has(ap.ID)}
                                                    onClick={() => addAP(ap)}
                                                >
                                                    {linkedIds.has(ap.ID) ? <i className="bi bi-check" /> : <i className="bi bi-plus" />}
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Divider */}
                        <div className="ma-ap-divider" />

                        {/* Right: linked patterns */}
                        <div className="ma-ap-col">
                            <p className="small fw-semibold text-secondary mb-2">
                                <i className="bi bi-link-45deg me-1" />
                                Linked attack patterns
                                <span className="badge bg-primary ms-2">{linked.length}</span>
                            </p>
                            <div className="ma-ap-list" style={{
                                overflowY: 'scroll',
                                maxHeight: '280px',
                                scrollbarWidth: 'thin',
                                scrollbarColor: 'white transparent',
                            }}>
                                {linked.length === 0 ? (
                                    <p className="text-secondary small text-center mt-3">
                                        No attack patterns linked yet
                                    </p>
                                ) : linked.map(ap => (
                                    <div key={ap.id} className="ma-ap-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <span className="small fw-semibold">{ap.name}</span>
                                            <span className="text-secondary small ms-2 opacity-75">{ap.id}</span>
                                        </div>
                                        <button
                                            className="btn btn-sm btn-outline-danger py-0 px-2"
                                            onClick={() => removeAP(ap.id)}
                                        >
                                            <i className="bi bi-x" />
                                        </button>
                                    </div>
                                ))}
                            </div>

                            {dirty && (
                                <button
                                    className="btn btn-sm btn-primary w-100 mt-2"
                                    onClick={save}
                                    disabled={saving}
                                >
                                    {saving
                                        ? <span className="spinner-border spinner-border-sm me-1" />
                                        : <i className="bi bi-floppy me-1" />
                                    }
                                    Save changes
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    );
};

// ─── Main page ───────────────────────────────────────────────────────────────
const MappingAssets = () => {
    const [assets, setAssets] = useState([]);
    const [mitreAssets, setMitreAssets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [mitreLoading, setMitreLoading] = useState(true);
    const [allAttackPatterns, setAllAttackPatterns] = useState({});
    const [apLoading, setApLoading] = useState(true);
    const [form, setForm] = useState(EMPTY_FORM);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [expandedId, setExpandedId] = useState(null);

    // Dynamic height calculation
    const getTableHeights = useCallback(() => {
        const savedCount = assets.length;
        const mitreCount = mitreAssets.length;

        // If an asset is expanded to Manage AP, give the Saved table lots of space
        // and aggressively shrink the Mitre one so the user can scroll within the AP menu easily.
        if (expandedId) {
            return { saved: '45vh', mitre: '20vh' };
        }

        // If both have 6+ items or are roughly equal, split 50/50 (35vh each)
        if ((savedCount >= 6 && mitreCount >= 6) || (savedCount > 0 && mitreCount > 0 && Math.abs(savedCount - mitreCount) <= 2)) {
            return { saved: '35vh', mitre: '35vh' };
        }

        // Calculate needed pixels
        const savedNeededPx = HEADER_HEIGHT + (savedCount * ROW_HEIGHT);
        const mitreNeededPx = HEADER_HEIGHT + (mitreCount * ROW_HEIGHT);

        // Convert approx px to VH (assuming 1080p display for rough estimate, 1vh ≈ 10px)
        // We'll use a safer approach: determine percentages of the 70vh max

        // If one is very small (or empty)
        if (savedCount === 0) return { saved: 'auto', mitre: '70vh' };
        if (mitreCount === 0) return { saved: '70vh', mitre: 'auto' };

        // Ratio based allocation
        const totalRows = savedCount + mitreCount;
        let savedVh = Math.max(15, Math.floor((savedCount / totalRows) * MAX_TOTAL_HEIGHT));
        let mitreVh = Math.max(15, Math.floor((mitreCount / totalRows) * MAX_TOTAL_HEIGHT));

        // Let's cap them at the actual needed height so we don't have empty space
        // if the total rows are low
        const totalNeededPx = savedNeededPx + mitreNeededPx;

        // Return computed or fallback to auto if they don't fill the screen
        return {
            saved: totalRows < 12 ? 'auto' : `${savedVh}vh`,
            mitre: totalRows < 12 ? 'auto' : `${mitreVh}vh`
        };
    }, [assets.length, mitreAssets.length, expandedId]);

    const tableHeights = getTableHeights();

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.remove('d-flex');
        root_element.classList.remove('align-content-center');
        root_element.classList.remove('justify-content-center');
        root_element.classList.remove('align-items-center');
        root_element.style.margin = '0';
        root_element.style.height = '100vh';
        root_element.style.overflow = 'hidden';

        loadAssets();

        fetchDataAttackPatternsGroupedByPhaseAPI()
            .then(r => setAllAttackPatterns(r?.data || {}))
            .catch(() => setAllAttackPatterns({}))
            .finally(() => setApLoading(false));
    }, []);

    const loadAssets = () => {
        setLoading(true);
        fetchPersonalAssetsAPI()
            .then(r => setAssets(r?.data || []))
            .catch(() => setAssets([]))
            .finally(() => setLoading(false));

        setMitreLoading(true);
        fetchAllMitreAssetsAPI()
            .then(r => setMitreAssets(r?.data || []))
            .catch(() => setMitreAssets([]))
            .finally(() => setMitreLoading(false));
    };

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        if (!form.name.trim()) { setError('Asset name is required.'); return; }
        setSubmitting(true);
        try {
            const payload = {
                name: form.name.trim(),
                description: form.description.trim(),
                x_mitre_platforms: form.x_mitre_platforms
                    ? form.x_mitre_platforms.split(',').map(s => s.trim()).filter(Boolean) : [],
                x_mitre_sectors: form.x_mitre_sectors
                    ? form.x_mitre_sectors.split(',').map(s => s.trim()).filter(Boolean) : [],
            };
            const response = await addPersonalAssetAPI(payload);
            setAssets(response?.data || []);
            setForm(EMPTY_FORM);
            setSuccess('Asset added successfully!');
        } catch {
            setError('Error while saving. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            const response = await deletePersonalAssetAPI(id);
            setAssets(response?.data || []);
            if (expandedId === id) setExpandedId(null);
        } catch {
            setError('Error while deleting the asset.');
        }
    };

    const toggleExpand = (id) => setExpandedId(prev => prev === id ? null : id);

    const handleImpactChange = async (assetId, newImpact, isMitre = false) => {
        try {
            await updateAssetImpactAPI(assetId, newImpact);
            if (isMitre) {
                setMitreAssets(prev => prev.map(a => a.id === assetId ? { ...a, impact: newImpact } : a));
            } else {
                setAssets(prev => prev.map(a => a.id === assetId ? { ...a, impact: newImpact } : a));
            }
        } catch {
            setError('Error updating impact rating.');
        }
    };

    return (
        <div className="ma-page container-fluid d-flex flex-column" style={{ height: 'calc(100vh - 70px)', marginTop: '70px', overflow: 'hidden' }}>

            {/* Header */}
            <div className="ma-header px-4 mb-4">
                <h2 className="text-color fw-bold mb-1">
                    <i className="bi bi-shield-lock me-2" />
                    My Assets
                </h2>
                <p className="text-secondary">
                    Manage your custom assets. They are stored locally and searchable in the{' '}
                    <em>Manual Search</em> page. Click <strong>Manage AP</strong> on any row to link attack patterns.
                </p>
            </div>

            <div className="d-flex gap-4 flex-wrap flex-lg-nowrap px-4 flex-grow-1" style={{ overflow: 'hidden' }}>

                {/* ── ADD FORM ─────────────────────────────── */}
                <div className="ma-form-card flex-shrink-0">
                    <h5 className="fw-semibold text-color mb-3">
                        <i className="bi bi-plus-circle me-2 text-primary" />
                        Add new asset
                    </h5>

                    {error && <div className="alert alert-danger py-2 px-3 small">{error}</div>}
                    {success && <div className="alert alert-success py-2 px-3 small">{success}</div>}

                    <form onSubmit={handleSubmit} noValidate>
                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">
                                Name <span className="text-danger">*</span>
                            </label>
                            <input className="form-control ma-input" type="text" name="name"
                                value={form.name} onChange={handleChange}
                                placeholder="e.g. Web Application Server" required />
                        </div>
                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">Description</label>
                            <textarea className="form-control ma-input" name="description"
                                value={form.description} onChange={handleChange}
                                rows={3} placeholder="Asset description..." />
                        </div>
                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">
                                Platforms <span className="text-secondary fw-normal">(comma-separated)</span>
                            </label>
                            <input className="form-control ma-input" type="text" name="x_mitre_platforms"
                                value={form.x_mitre_platforms} onChange={handleChange}
                                placeholder="e.g. Windows, Linux" />
                        </div>
                        <div className="mb-4">
                            <label className="form-label text-secondary small fw-semibold">
                                Sectors <span className="text-secondary fw-normal">(comma-separated)</span>
                            </label>
                            <input className="form-control ma-input" type="text" name="x_mitre_sectors"
                                value={form.x_mitre_sectors} onChange={handleChange}
                                placeholder="e.g. Energy, Healthcare" />
                        </div>
                        <button type="submit" className="btn btn-primary w-100" disabled={submitting}>
                            {submitting
                                ? <span className="spinner-border spinner-border-sm me-2" />
                                : <i className="bi bi-plus-lg me-2" />}
                            Save asset
                        </button>
                    </form>
                </div>

                {/* vertical divider */}
                <div className="d-none d-lg-flex align-items-stretch">
                    <div className="vr thick-vr border-primary" />
                </div>

                {/* ── ASSETS TABLE ─────────────────────────── */}
                <div className="flex-grow-1 d-flex flex-column gap-4 pb-3" style={{ overflowY: 'auto' }}>

                    {/* CUSTOM ASSETS */}
                    <div>
                        <h5 className="fw-semibold text-color mb-3">
                            <i className="bi bi-list-ul me-2 text-primary" />
                            Saved assets
                            {!loading && <span className="badge bg-primary ms-2 fs-6">{assets.length}</span>}
                        </h5>

                        {loading ? (
                            <Box sx={{ width: 1 }}>
                                {[...Array(4)].map((_, i) => <Skeleton key={i} animation="wave" height="60px" />)}
                            </Box>
                        ) : assets.length === 0 ? (
                            <div className="ma-empty-state text-center text-secondary mt-5">
                                <i className="bi bi-inbox fs-1 d-block mb-2 opacity-50" />
                                <p>No custom assets yet. Add one using the form!</p>
                            </div>
                        ) : (
                            <div className="search-result" style={{ maxHeight: tableHeights.saved }}>
                                <table className="table table-hover table-sorting mb-0">
                                    <thead className="position-sticky top-0 z-1" style={{ backgroundColor: 'var(--bs-body-bg)' }}>
                                        <tr>
                                            <th className="text-secondary">ID</th>
                                            <th className="text-secondary">Name</th>
                                            <th className="text-secondary">Impact</th>
                                            <th className="text-secondary">Description</th>
                                            <th className="text-secondary">Platforms</th>
                                            <th className="text-secondary">Sectors</th>
                                            <th className="text-secondary">Attack Patterns</th>
                                            <th />
                                        </tr>
                                    </thead>
                                    <tbody className="table-group-divider">
                                        {assets.map(asset => (
                                            <React.Fragment key={asset.id}>
                                                <tr className={expandedId === asset.id ? 'ma-row-active' : ''}>
                                                    <td>
                                                        <span className="fs-6 text-decoration-underline link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" role="button" onClick={() => navigateToThreats(asset.id, asset.type)}>
                                                            {asset.id}
                                                        </span>
                                                    </td>
                                                    <td className="fw-semibold text-color">{asset.name}</td>
                                                    <td>
                                                        <select
                                                            className="form-select form-select-sm"
                                                            value={asset.impact || 3}
                                                            onChange={(e) => handleImpactChange(asset.id, parseInt(e.target.value), false)}
                                                            style={{ width: '65px', fontSize: '13px' }}
                                                        >
                                                            {[1, 2, 3, 4, 5].map(v => <option key={v} value={v}>{v}</option>)}
                                                        </select>
                                                    </td>
                                                    <td className="text-secondary small">
                                                        {asset.description
                                                            ? (asset.description.length > 60
                                                                ? asset.description.slice(0, 60) + '…'
                                                                : asset.description)
                                                            : <span className="opacity-50">—</span>}
                                                    </td>
                                                    <td className="small">
                                                        {asset.x_mitre_platforms?.length
                                                            ? asset.x_mitre_platforms.join(', ')
                                                            : <span className="opacity-50">—</span>}
                                                    </td>
                                                    <td className="small">
                                                        {asset.x_mitre_sectors?.length
                                                            ? asset.x_mitre_sectors.join(', ')
                                                            : <span className="opacity-50">—</span>}
                                                    </td>
                                                    <td>
                                                        {asset.attack_patterns?.length
                                                            ? <span className="badge bg-primary">{asset.attack_patterns.length}</span>
                                                            : <span className="opacity-50 small">—</span>}
                                                    </td>
                                                    <td className="text-end" style={{ whiteSpace: 'nowrap' }}>
                                                        <button
                                                            className={`btn btn-sm me-1 ${expandedId === asset.id ? 'btn-primary' : 'btn-outline-primary'}`}
                                                            title="Manage attack patterns"
                                                            disabled={apLoading}
                                                            onClick={() => toggleExpand(asset.id)}
                                                        >
                                                            <i className="bi bi-diagram-3 me-1" />
                                                            Manage AP
                                                        </button>
                                                        <button
                                                            className="btn btn-sm btn-outline-danger"
                                                            title="Delete"
                                                            onClick={() => handleDelete(asset.id)}
                                                        >
                                                            <i className="bi bi-trash" />
                                                        </button>
                                                    </td>
                                                </tr>

                                                {/* Attack Pattern Panel */}
                                                {expandedId === asset.id && (
                                                    <AttackPatternPanel
                                                        asset={asset}
                                                        allAttackPatterns={allAttackPatterns}
                                                        onSave={(updatedAssets) => setAssets(updatedAssets)}
                                                    />
                                                )}
                                            </React.Fragment>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>

                    {/* MITRE ASSETS */}
                    <div>
                        <h5 className="fw-semibold text-color mb-3">
                            <i className="bi bi-list-ul me-2 text-primary" />
                            Mitre Asset
                            {!mitreLoading && <span className="badge bg-primary ms-2 fs-6">{mitreAssets.length}</span>}
                        </h5>

                        {mitreLoading ? (
                            <Box sx={{ width: 1 }}>
                                {[...Array(4)].map((_, i) => <Skeleton key={i} animation="wave" height="60px" />)}
                            </Box>
                        ) : mitreAssets.length === 0 ? (
                            <div className="ma-empty-state text-center text-secondary mt-5">
                                <i className="bi bi-inbox fs-1 d-block mb-2 opacity-50" />
                                <p>No Mitre assets found.</p>
                            </div>
                        ) : (
                            <div className="search-result" style={{ maxHeight: tableHeights.mitre }}>
                                <table className="table table-hover table-sorting mb-0">
                                    <thead className="position-sticky top-0 z-1" style={{ backgroundColor: 'var(--bs-body-bg)' }}>
                                        <tr>
                                            <th className="text-secondary">ID</th>
                                            <th className="text-secondary">Name</th>
                                            <th className="text-secondary">Impact</th>
                                            <th className="text-secondary">Description</th>
                                            <th className="text-secondary">Platforms</th>
                                            <th className="text-secondary">Sectors</th>
                                            <th className="text-secondary">Attack Patterns</th>
                                        </tr>
                                    </thead>
                                    <tbody className="table-group-divider">
                                        {mitreAssets.map(asset => (
                                            <tr key={asset.id}>
                                                <td>
                                                    <span className="fs-6 text-decoration-underline link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" role="button" onClick={() => navigateToThreats(asset.id, asset.type)}>
                                                        {asset.id}
                                                    </span>
                                                </td>
                                                <td className="fw-semibold text-color">{asset.name}</td>
                                                <td>
                                                    <select
                                                        className="form-select form-select-sm"
                                                        value={asset.impact || 3}
                                                        onChange={(e) => handleImpactChange(asset.id, parseInt(e.target.value), true)}
                                                        style={{ width: '65px', fontSize: '13px' }}
                                                    >
                                                        {[1, 2, 3, 4, 5].map(v => <option key={v} value={v}>{v}</option>)}
                                                    </select>
                                                </td>
                                                <td className="text-secondary small">
                                                    {asset.description
                                                        ? (asset.description.length > 60
                                                            ? asset.description.slice(0, 60) + '…'
                                                            : asset.description)
                                                        : <span className="opacity-50">—</span>}
                                                </td>
                                                <td className="small">
                                                    {asset.x_mitre_platforms?.length
                                                        ? asset.x_mitre_platforms.join(', ')
                                                        : <span className="opacity-50">—</span>}
                                                </td>
                                                <td className="small">
                                                    {asset.x_mitre_sectors?.length
                                                        ? asset.x_mitre_sectors.join(', ')
                                                        : <span className="opacity-50">—</span>}
                                                </td>
                                                <td>
                                                    {asset.attack_patterns?.length
                                                        ? <span className="badge bg-primary">{asset.attack_patterns.length}</span>
                                                        : <span className="opacity-50 small">—</span>}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default MappingAssets;
