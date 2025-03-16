import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import HomePage from './pages/Home/HomePage';
import AuthorPage from './pages/Author/AuthorPage';
import UploadPage from './pages/Upload/UploadPage';
import ReuploadPage from './pages/Reupload/ReuploadPage';
import CheckStatusPage from './pages/CheckStatus/CheckStatusPage';
import AuthorMessagingPage from './pages/AuthorMessaging/AuthorMessagingPage';
import ReviewerPage from './pages/Reviwer/ReviewerPage';
import EditorPage from './pages/Editor/EditorPage';
import ArticlePage from './pages/Article/ArticlePage';
import OriginalArticlePage from './pages/OriginalArticle/OriginalArticlePage';
import AnonymArticlePage from './pages/AnonymArticle/AnonymArticlePage';
import EditorMessagingPage from './pages/EditorMessaging/EditorMessagingPage';
import ReviwerByEmailPage from './pages/ReviwerByEmail/ReviwerByEmailPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reviewer" element={<ReviewerPage />} />
        <Route path="/editor" element={<EditorPage />} />
        <Route path="/articles/:articleId" element={<ArticlePage />} />
        <Route path="/original" element={<OriginalArticlePage />} />
        <Route path="/anonym" element={<AnonymArticlePage />} />
        <Route path="/author" element={<AuthorPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/reupload" element={<ReuploadPage />} />
        <Route path="/check-status" element={<CheckStatusPage />} />
        <Route path="/messaging" element={<AuthorMessagingPage />} />
        <Route path="/editor-messaging" element={<EditorMessagingPage />} />
        <Route path="/reviewer/:email" element={<ReviwerByEmailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
