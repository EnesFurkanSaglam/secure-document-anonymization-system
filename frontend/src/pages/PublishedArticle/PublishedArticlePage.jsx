import React, { useState, useEffect } from 'react';
import './PublishedArticlePage.css';

function PublishedArticlePage() {
    const [articles, setArticles] = useState([]);
    const [selectedPdf, setSelectedPdf] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetch('http://127.0.0.1:5000/author/published')
            .then((response) => response.json())
            .then((data) => {
                setArticles(data.published_articles);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching articles:', error);
                setLoading(false);
            });
    }, []);

    const handlePdfClick = (pdfPath) => {
        const fileName = pdfPath.split(/[\\/]/).pop();
        setSelectedPdf(fileName);
        // Scroll to PDF preview section
        setTimeout(() => {
            document.querySelector('.pdf-preview-container')?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    };

    return (
        <div className="published-container">
            <div className="published-header">
                <h1 className="published-title">Published Articles</h1>
                <p className="published-subtitle">Your research contributions to the scientific community</p>
            </div>

            {loading ? (
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading your published articles...</p>
                </div>
            ) : articles.length === 0 ? (
                <div className="no-articles">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="12" y1="18" x2="12" y2="12"></line>
                        <line x1="9" y1="15" x2="15" y2="15"></line>
                    </svg>
                    <h3>No published articles yet</h3>
                    <p>Your published research will appear here</p>
                </div>
            ) : (
                <div className="articles-grid">
                    {articles.map((article) => (
                        <div key={article.id} className="article-card">
                            <div className="article-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14 2 14 8 20 8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                    <polyline points="10 9 9 9 8 9"></polyline>
                                </svg>
                            </div>
                            <div className="article-content">
                                <h3 className="article-title">{article.title || "Untitled Article"}</h3>
                                {article.publication_date && (
                                    <p className="article-date">Published: {new Date(article.publication_date).toLocaleDateString()}</p>
                                )}
                                {article.journal && (
                                    <p className="article-journal">{article.journal}</p>
                                )}
                                <p className="article-keywords"><span>Keywords:</span> {article.keywords || "Not specified"}</p>
                                <button
                                    className="view-pdf-btn"
                                    onClick={() => handlePdfClick(article.published_pdf_path)}
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                    View PDF
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {selectedPdf && (
                <div className="pdf-preview-container">
                    <div className="preview-header">
                        <h2 className="preview-title">PDF Preview</h2>
                        <button
                            className="close-preview-btn"
                            onClick={() => setSelectedPdf(null)}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div className="iframe-container">
                        <iframe
                            src={`http://127.0.0.1:5000/pdf/publish/${selectedPdf}`}
                            className="pdf-iframe"
                            title="PDF Preview"
                            frameBorder="0"
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

export default PublishedArticlePage;