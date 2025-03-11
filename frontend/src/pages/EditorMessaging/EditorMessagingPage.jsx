import React from "react";
import ChatPage from "../Chat/ChatPage";

function EditorMessagingPage() {
    const articleTrackingCode = "ABC123";

    return (
        <div>
            <h2>Editor Chat Page</h2>
            <ChatPage
                role="editor"
                trackingCode={articleTrackingCode}
                baseUrl="http://localhost:5000"
            />
        </div>
    );
}

export default EditorMessagingPage;
