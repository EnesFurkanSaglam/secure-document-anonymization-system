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
            <h1 className="home-welcome">Welcome!</h1>
            <p className="home-description">
                Welcome Secure Document Anonymization System. Please select role.
            </p>
            <div className="home-buttons">
                <button
                    className="home-button home-button-author"
                    onClick={() => handleRoleClick('author')}
                >
                    Author
                </button>
                <button
                    className="home-button home-button-editor"
                    onClick={() => handleRoleClick('editor')}
                >
                    Editor
                </button>
                <button
                    className="home-button home-button-reviewer"
                    onClick={() => handleRoleClick('reviewer')}
                >
                    Reviewer
                </button>
                <button
                    className="home-button home-button-reviewer"
                    onClick={() => handleRoleClick('published')}
                >
                    Published Article
                </button>
            </div>
        </div>
    );
};

export default HomePage;
