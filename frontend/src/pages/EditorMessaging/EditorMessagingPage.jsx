import React from "react";
import ChatPage from "../Chat/ChatPage";
import { useLocation } from "react-router-dom";

function EditorMessagingPage() {
    const location = useLocation();
    const { trackingCode } = location.state || {};

    return (
        <div>
            <h1></h1>

            <ChatPage
                role="editor"
                trackingCode={trackingCode}
                baseUrl="http://localhost:5000"
            />
        </div>
    );
}

export default EditorMessagingPage;
