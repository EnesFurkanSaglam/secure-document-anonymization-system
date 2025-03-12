import React, { useState } from 'react';
import './ReuploadPage.css';

function ReuploadPage() {
    const [email, setEmail] = useState('');
    const [trackingCode, setTrackingCode] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !trackingCode || !pdfFile) {
            setMessage("Please fill in all fields and select a PDF file.");
            setMessageType('error');
            return;
        }

        const formData = new FormData();
        formData.append("email", email);
        formData.append("tracking_code", trackingCode);
        formData.append("pdf", pdfFile);

        try {
            const response = await fetch("http://127.0.0.1:5000/author/reupload-article", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                setMessage("Article reloaded successfully!");
                setMessageType('success');
            } else {
                setMessage("Upload failed: " + (result.error || "Unknown error"));
                setMessageType('error');
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("An error occurred during the request.");
            setMessageType('error');
        }
    };

    const handleFileChange = (e) => {
        setPdfFile(e.target.files[0]);
    };

    return (
        <div className="rup-container">
            <h2 className="rup-title">Article Reupload</h2>

            <form className="rup-form" onSubmit={handleSubmit}>
                <div className="rup-input-group">
                    <label className="rup-label">Email:</label>
                    <input
                        className="rup-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                    />
                </div>

                <div className="rup-input-group">
                    <label className="rup-label">Tracking Code:</label>
                    <input
                        className="rup-input"
                        type="text"
                        value={trackingCode}
                        onChange={(e) => setTrackingCode(e.target.value)}
                        placeholder="Enter tracking code"
                        required
                    />
                </div>

                <div className="rup-input-group">
                    <label className="rup-label">PDF File:</label>
                    <input
                        className="rup-file-input"
                        type="file"
                        accept="application/pdf"
                        onChange={handleFileChange}
                        required
                    />
                </div>

                <button className="rup-submit-button" type="submit">
                    Reupload
                </button>
            </form>

            {message && (
                <p className={`rup-message ${messageType === 'success' ? 'rup-success' : 'rup-error'}`}>
                    {message}
                </p>
            )}
        </div>
    );
}

export default ReuploadPage;