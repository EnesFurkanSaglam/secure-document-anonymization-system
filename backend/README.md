# Güvenli Belge Anonimleştirme Sistemi

## Proje Hakkında

Bu proje, akademik makalelerin güvenli bir şekilde anonimleştirilmesi ve yönetilmesi için geliştirilmiş bir backend sistemidir. Özellikle akademik dergiler ve konferanslar için tasarlanmış olup, makale değerlendirme sürecini güvenli ve etkili bir şekilde yönetmeyi amaçlamaktadır.

## Kullanılan Teknolojiler ve Nedenleri

### Backend Framework
- **Flask (2.3.3)**: 
  - Hafif ve esnek bir Python web framework'ü
  - Mikroservis mimarisine uygun
  - RESTful API geliştirmek için ideal
  - Kolay genişletilebilir yapı

### Veritabanı ve ORM
- **SQLAlchemy (2.0.20)**:
  - Güçlü ORM (Object-Relational Mapping) sistemi
  - Veritabanı işlemlerini Python nesneleri üzerinden yönetme
  - Veritabanı bağımsız kod yazabilme imkanı
- **Flask-SQLAlchemy (3.1.1)**:
  - Flask ile SQLAlchemy entegrasyonu
  - Veritabanı işlemlerini Flask uygulaması içinde kolay yönetme

### Güvenlik
- **cryptography (41.0.3)**:
  - Belgelerin şifrelenmesi için güçlü kriptografi kütüphanesi
  - Asimetrik ve simetrik şifreleme desteği
  - Güvenli anahtar yönetimi
- **python-dotenv (1.0.0)**:
  - Hassas bilgilerin (API anahtarları, şifreler) güvenli yönetimi
  - Ortam değişkenlerinin kolay yönetimi

### PDF İşleme
- **PyPDF2 (3.0.1)**:
  - PDF dosyalarını okuma ve yazma
  - PDF belgelerinin anonimleştirilmesi
  - PDF metadata yönetimi

### API ve CORS
- **Flask-Cors (4.0.0)**:
  - Cross-Origin Resource Sharing (CORS) desteği
  - Frontend uygulamalarıyla güvenli iletişim
  - API güvenliği

## Sistem Mimarisi

### 1. Rol Tabanlı Erişim Kontrolü
- **Yazar (Author)**
  - Makale gönderimi
  - Makale güncelleme
  - Makale durumu takibi
  - Hakem değerlendirmelerini görüntüleme

- **Editör (Editor)**
  - Makale değerlendirme sürecini yönetme
  - Hakem atama
  - Makale durumunu güncelleme
  - Yayın kararı verme

- **Hakem (Reviewer)**
  - Makale değerlendirme
  - Değerlendirme raporu oluşturma
  - Anonimleştirilmiş makalelere erişim

### 2. Belge İşleme Süreci
1. **Yükleme ve Şifreleme**
   - PDF belgelerin güvenli yüklenmesi
   - Otomatik şifreleme
   - Metadata temizleme

2. **Anonimleştirme**
   - Yazar bilgilerinin kaldırılması
   - Referansların anonimleştirilmesi
   - Metadata temizleme

3. **Değerlendirme**
   - Hakemlere anonimleştirilmiş belgelerin dağıtımı
   - Değerlendirme raporlarının güvenli saklanması

4. **Yayınlama**
   - Onaylanan makalelerin yayınlanması
   - Final versiyonların arşivlenmesi

## Güvenlik Özellikleri

1. **Veri Şifreleme**
   - Tüm belgeler AES-256 şifreleme ile saklanır
   - Hassas veriler için asimetrik şifreleme
   - Güvenli anahtar yönetimi

2. **Erişim Kontrolü**
   - JWT tabanlı kimlik doğrulama
   - Rol tabanlı yetkilendirme
   - IP bazlı erişim kısıtlamaları

3. **Veri Bütünlüğü**
   - Dosya hash kontrolü
   - İmza doğrulama
   - Audit logging

## Kurulum ve Çalıştırma

### Sistem Gereksinimleri
- Python 3.8+
- SQLite3
- 2GB RAM minimum
- 10GB disk alanı

### Kurulum Adımları

1. Projeyi klonlayın:
```bash
git clone [proje-url]
cd secure-document-anonymization-system/backend
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate     
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Ortam değişkenlerini ayarlayın:
```bash
cp .env.example .env

