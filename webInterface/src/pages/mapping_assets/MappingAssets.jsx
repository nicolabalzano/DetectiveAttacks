import React, { useEffect, useState } from 'react';
import './mapping_assets.scss';
import {
    fetchPersonalAssetsAPI,
    addPersonalAssetAPI,
    deletePersonalAssetAPI
} from '../../components/api/fetchAPI.jsx';
import { Skeleton, Box } from '@mui/material';

const EMPTY_FORM = {
    name: '',
    description: '',
    x_mitre_platforms: '',
    x_mitre_sectors: '',
};

const MappingAssets = () => {
    const [assets, setAssets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [form, setForm] = useState(EMPTY_FORM);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.remove('d-flex');
        root_element.classList.remove('align-content-center');
        root_element.classList.remove('justify-content-center');
        root_element.classList.remove('align-items-center');
        root_element.style.margin = '0';
        root_element.style.height = '100vh';

        loadAssets();
    }, []);

    const loadAssets = () => {
        setLoading(true);
        fetchPersonalAssetsAPI()
            .then(r => setAssets(r?.data || []))
            .catch(() => setAssets([]))
            .finally(() => setLoading(false));
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        if (!form.name.trim()) {
            setError('Asset name is required.');
            return;
        }
        setSubmitting(true);
        try {
            const payload = {
                name: form.name.trim(),
                description: form.description.trim(),
                x_mitre_platforms: form.x_mitre_platforms
                    ? form.x_mitre_platforms.split(',').map(s => s.trim()).filter(Boolean)
                    : [],
                x_mitre_sectors: form.x_mitre_sectors
                    ? form.x_mitre_sectors.split(',').map(s => s.trim()).filter(Boolean)
                    : [],
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
        } catch {
            setError('Error while deleting the asset.');
        }
    };

    return (
        <div className="ma-page container-fluid" style={{ marginTop: '80px', paddingBottom: '40px' }}>

            {/* Page header */}
            <div className="ma-header px-4 mb-4">
                <h2 className="text-color fw-bold mb-1">
                    <i className="bi bi-shield-lock me-2" />
                    My Assets
                </h2>
                <p className="text-secondary">
                    Manage your custom assets. They are stored locally and searchable in the{' '}
                    <em>Manual Search</em> page.
                </p>
            </div>

            <div className="d-flex gap-4 flex-wrap flex-lg-nowrap px-4">

                {/* ── ADD FORM ───────────────────────────── */}
                <div className="ma-form-card flex-shrink-0">
                    <h5 className="fw-semibold text-color mb-3">
                        <i className="bi bi-plus-circle me-2 text-primary" />
                        Add new asset
                    </h5>

                    {error && (
                        <div className="alert alert-danger py-2 px-3 small">{error}</div>
                    )}
                    {success && (
                        <div className="alert alert-success py-2 px-3 small">{success}</div>
                    )}

                    <form onSubmit={handleSubmit} noValidate>
                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">
                                Name <span className="text-danger">*</span>
                            </label>
                            <input
                                className="form-control ma-input"
                                type="text"
                                name="name"
                                value={form.name}
                                onChange={handleChange}
                                placeholder="e.g. Web Application Server"
                                required
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">
                                Description
                            </label>
                            <textarea
                                className="form-control ma-input"
                                name="description"
                                value={form.description}
                                onChange={handleChange}
                                rows={3}
                                placeholder="Asset description..."
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label text-secondary small fw-semibold">
                                Platforms
                                <span className="text-secondary fw-normal ms-1">(comma-separated)</span>
                            </label>
                            <input
                                className="form-control ma-input"
                                type="text"
                                name="x_mitre_platforms"
                                value={form.x_mitre_platforms}
                                onChange={handleChange}
                                placeholder="e.g. Windows, Linux"
                            />
                        </div>

                        <div className="mb-4">
                            <label className="form-label text-secondary small fw-semibold">
                                Sectors
                                <span className="text-secondary fw-normal ms-1">(comma-separated)</span>
                            </label>
                            <input
                                className="form-control ma-input"
                                type="text"
                                name="x_mitre_sectors"
                                value={form.x_mitre_sectors}
                                onChange={handleChange}
                                placeholder="e.g. Energy, Healthcare"
                            />
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary w-100"
                            disabled={submitting}
                        >
                            {submitting
                                ? <span className="spinner-border spinner-border-sm me-2" />
                                : <i className="bi bi-plus-lg me-2" />
                            }
                            Save asset
                        </button>
                    </form>
                </div>

                {/* vertical divider */}
                <div className="d-none d-lg-flex align-items-stretch">
                    <div className="vr thick-vr border-primary" />
                </div>

                {/* ── ASSETS TABLE ───────────────────────── */}
                <div className="flex-grow-1">
                    <h5 className="fw-semibold text-color mb-3">
                        <i className="bi bi-list-ul me-2 text-primary" />
                        Saved assets
                        {!loading && (
                            <span className="badge bg-primary ms-2 fs-6">{assets.length}</span>
                        )}
                    </h5>

                    {loading ? (
                        <Box sx={{ width: 1 }}>
                            {[...Array(4)].map((_, i) => (
                                <Skeleton key={i} animation="wave" height="60px" />
                            ))}
                        </Box>
                    ) : assets.length === 0 ? (
                        <div className="ma-empty-state text-center text-secondary mt-5">
                            <i className="bi bi-inbox fs-1 d-block mb-2 opacity-50" />
                            <p>No custom assets yet. Add one using the form!</p>
                        </div>
                    ) : (
                        <div className="table-responsive">
                            <table className="table table-hover ma-table">
                                <thead>
                                    <tr>
                                        <th className="text-secondary">Name</th>
                                        <th className="text-secondary">Description</th>
                                        <th className="text-secondary">Platforms</th>
                                        <th className="text-secondary">Sectors</th>
                                        <th className="text-secondary">ID</th>
                                        <th />
                                    </tr>
                                </thead>
                                <tbody className="table-group-divider">
                                    {assets.map(asset => (
                                        <tr key={asset.id}>
                                            <td className="fw-semibold text-color">{asset.name}</td>
                                            <td className="text-secondary small">
                                                {asset.description
                                                    ? (asset.description.length > 80
                                                        ? asset.description.slice(0, 80) + '…'
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
                                                <code className="ma-id-badge">{asset.id}</code>
                                            </td>
                                            <td className="text-end">
                                                <button
                                                    className="btn btn-sm btn-outline-danger"
                                                    title="Delete"
                                                    onClick={() => handleDelete(asset.id)}
                                                >
                                                    <i className="bi bi-trash" />
                                                </button>
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
    );
};

export default MappingAssets;
