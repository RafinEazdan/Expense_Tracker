# 💰 Expense Tracker API

<div align="center">

**A full-stack Expense Tracker application with a FastAPI backend and modern frontend interface**

Track your expenses • Manage categories • Visualize spending patterns

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 🚀 Live Deployment

### 🌐 Published Website
- **Frontend (Live Application):** [https://expense-tracker-self-mu-50.vercel.app/](https://expense-tracker-self-mu-50.vercel.app/)
- **Backend API (Hosted on Render):** [https://expense-tracker-r3tn.onrender.com](https://expense-tracker-r3tn.onrender.com)
- **API Documentation:** [https://expense-tracker-r3tn.onrender.com/docs](https://expense-tracker-r3tn.onrender.com/docs)

### 📦 Repositories
- **Frontend Repository:** [https://github.com/RafinEazdan/Expense_Tracker_Frontend](https://github.com/RafinEazdan/Expense_Tracker_Frontend)
- **Backend Repository:** _(Current Repository)_

---

## ✨ Backend Features

This backend API provides:

- 🔐 User registration and authentication
- 🎫 JWT-based login (OAuth2 password flow)
- 📝 CRUD endpoints for expense reports (protected)
- 👤 User-specific expense data (per-user isolation)
- 📚 Interactive API docs via Swagger UI
- 🌐 Production deployment on Render

### 🎉 Recent Updates

- ✅ **Backend deployed to production on Render**
- ✅ Frontend application deployed and live on Vercel
- ✅ Docker image updated on DockerHub (`eazdanrafin/expense_tracker:latest`)
- ✅ User-specific expense tracking implemented
- ✅ Complete authentication flow with JWT
- ✅ Full CRUD operations for expenses
---

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database via **psycopg**
- **JWT** - Secure authentication using `PyJWT`
- **Alembic** - Database Migration Tool
- **Argon2** - Password hashing with `passlib[argon2]`
- **Pydantic** - Data validation using Python type annotations
- **Render** - Cloud hosting platform for backend deployment

---

## 📁 Project Structure

```text
.
├── requirements.txt
├── .env
└── app/
    ├── main.py
    ├── database.py
    ├── oauth.py
    ├── schemas.py
    ├── utils.py
    └── routers/
        ├── auth.py
        ├── users.py
        └── reports.py
```

---

## 🚀 Setup

### 1️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

This project loads configuration from `.env`.

**Important:** do not commit real secrets (database passwords, JWT secret keys). Your repo currently contains a `.env`; consider rotating those credentials and adding `.env` to `.gitignore` if it isn’t already.

Create/adjust `.env` with values like:

```dotenv
# Postgres
USER_DB=postgres
PASSWORD=YOUR_PASSWORD
HOST_DB=localhost
DB_NAME=expense_db
DB_PORT=5432

# JWT
SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1000
```

Notes:
- `ALGORITHM` is typically `HS256`.
- `ACCESS_TOKEN_EXPIRE_MINUTES` must be a number.

---

## 🗄️ Database

The API expects a PostgreSQL database with `users` and `expenses` tables.

If you don’t already have tables created, here is a minimal schema that matches the current code:

```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS expenses (
  id SERIAL PRIMARY KEY,
  amount DOUBLE PRECISION NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## ▶️ Run the API

From the repository root:

```bash
fastapi dev ./app/main.py --port 5000
```

Alternative (uvicorn):

```bash
uvicorn app.main:app --reload --port 5000
```

Once running:

- ❤️ Health check: `GET /`
- 📖 Swagger UI: `GET /docs`
- 📘 ReDoc: `GET /redoc`

> **💡 Tip:** You can also test the live API at [https://expense-tracker-r3tn.onrender.com/docs](https://expense-tracker-r3tn.onrender.com/docs)

---

## 🐳 Run with Docker

### Option A: Run the published DockerHub image

The backend image is published/updated on DockerHub as:

- `eazdanrafin/expense_tracker:latest`
- DockerHub: https://hub.docker.com/repository/docker/eazdanrafin/expense_tracker/

Run it (expects a `.env` file in the current directory):

```bash
docker run -p 8000:8000 --env-file .env eazdanrafin/expense_tracker:latest
```

Note: this runs **only the API container**. Your `.env` must point to a reachable Postgres instance (e.g., a managed DB, or a local DB).

### Option B: Run API + Postgres with Docker Compose

This repo includes `docker-compose.yml` to start both the API and a Postgres container:

```bash
docker compose up --build
```

If you use compose, set `HOST_DB=postgres` in `.env` (so the API container can reach the Postgres service).

---

## 🔐 Authentication Flow

1) **Register** a user
2) **Login** to get a JWT token
3) Call protected endpoints with:

```http
Authorization: Bearer <token>
```

---

## 📍 API Endpoints

### 💚 Health

- `GET /` → `{ "message": "Website is UP!" }`

### 👥 Users

- `GET /users` — list users
- `POST /users` — create user

Request body (`POST /users`):

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

### 🔑 Auth

- `POST /login` — obtain JWT token

This endpoint uses `OAuth2PasswordRequestForm`, so it expects **form-encoded** fields:

- `username` (your email)
- `password`

Example:

```bash
curl -X POST "http://localhost:5000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=your-password"
```

Response:

```json
{
  "token": "<jwt>",
  "token_type": "bearer"
}
```

### 💸 Expense Reports (Protected)

All endpoints below require a valid `Authorization: Bearer ...` header.

- `GET /expenses` — list expense reports
- `POST /expenses` — create expense report
- `GET /expenses/{id}` — get one expense report
- `PUT /expenses/{id}` — update an expense report
- `DELETE /expenses/{id}` — delete an expense report

Example create request:

```bash
curl -X POST "http://localhost:5000/expenses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 12.5,
    "category": "Food",
    "description": "Lunch"
  }'
```

---

## 📝 Notes / Current Behavior

- 🔒 Expense reports are **linked to authenticated users** via the `owner_id` column.
- 🛡️ The `/expenses` routes are protected and require a valid JWT.
- 👤 Users can only view, create, edit, and delete their own expenses.
- 🎨 The frontend application provides a complete user interface for all API features.
- 🌐 Both frontend and backend are deployed and accessible online.

---

## 💻 Development Tips

- 🔄 If you change environment variables, restart the server.
- 🧪 Use Swagger UI at `/docs` to try endpoints quickly.
- 🌍 Test the production API at: [https://expense-tracker-r3tn.onrender.com/docs](https://expense-tracker-r3tn.onrender.com/docs)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Eazdan Mostafa Rafin**

Feel free to reach out for any questions or contributions!

---

<div align="center">

Made with ❤️ using FastAPI and PostgreSQL

**[⬆ Back to Top](#-expense-tracker-api)**

</div>
