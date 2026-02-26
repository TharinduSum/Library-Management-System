# 📚 Library Management System

A FastAPI-based library management backend with RBAC and Hybrid Authentication.

## Tech Stack

| Layer      | Technology                                      |
| ---------- | ---------------------------------------------- |
| Framework  | FastAPI 0.129.2                                |
| Runtime    | Python 3.13                                    |
| Database   | MySQL 8.0.44 (Docker)                          |
| ORM        | SQLAlchemy 2.x (async)                         |
| Migrations | Alembic (optional, not configured in this repo) |
| Auth       | JWT (access + refresh) + API Key               |
| Validation | Pydantic v2                                    |

## Project Structure

```
library-management/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py       # Login, refresh token
│   │       │   ├── books.py      # CRUD books
│   │       │   ├── borrows.py    # Borrow & return books
│   │       │   ├── roles.py      # Role management
│   │       │   └── users.py      # User & API key management
│   │       └── router.py
│   ├── core/
│   │   ├── config.py             # Settings (pydantic-settings)
│   │   ├── deps.py               # Auth dependencies (hybrid auth + RBAC)
│   │   ├── permissions.py        # Permission enum + role-permission map
│   │   └── security.py           # JWT, password hashing, API key gen
│   ├── db/
│   │   ├── seed.py               # DB seeder (roles + admin user)
│   │   └── session.py            # Async engine + session
│   ├── models/                   # Role, User, APIKey, Book, Borrow
│   ├── schemas/                  # Pydantic schemas (auth, users, books, borrows, roles, api_keys)
│   ├── services/                 # Business logic (auth, users, books, borrows)
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── .gitignore
```

## Quick Start

### 1. Clone & configure

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY to a random 32+ char string
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

This will:

- Start MySQL 8.0.44
- Run the seeder (creates roles + admin user)
- Start the FastAPI app on port 8000

### 3. Run locally (without Docker app)

```bash
# Start only the DB
docker compose up db -d

# Install dependencies
pip install -r requirements.txt

# Run seeder
python -m app.db.seed

# Start server
uvicorn app.main:app --reload
```

## Migrations (Alembic – optional)

```bash
# Create a new migration
alembic revision --autogenerate -m "your message"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Authentication

### JWT (Bearer Token)

```bash
# 1. Login
POST /api/v1/auth/login
{ "username": "admin", "password": "Admin@1234" }

# 2. Use access token
Authorization: Bearer <access_token>

# 3. Refresh
POST /api/v1/auth/refresh
{ "refresh_token": "<refresh_token>" }
```

### API Key

```bash
# 1. Create API key (while logged in via JWT)
POST /api/v1/users/me/api-keys
{ "name": "My App Key" }
# Returns raw_key once — store it securely

# 2. Use API key in requests
X-API-Key: lms_<your_key>
```

## RBAC

| Role          | Key Permissions                    |
| ------------- | ---------------------------------- |
| **admin**     | All permissions                    |
| **librarian** | Manage books, members, all borrows |
| **member**    | Read books, manage own borrows     |

### Default Admin Credentials

| Field    | Value        |
| -------- | ------------ |
| Username | `admin`      |
| Password | `Admin@1234` |

> ⚠️ Change the admin password immediately in production!

## API Endpoints

| Method          | Path                          | Permission / Access            |
| --------------- | ----------------------------- | ------------------------------ |
| POST            | `/api/v1/auth/login`          | Public                         |
| POST            | `/api/v1/auth/refresh`        | Public (valid refresh token)   |
| GET             | `/api/v1/users/me`            | Authenticated                  |
| POST            | `/api/v1/users/`              | Public (register member)       |
| GET             | `/api/v1/users/`              | `member:read`                  |
| PUT             | `/api/v1/users/{id}`          | `member:update`                |
| DELETE          | `/api/v1/users/{id}`          | `member:delete`                |
| GET/POST        | `/api/v1/users/me/api-keys`   | Authenticated                  |
| GET/POST        | `/api/v1/books/`              | `book:read/create`             |
| PATCH/DELETE    | `/api/v1/books/{id}`          | `book:update/delete`           |
| POST            | `/api/v1/borrows/`            | `borrow:create`                |
| GET             | `/api/v1/borrows/`            | `borrow:read`                  |
| POST            | `/api/v1/borrows/{id}/return` | `borrow:return`                |
| GET/POST        | `/api/v1/roles/`              | `role:manage`                  |

## Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health
