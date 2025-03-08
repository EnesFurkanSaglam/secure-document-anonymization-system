import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AuthorPage.css';

const AuthorPage = () => {
    const navigate = useNavigate();

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <div className="author-container">
            <header className="author-header">
                <h1 className="author-title">Author Dashboard</h1>
            </header>
            <div className="author-actions">
                <button
                    className="author-btn author-btn-upload"
                    onClick={() => handleNavigation('/upload')}
                >
                    Upload Article
                </button>
                <button
                    className="author-btn author-btn-reupload"
                    onClick={() => handleNavigation('/reupload')}
                >
                    Reupload Article
                </button>
                <button
                    className="author-btn author-btn-check"
                    onClick={() => handleNavigation('/check-status')}
                >
                    Check Status
                </button>
                <button
                    className="author-btn author-btn-message"
                    onClick={() => handleNavigation('/messaging')}
                >
                    Messaging
                </button>
            </div>
        </div>
    );
};

export default AuthorPage;