```

5. Veritabanını başlatın:
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

6. Uygulamayı başlatın:
```bash
python app.py
```

## API Dokümantasyonu

### Yazar API'leri
- `POST /author/submit`
  - Yeni makale gönderimi
  - PDF dosyası ve metadata
  - Otomatik anonimleştirme

- `GET /author/papers`
  - Yazarın tüm makalelerini listeleme
  - Durum ve değerlendirme bilgileri

- `PUT /author/papers/<id>`
  - Makale güncelleme
  - Revizyon yükleme

### Editör API'leri
- `GET /editor/papers`
  - Tüm makaleleri listeleme
  - Filtreleme ve sıralama

- `PUT /editor/papers/<id>/assign`
  - Hakem atama
  - Değerlendirme süresi belirleme

- `PUT /editor/papers/<id>/status`
  - Makale durumunu güncelleme
  - Yayın kararı verme

### Hakem API'leri
- `GET /reviewer/papers`
  - Atanan makaleleri listeleme
  - Değerlendirme durumu

- `POST /reviewer/papers/<id>/review`
  - Değerlendirme raporu gönderme
  - Puanlama ve yorumlar

## Hata Ayıklama ve Loglama

- Detaylı hata logları
- Performans metrikleri
- Güvenlik olayları izleme
- Kullanıcı aktivite logları



# Secure Document Anonymization System

## About the Project

This project is a backend system developed for secure anonymization and management of academic papers. It is specifically designed for academic journals and conferences, aiming to manage the paper review process securely and effectively.

## Technologies Used and Their Purposes

### Backend Framework
- **Flask (2.3.3)**: 
  - Lightweight and flexible Python web framework
  - Suitable for microservice architecture
  - Ideal for developing RESTful APIs
  - Easily extensible structure

### Database and ORM
- **SQLAlchemy (2.0.20)**:
  - Powerful ORM (Object-Relational Mapping) system
  - Database operations through Python objects
  - Database-independent code capability
- **Flask-SQLAlchemy (3.1.1)**:
  - Flask integration with SQLAlchemy
  - Easy database management within Flask application

### Security
- **cryptography (41.0.3)**:
  - Strong cryptography library for document encryption
  - Support for asymmetric and symmetric encryption
  - Secure key management
- **python-dotenv (1.0.0)**:
  - Secure management of sensitive information (API keys, passwords)
  - Easy management of environment variables

### PDF Processing
- **PyPDF2 (3.0.1)**:
  - Reading and writing PDF files
  - Anonymization of PDF documents
  - PDF metadata management

### API and CORS
- **Flask-Cors (4.0.0)**:
  - Cross-Origin Resource Sharing (CORS) support
  - Secure communication with frontend applications
  - API security

## System Architecture

### 1. Role-Based Access Control
- **Author**
  - Paper submission
  - Paper updates
  - Paper status tracking
  - Viewing reviewer evaluations

- **Editor**
  - Managing paper review process
  - Assigning reviewers
  - Updating paper status
  - Making publication decisions

- **Reviewer**
  - Paper evaluation
  - Creating evaluation reports
  - Access to anonymized papers

### 2. Document Processing Workflow
1. **Upload and Encryption**
   - Secure upload of PDF documents
   - Automatic encryption
   - Metadata cleaning

2. **Anonymization**
   - Removal of author information
   - Anonymization of references
   - Metadata cleaning

3. **Evaluation**
   - Distribution of anonymized documents to reviewers
   - Secure storage of evaluation reports

4. **Publication**
   - Publication of approved papers
   - Archiving of final versions

## Security Features

1. **Data Encryption**
   - All documents stored with AES-256 encryption
   - Asymmetric encryption for sensitive data
   - Secure key management

2. **Access Control**
   - JWT-based authentication
   - Role-based authorization
   - IP-based access restrictions

3. **Data Integrity**
   - File hash verification
   - Signature verification
   - Audit logging

## Installation and Running

### System Requirements
- Python 3.8+
- SQLite3
- 2GB RAM minimum
- 10GB disk space

### Installation Steps

1. Clone the project:
```bash
git clone [project-url]
cd secure-document-anonymization-system/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
venv\Scripts\activate     
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env

```

5. Initialize database:
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

6. Start the application:
```bash
python app.py
```

## API Documentation

### Author APIs
- `POST /author/submit`
  - New paper submission
  - PDF file and metadata
  - Automatic anonymization

- `GET /author/papers`
  - List all papers by author
  - Status and evaluation information

- `PUT /author/papers/<id>`
  - Update paper
  - Upload revision

### Editor APIs
- `GET /editor/papers`
  - List all papers
  - Filtering and sorting

- `PUT /editor/papers/<id>/assign`
  - Assign reviewers
  - Set evaluation period

- `PUT /editor/papers/<id>/status`
  - Update paper status
  - Make publication decision

### Reviewer APIs
- `GET /reviewer/papers`
  - List assigned papers
  - Evaluation status

- `POST /reviewer/papers/<id>/review`
  - Submit evaluation report
  - Scoring and comments

## Debugging and Logging

- Detailed error logs
- Performance metrics
- Security event monitoring
- User activity logs

