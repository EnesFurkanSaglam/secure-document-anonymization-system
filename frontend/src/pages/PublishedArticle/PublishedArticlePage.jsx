import React, { useState, useEffect } from 'react';
import './PublishedArticlePage.css';

function PublishedArticlePage() {
    const [articles, setArticles] = useState([]);
    const [selectedPdf, setSelectedPdf] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/author/published')
            .then((response) => response.json())
            .then((data) => {
                setArticles(data.published_articles);
            })
            .catch((error) => console.error('Error fetching articles:', error));
    }, []);

    const handlePdfClick = (pdfPath) => {
        const fileName = pdfPath.split(/[\\/]/).pop();
        setSelectedPdf(fileName);
    };

    return (
        <div className="published-container">
            <h1 className="published-title">Published Articles</h1>
            <div className="articles-grid">
                {articles.map((article) => (
                    <div key={article.id} className="article-card">
                        <p className="article-keywords"><strong>Keywords:</strong> {article.keywords}</p>
                        <button
                            className="view-pdf-btn"
                            onClick={() => handlePdfClick(article.published_pdf_path)}
                        >
                            View PDF
                        </button>
                    </div>
                ))}
            </div>
            {selectedPdf && (
                <div className="pdf-preview-container">
                    <h2 className="preview-title">PDF Preview</h2>
                    <iframe
                        src={`http://127.0.0.1:5000/pdf/publish/${selectedPdf}`}
                        className="pdf-iframe"
                        title="PDF Preview"
                        frameBorder="0"
                    />
                </div>
            )}
        </div>
    );
}

export default PublishedArticlePage;