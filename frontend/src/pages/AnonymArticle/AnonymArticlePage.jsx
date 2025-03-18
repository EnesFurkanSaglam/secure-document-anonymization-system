import React from 'react';
import { useLocation } from 'react-router-dom';
import './AnonymArticlePage.css';

function AnonymArticlePage() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const fileName = queryParams.get('file');
    const pdfUrl = fileName ? `http://127.0.0.1:5000/pdf/${fileName}` : null;

    return (
        <div className="anonym-container">
            <h1 className="anonym-title">Anonym PDF</h1>

            {pdfUrl ? (
                <div className="anonym-content">
                    <div className="anonym-pdf-container">
                        <iframe
                            src={pdfUrl}
                            className="anonym-pdf-frame"
                            title="Anonim PDF"
                        />
                    </div>
                </div>
            ) : (
                <p className="anonym-error-message">Anonym PDF not found.</p>
            )}
        </div>
    );
}

export default AnonymArticlePage;