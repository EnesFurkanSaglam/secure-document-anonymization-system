import React, { useState } from 'react';
import './CheckStatusPage.css';

function CheckStatusPage() {
    const [email, setEmail] = useState('');
    const [trackingCode, setTrackingCode] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const isEmailValid = (email) => {
        return email.includes('@');
    };

    const handleCheckStatus = async () => {
        if (!email || !trackingCode) {
            setError("Email and tracking code are required.");
            return;
        }

        if (!isEmailValid(email)) {
            setError("Please enter a valid email address.");
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch(
                `http://127.0.0.1:5000/author/check-status?email=${encodeURIComponent(email)}&tracking_code=${encodeURIComponent(trackingCode)}`
            );
            const data = await response.json();

            if (!response.ok) {
                setError(data.error || "An error occurred.");
            } else {
                setResult(data);
            }
        } catch (err) {
            setError("An error occurred: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const getFileName = (path) => {
        return path.split(/[\/\\]/).pop();
    };

    return (
        <div className="csp-container">
            <h2 className="csp-title">Check Article Status</h2>

            <div className="csp-form">
                <div className="csp-input-group">
                    <label className="csp-label">Email:</label>
                    <input
                        className="csp-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                    />
                </div>

                <div className="csp-input-group">
                    <label className="csp-label">Tracking Code:</label>
                    <input
                        className="csp-input"
                        type="text"
                        value={trackingCode}
                        onChange={(e) => setTrackingCode(e.target.value)}
                        placeholder="Enter tracking code"
                    />
                </div>

                <button
                    className="csp-button"
                    onClick={handleCheckStatus}
                    disabled={loading || !isEmailValid(email)}
                >
                    {loading ? "Checking..." : "Check Status"}
                </button>
            </div>

            {error && (
                <div className="csp-error">
                    {error}
                </div>
            )}

            {result && (
                <div className="csp-result">
                    <p className="csp-result-item">
                        <strong>Tracking Code:</strong> {result.tracking_code}
                    </p>
                    <p className="csp-result-item">
                        <strong>Status:</strong> {result.status}
                    </p>
                    <p className="csp-result-item">
                        <strong>Message:</strong> {result.message}
                    </p>

                    {result.path && result.status === "reviewed_and_send_back" && (
                        <div className="csp-pdf">
                            <iframe
                                src={`http://127.0.0.1:5000/pdf/rewiev/${getFileName(result.path)}`}
                                title="Review PDF"
                                frameBorder="0"
                                width="100%"
                                height="600px"
                            ></iframe>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default CheckStatusPage;
