import React, { useState } from 'react';
import './CheckStatusPage.css'; // Import the CSS file

function CheckStatusPage() {
    const [email, setEmail] = useState('');
    const [trackingCode, setTrackingCode] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCheckStatus = async () => {
        if (!email || !trackingCode) {
            setError("Email and tracking code are required.");
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
                    disabled={loading}
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
                </div>
            )}
        </div>
    );
}

export default CheckStatusPage;