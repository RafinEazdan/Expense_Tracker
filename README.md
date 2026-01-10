# Expense Tracker API (FastAPI + PostgreSQL)

A full-stack Expense Tracker application with a **FastAPI** backend and a modern frontend interface. Track your expenses, manage categories, and visualize your spending patterns.

## 🌐 Live Demo & Frontend

- **Live Application:** [https://expense-tracker-self-mu-50.vercel.app/](https://expense-tracker-self-mu-50.vercel.app/)
- **Frontend Repository:** [https://github.com/RafinEazdan/Expense_Tracker_Frontend](https://github.com/RafinEazdan/Expense_Tracker_Frontend)

## Backend Features

This backend API provides:

- User registration and authentication
- JWT-based login (OAuth2 password flow)
- CRUD endpoints for expense reports (protected)
- User-specific expense data (per-user isolation)
- Interactive API docs via Swagger UI

### Recent Updates

- ✅ Frontend application deployed and live
- ✅ User-specific expense tracking implemented
- ✅ Complete authentication flow with JWT
- ✅ Full CRUD operations for expenses

### Roadmap (near-term)

- Add pagination / filtering to expense listings
- Improve validation and error responses
- Add expense categories management
- Implement export functionality (CSV/PDF)

---

## Tech Stack

- **FastAPI** (Python)
- **PostgreSQL** via **psycopg**
- **JWT** auth (`PyJWT`)
- **Password hashing** with `passlib[argon2]`
- **Pydantic** schemas

---

## Project Structure

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

## Setup

### 1) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

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

## Database

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

## Run the API

From the repository root:

```bash
fastapi dev ./app/main.py --port 5000
```

Alternative (uvicorn):

```bash
uvicorn app.main:app --reload --port 5000
```

Once running:

- Health check: `GET /`
- Swagger UI: `GET /docs`
- ReDoc: `GET /redoc`

---

## Authentication Flow

1) **Register** a user
2) **Login** to get a JWT token
3) Call protected endpoints with:

```http
Authorization: Bearer <token>
```

---

## API Endpoints

### Health

- `GET /` → `{ "message": "Website is UP!" }`

### Users

- `GET /users` — list users
- `POST /users` — create user

Request body (`POST /users`):

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

### Auth

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

### Expense Reports (Protected)

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

## Notes / Current Behavior

- Expense reports are **linked to authenticated users** via the `owner_id` column.
- The `/expenses` routes are protected and require a valid JWT.
- Users can only view, create, edit, and delete their own expenses.
- The frontend application provides a complete user interface for all API features.

---

## Development Tips

- If you change environment variables, restart the server.
- Use Swagger UI at `/docs` to try endpoints quickly.

---
