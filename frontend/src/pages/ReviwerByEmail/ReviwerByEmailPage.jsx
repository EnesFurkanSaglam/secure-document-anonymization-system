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
    const [submitLoading, setSubmitLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch(`http://127.0.0.1:5000/reviewer/assigned-articles?email=${email}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data && data.assigned_articles) {
                    const uniqueArticles = data.assigned_articles.filter((article, index, self) =>
                        index === self.findLastIndex(a => a.article_id === article.article_id)
                    );
                    setAssignedArticles(uniqueArticles);
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
        if (!notes.trim()) {
            alert("Please enter your review notes before submitting.");
            return;
        }

        setSubmitLoading(true);
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
                alert("Review notes saved successfully and sent to the author!");
                setSubmitLoading(false);
                handleCloseModal();

                // Refresh the list to update statuses
                setLoading(true);
                return fetch(`http://127.0.0.1:5000/reviewer/assigned-articles?email=${email}`);
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.assigned_articles) {
                    const uniqueArticles = data.assigned_articles.filter((article, index, self) =>
                        index === self.findLastIndex(a => a.article_id === article.article_id)
                    );
                    setAssignedArticles(uniqueArticles);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error("Error saving notes:", error);
                alert("Failed to save notes! Please try again.");
                setSubmitLoading(false);
            });
    };

    const handlePublish = () => {
        if (!selectedArticle) {
            alert("No article selected!");
            return;
        }

        if (!window.confirm("Are you sure you want to publish this article? This action cannot be undone.")) {
            return;
        }

        setSubmitLoading(true);
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
                setSubmitLoading(false);
                handleCloseModal();

                // Refresh the list to update statuses
                setLoading(true);
                return fetch(`http://127.0.0.1:5000/reviewer/assigned-articles?email=${email}`);
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.assigned_articles) {
                    const uniqueArticles = data.assigned_articles.filter((article, index, self) =>
                        index === self.findLastIndex(a => a.article_id === article.article_id)
                    );
                    setAssignedArticles(uniqueArticles);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error("Error publishing article:", error);
                alert("Failed to publish article! Please try again.");
                setSubmitLoading(false);
            });
    };

    const getStatusClass = (status) => {
        if (status.toLowerCase().includes('pending')) return 'status-pending';
        if (status.toLowerCase().includes('complete')) return 'status-completed';
        if (status.toLowerCase().includes('reject')) return 'status-rejected';
        return '';
    };

    const formatDate = (dateString) => {
        if (!dateString) return "N/A";
        try {
            const date = new Date(dateString);
            return date.toLocaleString();
        } catch (error) {
            return dateString;
        }
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
                            key={article.assignment_id || article.article_id}
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
                                <strong>Assigned Date:</strong> {formatDate(article.assigned_at)}
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
                                <h3>Review Notes</h3>
                                <textarea
                                    className="notes-textarea"
                                    placeholder="Enter your review notes for this article..."
                                    value={notes}
                                    onChange={(e) => setNotes(e.target.value)}
                                    disabled={submitLoading}
                                />
                                <div className="button-container">
                                    <button
                                        className="save-notes-btn"
                                        onClick={handleSaveNotes}
                                        disabled={submitLoading}
                                    >
                                        {submitLoading ? "Saving..." : "Save Notes & Send to Author"}
                                    </button>
                                    <button
                                        className="publish-btn"
                                        onClick={handlePublish}
                                        disabled={submitLoading}
                                    >
                                        {submitLoading ? "Processing..." : "Approve & Publish Article"}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ReviewerByEmailPage;