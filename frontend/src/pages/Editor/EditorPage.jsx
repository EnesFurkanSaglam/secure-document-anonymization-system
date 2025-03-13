import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './EditorPage.css';



function EditorPage() {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        setLoading(true);
        fetch('http://127.0.0.1:5000/editor/list-articles')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch articles');
                }
                return response.json();
            })
            .then(data => {

                if (data.articles) {
                    setArticles(data.articles);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching articles:', error);
                setError(error.message);
                setLoading(false);
            });
    }, []);

    return (
        <div className="edp-container">
            <div className="edp-header">
                <h1 className="edp-title">Articles</h1>
            </div>

            {loading ? (
                <div className="edp-empty-state">Loading articles...</div>
            ) : error ? (
                <div className="edp-empty-state">Error: {error}</div>
            ) : articles.length === 0 ? (
                <div className="edp-empty-state">No articles found.</div>
            ) : (
                <ul className="edp-article-grid">
                    {articles.map(article => (
                        <li key={article.id} className="edp-article-card">
                            <Link to={`/articles/${article.id}`} className="edp-article-link">
                                <div className="edp-article-header">
                                    <svg
                                        className="edp-article-icon"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                    >
                                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                        <polyline points="14 2 14 8 20 8"></polyline>
                                        <line x1="16" y1="13" x2="8" y2="13"></line>
                                        <line x1="16" y1="17" x2="8" y2="17"></line>
                                        <polyline points="10 9 9 9 8 9"></polyline>
                                    </svg>
                                    <span>Document #{article.id}</span>
                                </div>
                                <div className="edp-article-body">
                                    <h2 className="edp-article-title">
                                        Article ID: {article.id}
                                    </h2>
                                    <div className="edp-article-meta">
                                        {article.status && <span className="edp-article-status">Status: {article.status}</span>}
                                        {article.created_at && <span className="edp-article-date">Submitted: {new Date(article.created_at).toLocaleDateString()}</span>}
                                    </div>
                                </div>
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default EditorPage;