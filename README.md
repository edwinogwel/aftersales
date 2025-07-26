# ⚡ E-Bike Aftersales Service 

A FastAPI-based backend for managing aftersales service operation at Roam, including:

- Service Jobs
- Service Requests
- Warranty tracking
- Support ticketing
- Admin-ready API architecture

## 🚀 Features

- ✅ JWT Authentication (Register/Login)
- 🛠️ Create & Track Service Requests
- 🧾 Warranty Info Storage
- 🔐 Secure API Routes with OAuth2
- 🗂️ Modular Structure (routes, schemas, db)
- 🌱 Easily extendable to include: support tickets, maintenance logs, email alerts

## 🏗️ Project Structure

```
aftersales/
├── app/
│ ├── routers/
│ │ ├── job_card.py
│ │ ├── parts.py
│ │ ├── service_job.py
│ │ ├── service_request.py
│ │ ├── etc.
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ └── schemas.py
├── main.py
├── README.md
└── requirements.txt
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/aftersales.git
cd aftersales
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the Database
```bash
# For SQLite
sqlite3 app/db/aftersale.db
```

## 5. Run the Server
```bash
uvicorn app:main:app --reload
```

## 🛠️ Future Improvements

- Support ticket system
- Role-based access (admin, support, customer)
- Email notifications for service status
- Scheduled maintenance logs
- Frontend (Next.js + RippleUI)

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.