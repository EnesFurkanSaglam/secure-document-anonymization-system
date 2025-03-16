import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ReviewerPage.css';

function ReviewerPage() {
    const [reviewers, setReviewers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        setLoading(true);
        fetch('http://127.0.0.1:5000/reviewer/all-reviewers')
            .then(response => response.json())
            .then(data => {
                if (data && data.reviewers) {
                    setReviewers(data.reviewers);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error('Error occurred while fetching reviewers:', error);
                setLoading(false);
            });
    }, []);

    const handleReviewerClick = (email) => {
        navigate(`/reviewer/${email}`);
    };

    const getInitialLetters = (email) => {
        if (!email) return "?";
        const parts = email.split("_");
        if (parts.length > 1) {
            return parts[0].charAt(0).toUpperCase();
        }
        return email.charAt(0).toUpperCase();
    };

    return (
        <div className="reviewer-container">
            <h1 className="reviewer-title">Reviewers</h1>

            {loading ? (
                <div className="reviewer-loading">Loading...</div>
            ) : (
                <div className="reviewer-grid">
                    {reviewers.map((reviewer) => (
                        <div
                            key={reviewer.id}
                            className="reviewer-card"
                            onClick={() => handleReviewerClick(reviewer.email)}
                        >
                            <div className="reviewer-card-header">
                                <div className="reviewer-avatar">
                                    {getInitialLetters(reviewer.email)}
                                </div>
                                <div className="reviewer-id">#{reviewer.id}</div>
                            </div>

                            <div className="reviewer-card-body">
                                <div className="reviewer-email">
                                    {reviewer.email}
                                </div>

                                <div className="reviewer-interests">
                                    {reviewer.interests}
                                </div>

                                <div className="reviewer-dates">
                                    <span>Created: {new Date(reviewer.created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {reviewers.length === 0 && !loading && (
                <div className="reviewer-empty">No reviewers found.</div>
            )}
        </div>
    );
}

export default ReviewerPage;
