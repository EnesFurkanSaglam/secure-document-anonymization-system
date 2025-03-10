import React, { useState } from 'react';
import './UploadPage.css'; // Import the CSS file

function UploadPage() {
    const [email, setEmail] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'
    const [trackingCode, setTrackingCode] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !pdfFile) {
            setMessage('Please provide your email and select a PDF file.');
            setMessageType('error');
            return;
        }

        const formData = new FormData();
        formData.append('email', email);
        formData.append('pdf', pdfFile);

        try {
            const response = await fetch('http://127.0.0.1:5000/author/upload-article', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                setMessage('Article uploaded successfully! Your tracking code:');
                setTrackingCode(data.tracking_code);
                setMessageType('success');
            } else {
                setMessage(data.error || 'An error occurred.');
                setMessageType('error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            setMessage('An error occurred while uploading the file.');
            setMessageType('error');
        }
    };

    return (
        <div className="upl-container">
            <h1 className="upl-title">Upload Article</h1>

            <form className="upl-form" onSubmit={handleSubmit}>
                <div className="upl-input-group">
                    <label className="upl-label" htmlFor="email">Email:</label>
                    <input
                        className="upl-input"
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                    />
                </div>

                <div className="upl-input-group">
                    <label className="upl-label" htmlFor="pdf">PDF File:</label>
                    <input
                        className="upl-file-input"
                        type="file"
                        id="pdf"
                        accept="application/pdf"
                        onChange={(e) => setPdfFile(e.target.files[0])}
                        required
                    />
                </div>

                <button className="upl-submit-button" type="submit">
                    Upload
                </button>
            </form>

            {message && (
                <div className={`upl-message ${messageType === 'success' ? 'upl-success' : 'upl-error'}`}>
                    {message}
                    {trackingCode && <span className="upl-tracking-code">{trackingCode}</span>}
                </div>
            )}
        </div>
    );
}

export default UploadPage;