# KanMind

This is the backend API for **KanMind**, a Django + Django REST Framework application.

> ⚠️ A frontend is required for full project usage — placeholder for future GitHub repo.

---

## 🚀 Setup Option 1 — using `uv` (uv Toolchain)

This option uses **uv** to manage your virtual environment and run your Django app.

### 🛠️ Prerequisites

Make sure **uv** is installed and available in your shell.

### 📦 Install Dependencies
```bash
uv sync
```

This will install all dependencies into the managed `.venv`.

### 📁 Activate Environment
```bash
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 🔐 Environment Configuration

Create your environment file from the template:
```bash
cp .env.template .env
```

Generate a new Django secret key at [https://djecrety.ir/](https://djecrety.ir/) and add it to your `.env` file:
```
SECRET_KEY=your-generated-secret-key-here
```

### 🗄️ Database Setup

The database is not included in this repository. You need to create it from scratch:
```bash
# Create the database and apply all migrations
uv run python manage.py migrate
```

This will create a fresh `db.sqlite3` file with all necessary tables.

### 👤 Create a Superuser (Admin)

To access the Django admin panel:
```bash
uv run python manage.py createsuperuser
```

Follow the prompts and enter a username, email, and password.

### ▶️ Run the Development Server
```bash
uv run python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/admin/
```

Your backend API will be available at:
```
http://127.0.0.1:8000/
```

---

## 🐍 Setup Option 2 — using Python + .venv

This option uses a standard Python virtual environment.

### 📍 Create & Activate the Virtual Environment
```bash
python -m venv .venv
```

Activate it:
```bash
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 📥 Install Requirements
```bash
pip install -r requirements.txt
```

### 🔐 Environment Configuration

Create your environment file from the template:
```bash
cp .env.template .env
```

Generate a new Django secret key at [https://djecrety.ir/](https://djecrety.ir/) and add it to your `.env` file:
```
SECRET_KEY=your-generated-secret-key-here
```

### 🗄️ Database Setup

The database is not included in this repository. You need to create it from scratch:
```bash
# Create the database and apply all migrations
python manage.py migrate
```

This will create a fresh `db.sqlite3` file with all necessary tables.

### 👤 Create a Superuser (Admin)

To access the Django admin panel:
```bash
python manage.py createsuperuser
```

Follow the prompts and enter a username, email, and password.

### ▶️ Run the Development Server
```bash
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/admin/
```

Your backend API will be available at:
```
http://127.0.0.1:8000/
```

---

## 📌 Notes

### 🔐 Environment Variables
- The `.env` file contains sensitive configuration like your `SECRET_KEY`.
- **Never commit your `.env` file** to version control — it should be in your `.gitignore`.
- Use the provided `.env.template` as a reference for required variables.

### 🗄️ Database
- The database file (`db.sqlite3`) is **not** included in this repository.
- You must run `python manage.py migrate` after setup to create a fresh database.
- Make sure `db.sqlite3` is in your `.gitignore` to avoid committing it.

### 🧠 Frontend
- This project requires a frontend to fully interact with the API.
- A frontend application (separate repository) will be created later.

### 🧹 Git Ignore
- Make sure your `.venv/`, `db.sqlite3`, and `.env` are not committed to version control — add them to your `.gitignore`.

---

## 📚 Summary

| Step                | Command                              |
|---------------------|--------------------------------------|
| Create environment  | `uv sync` OR `python -m venv .venv` |
| Activate environment| `source .venv/bin/activate`          |
| **Configure .env**  | `cp .env.template .env`              |
| **Generate SECRET_KEY** | Visit https://djecrety.ir/       |
| **Create database** | `python manage.py migrate`           |
| Create superuser    | `python manage.py createsuperuser`   |
| Run server          | `python manage.py runserver`         |

---

**Welcome to KanMind!** 🧠✨