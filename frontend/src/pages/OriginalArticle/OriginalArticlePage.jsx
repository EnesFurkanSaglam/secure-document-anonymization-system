import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './OriginalArticlePage.css';

function OriginalArticlePage() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const fileName = queryParams.get('file');
    const pdfUrl = fileName ? `http://127.0.0.1:5000/pdf/${fileName}` : null;
    const articleId = location.state?.articleId;

    const [anonymizeNames, setAnonymizeNames] = useState(false);
    const [anonymizePhotos, setAnonymizePhotos] = useState(false);

    const handleAnonymize = async () => {
        console.log("Anonymize clicked");
        try {
            const response = await fetch("http://127.0.0.1:5000/editor/anonymize-article", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    article_id: articleId,
                    anonymize_names: anonymizeNames,
                    anonymize_photos: anonymizePhotos
                })
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            console.log("Success:", data);
            alert("Success");
        } catch (error) {
            console.error("Error in anonymization:", error);
            alert("An error occurred");
        }
    };

    return (
        <div className="original-container">
            <h1 className="original-title">Original PDF</h1>
            {pdfUrl ? (
                <div className="original-content">
                    <div className="original-sidebar">
                        <div className="original-checkbox-group">
                            <label className="original-checkbox-label">
                                <input
                                    type="checkbox"
                                    className="original-checkbox"
                                    checked={anonymizeNames}
                                    onChange={() => setAnonymizeNames(!anonymizeNames)}
                                />
                                <span className="original-checkbox-text">Author Names Organization and Email</span>
                            </label>
                            <label className="original-checkbox-label">
                                <input
                                    type="checkbox"
                                    className="original-checkbox"
                                    checked={anonymizePhotos}
                                    onChange={() => setAnonymizePhotos(!anonymizePhotos)}
                                />
                                <span className="original-checkbox-text">Author Photos</span>
                            </label>
                        </div>
                        <button
                            className="original-anonymize-button"
                            onClick={handleAnonymize}
                        >
                            Anonymize and Assign
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
