import React, { useState, useEffect, useRef } from "react";
import "./ChatPage.css";

function ChatPage({ role, email, trackingCode, baseUrl = "" }) {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [sending, setSending] = useState(false);
    const messagesEndRef = useRef(null);
    const pollingIntervalRef = useRef(null);

    const POLLING_INTERVAL = 3000;

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (!trackingCode) return;

        loadMessages();

        pollingIntervalRef.current = setInterval(() => {
            if (!sending) {
                loadMessages(true);
            }
        }, POLLING_INTERVAL);

        return () => {
            if (pollingIntervalRef.current) {
                clearInterval(pollingIntervalRef.current);
            }
        };
    }, [trackingCode, sending]);

    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    };

    const loadMessages = async (silent = false) => {
        try {
            if (!silent) {
                setLoading(true);
            }

            let url = "";
            if (role === "author") {
                url = `${baseUrl}/author/messages?email=${email}&tracking_code=${trackingCode}`;
            } else if (role === "editor") {
                url = `${baseUrl}/editor/messages?tracking_code=${trackingCode}`;
            }

            const res = await fetch(url);
            const data = await res.json();

            if (res.ok) {
                if (JSON.stringify(data.conversation) !== JSON.stringify(messages)) {
                    setMessages(data.conversation || []);
                }
                setError(null);
            } else {
                if (!silent) {
                    setError("Your information could not be verified. Please try again.");
                }
            }
        } catch (err) {
            if (!silent) {
                setError("An error occurred while connecting to the server. Please try again.");
            }
        } finally {
            if (!silent) {
                setLoading(false);
            }
        }
    };

    const handleSendMessage = async () => {
        if (!newMessage.trim()) return;

        try {
            setSending(true);
            let url = "";
            let bodyObj = {};
            if (role === "author") {
                url = `${baseUrl}/author/send-message`;
                bodyObj = {
                    email: email,
                    tracking_code: trackingCode,
                    content: newMessage
                };
            } else if (role === "editor") {
                url = `${baseUrl}/editor/messages`;
                bodyObj = {
                    tracking_code: trackingCode,
                    content: newMessage
                };
            }

            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(bodyObj)
            });

            if (res.ok) {
                setNewMessage("");
                await loadMessages(true);

                const optimisticMsg = {
                    message_id: Date.now(),
                    sender_id: role === "editor" ? "1" : email,
                    receiver_id: role === "editor" ? email : "1",
                    content: newMessage,
                    timestamp: new Date().toISOString()
                };

                const messageExists = messages.some(
                    msg => msg.content === newMessage &&
                        msg.sender_id === optimisticMsg.sender_id
                );

                if (!messageExists) {
                    setMessages(prev => [...prev, optimisticMsg]);
                }
            } else {
                setError("There was an error sending the message. Please try again.");
            }
        } catch (err) {
            setError("An error occurred while connecting to the server. Please try again.");
        } finally {
            setSending(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const isEditorMessage = (msg) => {
        return msg.sender_id === "1" || msg.sender_id === 1;
    };

    const isOwnMessage = (msg) => {
        if (role === "editor") {
            return isEditorMessage(msg);
        } else {
            return !isEditorMessage(msg);
        }
    };

    const isPolling = true;

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h3>{role === "author" ? "Author Messaging" : "Editor Messaging"}</h3>
                {isPolling && <div className="chat-sync-indicator"></div>}
            </div>

            {error && <div className="chat-error">{error}</div>}

            <div className="messages-container">
                {loading && messages.length === 0 ? (
                    <div className="chat-loading">Loading messages...</div>
                ) : messages.length > 0 ? (
                    <>
                        {messages.map((msg) => (
                            <div
                                key={msg.message_id}
                                className={`message ${isOwnMessage(msg) ? "message-sent" : "message-received"
                                    } ${isEditorMessage(msg) ? "editor-message" : "author-message"}`}
                            >
                                <div className="message-content">{msg.content}</div>
                                <div className="message-time">
                                    {new Date(msg.timestamp || Date.now()).toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit"
                                    })}
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </>
                ) : (
                    <div className="no-messages">There are no messages yet.</div>
                )}
            </div>

            <div className="message-input-container">
                <textarea
                    className="message-input"
                    placeholder="Write your message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={sending}
                />
                <button
                    className="send-button"
                    onClick={handleSendMessage}
                    disabled={sending || !newMessage.trim()}
                >
                    {sending ? "..." : "Send"}
                </button>
            </div>
        </div>
    );
}

export default ChatPage;
