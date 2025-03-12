import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Document, Page, pdfjs } from 'react-pdf';
import { Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import './ArticlePage.css';


pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

function ArticlePage() {
    const { articleId } = useParams();
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activePdf, setActivePdf] = useState(null);
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    useEffect(() => {
        setLoading(true);
        fetch(`http://127.0.0.1:5000/editor/get-article-by-id?article_id=${articleId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch article');
                }
                return response.json();
            })
            .then(data => {
                if (data.article) {
                    setArticle(data.article);
                } else {
                    throw new Error('Article data not found');
                }
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching article:', error);
                setError(error.message);
                setLoading(false);
            });
    }, [articleId]);

    const handleViewPdf = (pdfPath) => {
        const filename = pdfPath.split(/[\\/]/).pop();
        setActivePdf(`http://127.0.0.1:5000/pdf/${filename}`);
    };

    const onDocumentLoadSuccess = ({ numPages }) => {
        setNumPages(numPages);
        setPageNumber(1);
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loading-content">
                    <div className="loading-spinner"></div>
                    <p>Loading article...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                <div className="error-content">
                    <h2>Error Loading Article</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="article-page">
            <div className="article-container">
                {activePdf ? (
                    <div className="pdf-viewer-card">
                        <div className="pdf-header">
                            <h2>PDF Viewer</h2>
                            <button onClick={() => setActivePdf(null)} className="back-button">
                                Back to Article
                            </button>
                        </div>
                        <div className="pdf-frame-container">
                            <Worker>
                                <Document
                                    file={activePdf}
                                    onLoadSuccess={onDocumentLoadSuccess}
                                    className="pdf-document"
                                >
                                    <Page pageNumber={pageNumber} />
                                </Document>
                            </Worker>
                            <div className="pdf-controls">
                                <button disabled={pageNumber <= 1} onClick={() => setPageNumber(pageNumber - 1)}>
                                    Previous
                                </button>
                                <span>Page {pageNumber} of {numPages}</span>
                                <button disabled={pageNumber >= numPages} onClick={() => setPageNumber(pageNumber + 1)}>
                                    Next
                                </button>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="article-card">
                        <div className="article-header">
                            <h1>Article Details</h1>
                        </div>
                        <div className="article-body">
                            <div className="info-grid">
                                <div className="info-box">
                                    <p className="info-label">Article ID</p>
                                    <p className="info-value">{article.id}</p>
                                </div>
                                <div className="info-box">
                                    <p className="info-label">Status</p>
                                    <span className={`status-badge ${article.status}`}>
                                        {article.status}
                                    </span>
                                </div>
                                <div className="info-box">
                                    <p className="info-label">Tracking Code</p>
                                    <p className="info-value">{article.tracking_code}</p>
                                </div>
                            </div>
                            <div className="pdf-buttons">
                                {article.original_pdf_path && (
                                    <button onClick={() => handleViewPdf(article.original_pdf_path)} className="pdf-button">
                                        View Original PDF
                                    </button>
                                )}
                                {article.anonymized_pdf_path && (
                                    <button onClick={() => handleViewPdf(article.anonymized_pdf_path)} className="pdf-button">
                                        View Anonymized PDF
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ArticlePage;
