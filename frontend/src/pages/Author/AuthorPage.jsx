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
            <div className="author-card">
                <header className="author-header">
                    <h1 className="author-title">Author Dashboard</h1>
                    <p className="author-subtitle">Manage your content and communications</p>
                </header>

                <div className="author-actions">
                    <button
                        className="author-btn upload"
                        onClick={() => handleNavigation('/upload')}
                    >
                        <span className="btn-icon">+</span>
                        <span className="btn-text">Upload Article</span>
                    </button>

                    <button
                        className="author-btn reupload"
                        onClick={() => handleNavigation('/reupload')}
                    >
                        <span className="btn-icon">↑</span>
                        <span className="btn-text">Reupload Article</span>
                    </button>

                    <button
                        className="author-btn check"
                        onClick={() => handleNavigation('/check-status')}
                    >
                        <span className="btn-icon">✓</span>
                        <span className="btn-text">Check Status</span>
                    </button>

                    <button
                        className="author-btn message"
                        onClick={() => handleNavigation('/messaging')}
                    >
                        <span className="btn-icon">✉</span>
                        <span className="btn-text">Messaging</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AuthorPage;