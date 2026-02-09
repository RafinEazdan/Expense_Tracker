# 💰 Expense Tracker API

<div align="center">

**Expense tracker backend API built with FastAPI + Postgres**

Auth • Per-user expense CRUD • Optional LLM-assisted insights and entry

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 🚀 Live Deployment

- **Frontend (Vercel):** https://expense-tracker-self-mu-50.vercel.app/
- **Backend API (Render):** https://expense-tracker-r3tn.onrender.com
- **API Docs:** https://expense-tracker-r3tn.onrender.com/docs

### 📦 Repositories

- **Frontend Repository:** https://github.com/RafinEazdan/Expense_Tracker_Frontend
- **Backend Repository:** (this repository)

---

## ✨ Features

- 🔐 User registration + JWT login (OAuth2 password flow)
- 🧾 Expense CRUD (scoped to the logged-in user)
- 📚 Interactive API docs via Swagger UI
- 🤖 Optional LLM endpoints:
  - Generate a short “spending story” analysis from your expense history
  - Convert natural language into an expense entry (amount/category/description)

---

## 🛠️ Tech Stack

- **FastAPI** / **Starlette**
- **PostgreSQL** via **psycopg**
- **SQLAlchemy + Alembic** for models/migrations
- **JWT** via **PyJWT**
- **Argon2** via **passlib[argon2]**
- **LangChain + Ollama** (optional, for LLM endpoints)

---

## 📁 Project Structure

```text
.
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── alembic/
├── requirements.txt
└── app/
    ├── main.py
    ├── database.py
    ├── models.py
    ├── oauth.py
    ├── schemas.py
    ├── utils.py
    ├── LLM/
    │   ├── autoSQL.py
    │   └── storyLLM.py
    └── routers/
        ├── auth.py
        ├── users.py
        ├── reports.py
        └── llm.py
```

---

## ⚙️ Environment Variables

This project reads configuration from a `.env` file. The repo ignores it (see `.gitignore`), so you should create your own locally.

Minimum required:

```dotenv
# Database (used by app/database.py and Alembic)
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_db

# JWT (used by app/oauth.py)
SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1000
```

Optional (only needed for LLM routes):

```dotenv
LLM_MODEL=llama3.1
```

### Docker Compose `.env` example

If you run with Docker Compose, the Postgres service also reads `.env`. A typical file looks like:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=expense_db

DATABASE_URL=postgresql://postgres:password@postgres:5432/expense_db

SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1000

# Optional
LLM_MODEL=llama3.1
```

---

## 🗄️ Database & Migrations

The app uses two main tables:

- `users`
- `expenses` (with `owner_id` → `users.id`)

In Docker Compose, migrations are applied automatically on container start via `alembic upgrade head`.

If you’re running locally (non-docker), run:

```bash
alembic upgrade head
```

---

## ▶️ Run Locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5000
```

Then open:

- `GET /` (health)
- `GET /docs` (Swagger UI)

---

## 🐳 Run with Docker

### Option A: API + Postgres (recommended)

```bash
docker compose up --build
```

API will be available at `http://localhost:8000`.

To wipe the database volume:

```bash
docker compose down -v
```

### Option B: Run the published DockerHub image

- Image: `eazdanrafin/expense_tracker:latest`

```bash
docker run -p 8000:8000 --env-file .env eazdanrafin/expense_tracker:latest
```

Note: this runs only the API container — you still need a reachable Postgres instance referenced by `DATABASE_URL`.

---

## 🔑 API Quickstart

### 1) Create a user

`POST /users`

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"secret"}'
```

### 2) Login

`POST /login` (OAuth2 password flow; uses form fields `username` + `password`)

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=me@example.com&password=secret"
```

Use the returned token as:

`Authorization: Bearer <token>`

### 3) Expenses (protected)

- `GET /expenses`
- `POST /expenses`
- `GET /expenses/{id}`
- `PUT /expenses/{id}`
- `DELETE /expenses/{id}`

Example create:

```bash
curl -X POST http://localhost:8000/expenses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":12.5,"category":"Food & Dining","description":"Lunch"}'
```

---

## 🤖 LLM Endpoints (optional)

These routes require:

- An Ollama server running locally/where the API can reach it
- `LLM_MODEL` set to a model that exists in your Ollama instance

Routes (protected):

- `GET /llm/analysis/story` — returns a short narrative analysis of the user’s expenses
- `POST /llm/sql-gen` — takes `{ "query": "..." }` and inserts a generated expense

Example:

```bash
curl -X POST http://localhost:8000/llm/sql-gen \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Spent 18.99 on groceries at Target"}'
```

---

## ✅ Notes

- The live API is available at https://expense-tracker-r3tn.onrender.com/docs
- CORS origins are configured in [app/main.py](app/main.py)

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
