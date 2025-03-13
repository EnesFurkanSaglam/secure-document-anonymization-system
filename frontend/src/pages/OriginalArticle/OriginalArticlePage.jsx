import React from 'react';
import { useLocation } from 'react-router-dom';
import './OriginalArticlePage.css';

function OriginalArticlePage() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const fileName = queryParams.get('file');
    const pdfUrl = fileName ? `http://127.0.0.1:5000/pdf/${fileName}` : null;

    const handleAnonymize = () => {
        console.log("anonym click");
    };

    return (
        <div className="original-container">
            <h1 className="original-title">Orijinal PDF</h1>

            {pdfUrl ? (
                <div className="original-content">
                    <div className="original-sidebar">
                        <div className="original-checkbox-group">
                            <label className="original-checkbox-label">
                                <input type="checkbox" className="original-checkbox" />
                                <span className="original-checkbox-text">Example</span>
                            </label>

                            <label className="original-checkbox-label">
                                <input type="checkbox" className="original-checkbox" />
                                <span className="original-checkbox-text">Example</span>
                            </label>
                        </div>

                        <button
                            className="original-anonymize-button"
                            onClick={handleAnonymize}
                        >
                            Anonymize
                        </button>
                    </div>

                    <div className="original-pdf-container">
                        <iframe
                            src={pdfUrl}
                            className="original-pdf-frame"
                            title="Orijinal PDF"
                        />
                    </div>
                </div>
            ) : (
                <p className="original-error-message">PDF not found.</p>
            )}
        </div>
    );
}

export default OriginalArticlePage;