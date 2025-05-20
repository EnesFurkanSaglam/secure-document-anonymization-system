# 🛡️ Güvenli Belge Anonimleştirme Sistemi

## 📄 Genel Bakış

Bu proje, **akademik makalelerin güvenli ve anonim bir şekilde işlenmesini** ve değerlendirilmesini sağlayan tam kapsamlı bir sistemdir. Sistem iki ana bileşenden oluşur:

- 🔙 **Backend:** Flask tabanlı RESTful API, belge şifreleme, anonimleştirme, değerlendirme ve kullanıcı yönetimi.
- 🎨 **Frontend:** React tabanlı kullanıcı dostu arayüz ile PDF görüntüleme ve anonimleştirme etkileşimi.

Bu yapı, akademik dergiler ve konferanslar için çift kör hakemli (double-blind) değerlendirme süreçlerinde kullanılmak üzere geliştirilmiştir.

## 🧱 Klasör Yapısı

```
secure-document-anonymization-system/
├── backend/      # Flask API ve veri işleme servisleri
├── frontend/     # React arayüz ve kullanıcı etkileşimi
└── README.md     # Genel proje açıklaması (bu dosya)
```

> 📌 Daha fazla bilgi için:
> - Backend detayları için: [`/backend/README.md`](./backend/README.md)
> - Frontend detayları için: [`/frontend/README.md`](./frontend/README.md)

## ⚙️ Kullanılan Temel Teknolojiler

| Katman    | Teknolojiler                                                                 |
|-----------|-------------------------------------------------------------------------------|
| Backend   | Flask, SQLAlchemy, PyPDF2, Cryptography, JWT, Flask-CORS                    |
| Frontend  | React 19, Vite 6, React Router, React PDF Viewer, Lucide Icons              |
| Ortak     | RESTful API, AES şifreleme, Rol Tabanlı Erişim, JWT tabanlı kimlik doğrulama |

## 🚀 Hızlı Başlangıç

### Backend için
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context(): db.create_all()
python app.py
```

### Frontend için
```bash
cd frontend
npm install  # veya yarn install
npm run dev  # veya yarn dev
```

Uygulama tarayıcınızda `http://localhost:5173` üzerinde çalışır.

## 🧩 Sistem Özeti

- 👨‍💻 **Yazar:** Makale yükleme, revizyon gönderme
- 🧑‍⚖️ **Editör:** Hakem atama, değerlendirme yönetimi
- 🧑‍🔬 **Hakem:** Anonim belge inceleme ve değerlendirme
- 🔐 **Güvenlik:** AES-256 şifreleme, JWT, IP kısıtlamaları, loglama
- 📑 **PDF İşleme:** Metadata temizleme, anonimleştirme, revizyon desteği

---


# 🛡️ Secure Document Anonymization System

## 📄 Overview

This project is a **comprehensive system for securely and anonymously processing and evaluating academic papers**. The system consists of two main components:

- 🔙 **Backend:** Flask-based RESTful API for document encryption, anonymization, evaluation, and user management.
- 🎨 **Frontend:** User-friendly React interface for PDF viewing and anonymization interaction.

This structure is designed for use in double-blind peer review processes for academic journals and conferences.

## 🧱 Folder Structure

```
secure-document-anonymization-system/
├── backend/      # Flask API and data processing services
├── frontend/     # React interface and user interaction
└── README.md     # General project description (this file)
```

> 📌 For more information:
> - For backend details: [`/backend/README.md`](./backend/README.md)
> - For frontend details: [`/frontend/README.md`](./frontend/README.md)

## ⚙️ Core Technologies Used

| Layer     | Technologies                                                                |
|-----------|-------------------------------------------------------------------------------|
| Backend   | Flask, SQLAlchemy, PyPDF2, Cryptography, JWT, Flask-CORS                    |
| Frontend  | React 19, Vite 6, React Router, React PDF Viewer, Lucide Icons              |
| Common    | RESTful API, AES encryption, Role-Based Access, JWT-based authentication    |

## 🚀 Quick Start

### For Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context(): db.create_all()
python app.py
```

### For Frontend
```bash
cd frontend
npm install  # or yarn install
npm run dev  # or yarn dev
```

The application runs at `http://localhost:5173` in your browser.

## 🧩 System Summary

- 👨‍💻 **Author:** Upload paper, submit revision
- 🧑‍⚖️ **Editor:** Assign reviewers, manage evaluations
- 🧑‍🔬 **Reviewer:** Review and evaluate anonymized documents
- 🔐 **Security:** AES-256 encryption, JWT, IP restrictions, logging
- 📑 **PDF Processing:** Metadata cleaning, anonymization, revision support

--- 

