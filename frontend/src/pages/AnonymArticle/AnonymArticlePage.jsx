import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { ChevronDown, ChevronUp, UserCircle, FileText } from 'lucide-react';
import './AnonymArticlePage.css';

function AnonymArticlePage() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const fileName = queryParams.get('file');
    const articleId = queryParams.get('id');
    const pdfUrl = fileName ? `http://127.0.0.1:5000/pdf/anonym/${fileName}` : null;

    const [showReviewers, setShowReviewers] = useState(false);
    const [reviewers, setReviewers] = useState([]);
    const [loadingReviewers, setLoadingReviewers] = useState(false);

    const toggleReviewers = () => {
        if (showReviewers) {
            setShowReviewers(false);
        } else {
            fetchReviewers();
        }
    };

    const fetchReviewers = () => {
        setLoadingReviewers(true);
        fetch(`http://127.0.0.1:5000/reviewer/all-reviewers`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('There was a problem retrieving the reviewers');
                }
                return res.json();
            })
            .then(data => {
                setReviewers(data.reviewers);
                setLoadingReviewers(false);
                setShowReviewers(true);
            })
            .catch(err => {
                console.error('An error occurred while retrieving reviewers:', err);
                setLoadingReviewers(false);
                alert('Failed to load reviewers. Please try again.');
            });
    };

    const handleAssignReviewer = (reviewerId) => {
        if (!articleId) {
            alert('Article ID is missing.');
            return;
        }
        fetch(`http://127.0.0.1:5000/editor/assign-article`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                article_id: articleId,
                reviewer_id: reviewerId,
            }),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Assignment failed');
                }
                return res.json();
            })
            .then(data => {
                alert(`Assignment successful: ${data.message}`);
                setShowReviewers(false);
            })
            .catch(err => {
                console.error('An error occurred during assignment:', err);
                alert('Failed to assign reviewer. Please try again.');
            });
    };

    return (
        <div className="anonym-container">
            <div className="anonym-header">
                <h1 className="anonym-title">
                    <FileText className="title-icon" />
                    Anonymized Article Review
                </h1>
            </div>

            {pdfUrl ? (
                <div className="anonym-content">
                    <div className="anonym-pdf-container">
                        <iframe
                            src={pdfUrl}
                            className="anonym-pdf-frame"
                            title="Anonim PDF"
                        />
                    </div>
                    <div className="anonym-actions">
                        <button
                            className="anonym-reviewers-toggle"
                            onClick={toggleReviewers}
                            disabled={loadingReviewers}
                        >
                            {loadingReviewers ? (
                                'Loading Reviewers...'
                            ) : (
                                <>
                                    {showReviewers ? <ChevronUp /> : <ChevronDown />}
                                    {showReviewers ? 'Hide Reviewers' : 'Show Reviewers'}
                                </>
                            )}
                        </button>
                        {showReviewers && (
                            <div className="anonym-reviewers-container">
                                {reviewers.length > 0 ? (
                                    <ul className="anonym-reviewers-list">
                                        {reviewers.map(reviewer => (
                                            <li key={reviewer.id} className="anonym-reviewer-item">
                                                <button
                                                    className="anonym-reviewer-button"
                                                    onClick={() => handleAssignReviewer(reviewer.id)}
                                                >
                                                    <UserCircle className="reviewer-icon" />
                                                    <div className="reviewer-details">
                                                        <span className="reviewer-name">
                                                            {reviewer.name || `Reviewer ${reviewer.id}`}
                                                        </span>
                                                        <span className="reviewer-interests">
                                                            {reviewer.interests || 'No specified interests'}
                                                        </span>
                                                    </div>
                                                </button>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="anonym-reviewers-empty">No reviewers available.</p>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            ) : (
                <div className="anonym-error-message">
                    <p>Anonymized PDF not found</p>
                    <span>Please check the file URL and try again</span>
                </div>
            )}
        </div>
    );
}

export default AnonymArticlePage;