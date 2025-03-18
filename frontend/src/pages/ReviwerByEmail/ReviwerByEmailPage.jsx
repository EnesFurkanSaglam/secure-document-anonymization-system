import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './ReviwerByEmailPage.css';

function ReviewerByEmailPage() {
    const { email } = useParams();
    const [assignedArticles, setAssignedArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedArticle, setSelectedArticle] = useState(null);
    const [showPdfModal, setShowPdfModal] = useState(false);
    const [notes, setNotes] = useState('');
    const [isFinal, setIsFinal] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch(`http://127.0.0.1:5000/reviewer/assigned-articles?email=${email}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.assigned_articles) {
                    setAssignedArticles(data.assigned_articles);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching assigned articles:', err);
                setError(err);
                setLoading(false);
            });
    }, [email]);

    const handleArticleClick = (article) => {
        setSelectedArticle(article);
        setShowPdfModal(true);
        setNotes('');
        setIsFinal(false);
    };

    const handleCloseModal = () => {
        setShowPdfModal(false);
        setSelectedArticle(null);
    };

    const handleSaveNotes = () => {
        const reviewData = {
            email: email,
            tracking_code: selectedArticle.tracking_code,
            review_text: notes,
            is_final: isFinal
        };

        fetch('http://127.0.0.1:5000/reviewer/submit-review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                alert("Notes saved successfully!");

            })
            .catch(error => {
                console.error("Error saving notes:", error);
                alert("Failed to save notes!");
            });
    };

    const pusblished = () => {
        if (!selectedArticle) {
            alert("No article selected!");
            return;
        }

        fetch('http://127.0.0.1:5000/reviewer/publish-article', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ article_id: selectedArticle.article_id })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                alert("Article published successfully!");
                handleCloseModal();
            })
            .catch(error => {
                console.error("Error publishing article:", error);
                alert("Failed to publish article!");
            });
    };


    const getStatusClass = (status) => {
        if (status.toLowerCase().includes('pending')) return 'status-pending';
        if (status.toLowerCase().includes('complete')) return 'status-completed';
        if (status.toLowerCase().includes('reject')) return 'status-rejected';
        return '';
    };

    return (
        <div className="assigned-articles-container">
            <h1>Assigned Articles - {email}</h1>

            {loading ? (
                <div className="loading-spinner">Loading...</div>
            ) : error ? (
                <div className="error-message">Error: {error.message}</div>
            ) : assignedArticles.length > 0 ? (
                <div className="articles-list">
                    {assignedArticles.map(article => (
                        <div
                            key={article.assignment_id}
                            className="article-card"
                            onClick={() => handleArticleClick(article)}
                        >
                            <p><strong>Article ID:</strong> {article.article_id}</p>
                            <p>
                                <strong>Status:</strong>
                                <span className={`status ${getStatusClass(article.status)}`}>
                                    {article.status}
                                </span>
                            </p>
                            <p><strong>Tracking Code:</strong> {article.tracking_code}</p>
                            <p>
                                <strong>Assigned Date:</strong> {article.assigned_at ? new Date(article.assigned_at).toLocaleString() : "N/A"}
                            </p>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="no-articles">No assigned articles found.</div>
            )}

            {showPdfModal && selectedArticle && (
                <div className="pdf-modal">
                    <div className="pdf-modal-content">
                        <div className="pdf-header">
                            <h2>
                                Article ID: {selectedArticle.article_id} - {selectedArticle.tracking_code}
                            </h2>
                            <button className="close-button" onClick={handleCloseModal}>×</button>
                        </div>
                        <div className="pdf-container">
                            <iframe
                                className="pdf-viewer"
                                src={`http://127.0.0.1:5000/pdf/anonym/${selectedArticle.anonymized_pdf_path.split(/[\\/]/).pop()}`}
                                title={`PDF Viewer for Article ${selectedArticle.article_id}`}
                            />
                            <div className="notes-section">
                                <h3>Notes</h3>
                                <textarea
                                    className="notes-textarea"
                                    placeholder="Enter your notes about the article here..."
                                    value={notes}
                                    onChange={(e) => setNotes(e.target.value)}
                                />
                                <button className="save-notes-btn" onClick={handleSaveNotes}>
                                    Save Notes and send back the author
                                </button>
                                <button className="save-notes-btn" onClick={pusblished}>
                                    Publish
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ReviewerByEmailPage;
