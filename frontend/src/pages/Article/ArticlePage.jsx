import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './ArticlePage.css';
import { Link } from 'react-router-dom';

function ArticlePage() {
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showLogs, setShowLogs] = useState(false);
    const [logs, setLogs] = useState([]);
    const [loadingLogs, setLoadingLogs] = useState(false);
    const navigate = useNavigate();
    const { articleId } = useParams();

    useEffect(() => {
        if (articleId) {
            setLoading(true);
            fetch(`http://127.0.0.1:5000/editor/get-article-by-id?article_id=${articleId}`)
                .then(res => {
                    if (!res.ok) {
                        throw new Error('There was a problem retrieving the article');
                    }
                    return res.json();
                })
                .then(data => {
                    setArticle(data.article);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('An error occurred while retrieving the article:', err);
                    setError(err.message);
                    setLoading(false);
                });
        }
    }, [articleId]);

    const handleOriginalClick = () => {
        if (article && article.original_pdf_path) {
            const parts = article.original_pdf_path.split(/[\\/]/);
            const fileName = parts[parts.length - 1];
            navigate(`/original?file=${fileName}`, { state: { articleId: article.id } });
        }
    };

    const handleAnonymClick = () => {
        if (article && article.anonymized_pdf_path) {
            const parts = article.anonymized_pdf_path.split(/[\\/]/);
            const fileName = parts[parts.length - 1];
            navigate(`/anonym?file=${fileName}`);
        } else {
            alert("Anonymous PDF is not available.");
        }
    };

    const handleShowLogs = () => {
        if (!showLogs && article) {
            setLoadingLogs(true);
            fetch(`http://127.0.0.1:5000/editor/get-logs-by-article?article_id=${article.id}`)
                .then(res => {
                    if (!res.ok) {
                        throw new Error('There was a problem retrieving the logs');
                    }
                    return res.json();
                })
                .then(data => {
                    setLogs(data.logs);
                    setLoadingLogs(false);
                    setShowLogs(true);
                })
                .catch(err => {
                    console.error('An error occurred while retrieving logs:', err);
                    setLoadingLogs(false);
                    alert('Failed to load logs. Please try again.');
                });
        } else {
            setShowLogs(!showLogs);
        }
    };

    const formatLogAction = (action) => {
        return action.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };

    return (
        <div className="article-container">
            <div className="article-header">
                <h1 className="article-title">Article Information</h1>
                {article && (
                    <button className="article-logs-button" onClick={handleShowLogs}>
                        {showLogs ? 'Hide Logs' : 'Show Logs'}
                    </button>
                )}
            </div>

            {loading ? (
                <div className="article-loading">
                    <div className="article-loading-spinner"></div>
                    <p>Loading article information...</p>
                </div>
            ) : error ? (
                <div className="article-error">
                    <p>{error}</p>
                    <button className="article-retry-button" onClick={() => window.location.reload()}>
                        Try again
                    </button>
                </div>
            ) : article ? (
                <>
                    {showLogs && (
                        <div className="article-logs-container">
                            <div className="article-logs-header">
                                <h2>Article Activity Logs</h2>
                                <button className="article-logs-close" onClick={() => setShowLogs(false)}>×</button>
                            </div>
                            <div className="article-logs-content">
                                {loadingLogs ? (
                                    <div className="article-loading">
                                        <div className="article-loading-spinner"></div>
                                        <p>Loading logs...</p>
                                    </div>
                                ) : logs.length > 0 ? (
                                    <ul className="article-logs-list">
                                        {logs.map(log => (
                                            <li key={log.id} className="article-log-item">
                                                <div className="article-log-action">
                                                    {formatLogAction(log.action)}
                                                </div>
                                                <div className="article-log-details">
                                                    <span className="article-log-user">User ID: {log.user_id}</span>
                                                    <span className="article-log-time">
                                                        {new Date(log.timestamp).toLocaleString('tr-TR')}
                                                    </span>
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="article-logs-empty">No logs available for this article.</p>
                                )}
                            </div>
                        </div>
                    )}

                    <div className="article-content">
                        <div className="article-info-card">
                            <div className="article-info-item">
                                <span className="article-info-label">ID:</span>
                                <span className="article-info-value">{article.id}</span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Tracking Code:</span>
                                <span className="article-info-value article-tracking-code">{article.tracking_code}</span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Status:</span>
                                <span className="article-info-value">
                                    <span className={`article-status article-status-${article.status.toLowerCase()}`}>
                                        {article.status}
                                    </span>
                                </span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Keywords:</span>
                                <span className="article-info-value">
                                    {article.keywords ? article.keywords : <span className="article-empty-value">Unspecified</span>}
                                </span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Author ID:</span>
                                <span className="article-info-value">{article.author_id}</span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Created at:</span>
                                <span className="article-info-value">{new Date(article.created_at).toLocaleString('tr-TR')}</span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">Updated at:</span>
                                <span className="article-info-value">{new Date(article.updated_at).toLocaleString('tr-TR')}</span>
                            </div>

                            <div className="article-info-item">
                                <span className="article-info-label">PDF Status:</span>
                                <span className="article-info-value">
                                    <div className="article-pdf-status">
                                        <div className="article-pdf-status-item">
                                            <span className="article-pdf-label">Original:</span>
                                            <span className={`article-pdf-indicator ${article.original_pdf_path ? 'article-pdf-available' : 'article-pdf-unavailable'}`}>
                                                {article.original_pdf_path ? 'Available' : 'Not Available'}
                                            </span>
                                        </div>
                                        <div className="article-pdf-status-item">
                                            <span className="article-pdf-label">Anonim:</span>
                                            <span className={`article-pdf-indicator ${article.anonymized_pdf_path ? 'article-pdf-available' : 'article-pdf-unavailable'}`}>
                                                {article.anonymized_pdf_path ? 'Available' : 'Not Available'}
                                            </span>
                                        </div>
                                    </div>
                                </span>
                            </div>
                        </div>

                        <Link to="/editor-messaging" className="edp-message-btn" state={{ trackingCode: article.tracking_code }}>
                            <svg
                                className="edp-message-icon"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                            </svg>
                            Go to Messages
                        </Link>

                        <div className="article-actions">
                            <button
                                className="article-button article-button-primary"
                                onClick={handleOriginalClick}
                                disabled={!article.original_pdf_path}
                            >
                                Show Original PDF
                            </button>

                            <button
                                className="article-button article-button-secondary"
                                onClick={handleAnonymClick}
                                disabled={!article.anonymized_pdf_path}
                            >
                                Show Anonym PDF
                            </button>
                        </div>
                    </div>
                </>
            ) : (
                <p className="article-not-found">Article not found.</p>
            )}
        </div>
    );
}

export default ArticlePage;