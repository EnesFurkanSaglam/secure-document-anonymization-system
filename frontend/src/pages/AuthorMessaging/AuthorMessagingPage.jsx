import React, { useState } from "react";
import ChatPage from "../Chat/ChatPage";
import "./AuthorMessagingPage.css";

function AuthorMessagingPage() {
    const [email, setEmail] = useState("");
    const [trackingCode, setTrackingCode] = useState("");
    const [showChat, setShowChat] = useState(false);
    const [formError, setFormError] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        setFormError("");

        if (!email.trim()) {
            setFormError("Lütfen email adresinizi girin.");
            return;
        }

        if (!trackingCode.trim()) {
            setFormError("Lütfen takip kodunuzu girin.");
            return;
        }

        setShowChat(true);
    };

    return (
        <div className="author-page-container">
            {!showChat ? (
                <div className="login-container">
                    <h2>Yazar Mesajlaşma Sistemi</h2>
                    <p className="login-subtitle">
                        Editörünüzle mesajlaşmak için lütfen bilgilerinizi girin.
                    </p>

                    {formError && <div className="form-error">{formError}</div>}

                    <form onSubmit={handleSubmit} className="login-form">
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Email adresiniz"
                                className="form-input"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="trackingCode">Takip Kodu</label>
                            <input
                                id="trackingCode"
                                type="text"
                                value={trackingCode}
                                onChange={(e) => setTrackingCode(e.target.value)}
                                placeholder="Takip kodunuz"
                                className="form-input"
                            />
                        </div>

                        <button type="submit" className="login-button">
                            Mesajları Görüntüle
                        </button>
                    </form>
                </div>
            ) : (
                <div className="chat-page-wrapper">
                    <ChatPage
                        role="author"
                        email={email}
                        trackingCode={trackingCode}
                        baseUrl="http://localhost:5000"
                    />
                    <button onClick={() => setShowChat(false)} className="back-button">
                        Giriş Ekranına Dön
                    </button>
                </div>
            )}
        </div>
    );
}

export default AuthorMessagingPage;