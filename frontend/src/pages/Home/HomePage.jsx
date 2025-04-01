import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate();

    const handleRoleClick = (role) => {
        switch (role) {
            case 'author':
                navigate('/author');
                break;
            case 'editor':
                navigate('/editor');
                break;
            case 'reviewer':
                navigate('/reviewer');
                break;
            case 'published':
                navigate('/published');
                break;
            default:
                break;
        }
    };

    return (
        <div className="home-container">
            <div className="home-content">
                <h1 className="home-welcome">Welcome</h1>
                <p className="home-description">
                    Welcome to Secure Document Anonymization System. Please select your role.
                </p>

                <div className="home-buttons">
                    <button
                        className="home-button home-button-author"
                        onClick={() => handleRoleClick('author')}
                    >
                        <span className="button-icon">📝</span>
                        <span>Author</span>
                    </button>

                    <button
                        className="home-button home-button-editor"
                        onClick={() => handleRoleClick('editor')}
                    >
                        <span className="button-icon">✏️</span>
                        <span>Editor</span>
                    </button>

                    <button
                        className="home-button home-button-reviewer"
                        onClick={() => handleRoleClick('reviewer')}
                    >
                        <span className="button-icon">👁️</span>
                        <span>Reviewer</span>
                    </button>

                    <button
                        className="home-button home-button-published"
                        onClick={() => handleRoleClick('published')}
                    >
                        <span className="button-icon">📄</span>
                        <span>Published Article</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default HomePage;