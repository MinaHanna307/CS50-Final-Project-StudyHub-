# Study Hub — README

✅ **Project:** Study Hub

**Study Hub** is a lightweight Flask web application designed to make studying more structured and manageable by letting students create, edit, and organize study sessions (called "courses") with descriptions, links, and a day of the week. It includes user registration and authentication, persistent storage with SQLite, and a small, maintainable codebase intended for learning and incremental improvement.

---

## Table of Contents

- **Overview** ✅
- **Demo / Screenshots** 📺
- **Key Features** ⭐
- **Technology Stack** 🔧
- **Project Structure** 📁
- **Database Schema** 🗄️
- **Installation & Setup** 🛠️
- **Running the App** ▶️
- **Usage Guide** ✍️
- **API & Routes** 🔍
- **Security Considerations** 🔐
- **Testing** 🧪
- **Deployment Tips** 🚀
- **Troubleshooting** ⚠️
- **Roadmap / Improvements** 📈
- **Contributing** 🤝
- **License & Credits** 📜

---

## Overview

Study Hub helps students consolidate study materials and schedule study sessions across a weekly calendar. Each authenticated user can add courses with a name, description, optional links, and a selected day of the week. The app stores data in an SQLite database inside the `instance/` directory, and user accounts are protected with password hashing.

This README explains the design, how to set up and run Study Hub locally, the internal database structure, security best practices, and how to extend and deploy the application.

---

## Demo / Screenshots 📺

A short video demo is included in the project README originally: 

> Video Demo: https://youtu.be/CG2yRittCF0

Screenshots and the video demonstrate: registration flow, login, the user home page showing courses (with edit and delete controls), and the submit page used for both creating and editing courses.

---

## Key Features ⭐

- User registration with hashed passwords (Werkzeug’s `generate_password_hash`).
- Login using Flask-Login for simple session management.
- Add, edit, and delete courses for the current user.
- Persisted data using SQLite (`instance/app.db`).
- Input validation in forms (non-empty fields, valid day of week, length checks, reserved names banned).
- Secure cookie flags set in configuration to make it easier to run under HTTPS in production (`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`).
- Minimal, easy-to-read codebase—great for learning full-stack Flask web app basics.

---

## Technology Stack 🔧

- Python 3.x
- Flask
- Flask-Login
- Werkzeug (for password hashing)
- cs50 SQL wrapper (thin wrapper around SQLite; functionality used here is simple SQL execution)
- SQLite (stored under `instance/app.db`)
- Jinja2 templates under `templates/` and static assets under `static/`

> Note: The code uses a small `cs50` package wrapper for SQL. The same SQL code can be used directly with `sqlite3` or `SQLAlchemy` if you prefer a different ORM layer.

---

## Project Structure 📁

An overview of the important files and folders:

- `app.py` - Main Flask application and route definitions.
- `readme.md` - Short project description included originally (this repo also now contains this comprehensive `README.md`).
- `requirements.txt` - Python dependencies used by the project.
- `instance/` - Local instance folder that holds `app.db` (SQLite database).
- `templates/` - Jinja2 templates: `index.html`, `home.html`, `register.html`, `login.html`, `submit.html`.
- `static/` - CSS and other static assets.

Key route files and templates are directly implemented in `app.py`, making it easy to navigate and change behavior quickly during development.

---

## Database Schema 🗄️

Study Hub uses a simple schema with two tables: `users` and `courses`. SQL used in `app.py` creates these tables if they do not exist:

- `users` table:
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `name` TEXT NOT NULL UNIQUE
  - `password` TEXT NOT NULL (hashed)

- `courses` table:
  - `day` TEXT NOT NULL
  - `name` TEXT NOT NULL
  - `description` TEXT NOT NULL
  - `links` TEXT
  - `user_id` INTEGER NOT NULL (FOREIGN KEY to `users.id`)

The database design assumes that a (user_id, name) pair is used as a logical unique identifier for a user's course; the app enforces unique names per user by checking before insertion.

---

## Installation & Setup 🛠️

Follow these steps to run Study Hub on your machine.

### Prerequisites

- Python 3.8 or newer recommended
- Recommended to use a virtual environment
- On Windows 10/11, PowerShell or cmd.exe

### 1) Clone the repository

```bash
# Example
git clone <your-repo-url>
cd FinalProjectCS50
```

### 2) Create and activate a virtual environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Windows (cmd.exe):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

On macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing or incomplete, a minimal set likely includes: `Flask`, `Flask-Login`, `Werkzeug`, and `cs50`. Install with `pip install Flask Flask-Login Werkzeug cs50`.

### 4) Set configuration and environment variables

- **SECRET_KEY**: For local development you can keep it default (the application falls back to `dev-only`). For production set a secure value.

Windows PowerShell:

```powershell
$env:SECRET_KEY = "your-secure-random-string"
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"  # optional for debug behavior
```

Windows cmd.exe:

```cmd
set SECRET_KEY=your-secure-random-string
set FLASK_APP=app.py
set FLASK_ENV=development
```

macOS / Linux:

```bash
export SECRET_KEY='your-secure-random-string'
export FLASK_APP=app.py
export FLASK_ENV=development
```

> Important: When deploying, **do not** keep `SECRET_KEY=dev-only`. Use a secure secret and never commit secrets into version control.

### 5) Ensure `instance/` exists

The application expects an `instance/` folder (it holds the SQLite DB). If it is missing, create it:

```bash
mkdir instance
```

The app will create the database file and the required tables automatically on first run.

---

## Running the App ▶️

There are two main ways to run the app for development:

### 1) Flask CLI (recommended for dev)

```bash
# In PS or bash with the correct env vars set:
flask run
```

Visit http://127.0.0.1:5000/ — you will be redirected to the login page until you register and sign in.

### 2) Run directly with Python (if entrypoint exists)

If `app.py` had an if __name__ == '__main__' guard, you could run `python app.py`. As an alternative, use the Flask CLI as shown above.

---

## Usage Guide ✍️

Below is a quick walk-through of the main user flows.

### Registration

- Visit `/register`.
- Provide a unique username, a password, and a confirmation password.
- The server will check the inputs and ensure passwords match and the username is unique.
- On success, you are redirected to `/login`.

### Login

- Visit `/login`.
- Provide username and password.
- If credentials are valid, the `login_user` from Flask-Login creates a session and redirects to `/` (home).

### Home Page (`/`)

- Shows a welcome message and a list of your courses retrieved from the database by `user_id`.
- Each course shows the name, description, associated links, and the day of the week.
- Each course has Edit and Delete controls.

### Submit / Edit (`/submit`)

- Visit `/submit` to add a new course.
- When editing, the `edit` query parameter or `courseName` query param will load the course into the form for modification.
- Required fields: course name, description, day. Links are optional and default to `N/A` if left empty.
- Validation includes: non-empty required fields, day-of-week validation, length check on course name (<= 100), reserved names blocked.

### Deleting a course

- The DELETE workflow is implemented via a `POST` at `/delete` with `courseName` as the submitted form field.
- The server checks `request.form.get("courseName")` and `current_user.id` before deleting the row from `courses` table.

---

## API & Routes 🔍

Here's a summary of the key routes implemented in `app.py`:

- `GET /` — Home page (requires authentication)
- `GET|POST /login` — Login page and authentication
- `GET|POST /register` — Registration page
- `GET|POST /submit` — Submit or edit a course
- `POST /delete` — Delete a course
- `GET /logout` — Log out the user

For automated tests or API driven clients, remember to use the Flask `session` cookie set after login to access protected endpoints.

---

## Security Considerations 🔐

Study Hub includes some built-in protections and also areas where security can be improved:

- Passwords are stored hashed using Werkzeug (`generate_password_hash` and validated with `check_password_hash`). This is a **must** and is implemented.

- Flask-Login is used for session-based user authentication which handles login state securely when used over HTTPS.

- App config sets `SESSION_COOKIE_SECURE = True` and `SESSION_COOKIE_HTTPONLY = True` which is good for production behind HTTPS but may prevent cookie-based sessions over plain HTTP during development. Consider setting `DEBUG=True` and adjusting for non-HTTPS development only.

- Input validation is performed for required fields and day-of-week values. Additional measures are recommended:
  - Add CSRF protection (e.g., via Flask-WTF) to all forms.
  - Sanitize or escape any content that will be rendered in templates (Jinja2 auto-escaping helps, but be careful with links and user-provided HTML).
  - Add rate limiting on authentication endpoints to prevent brute force.
  - Add account confirmation via email and password reset flows for a production-ready app.

---

## Testing 🧪

No automated tests are included in the starter project, but here are recommendations and a minimal example for getting started with pytest and Flask's test client.

### Install testing dependencies

```bash
pip install pytest pytest-flask
```

### Minimal test example (create `tests/test_auth.py`)

```python
from app import create_app, db
import pytest

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_login_logout(client):
    # Register
    resp = client.post('/register', data={'username':'testuser','password':'pass','confirm_password':'pass'})
    assert resp.status_code == 200

    # Login
    resp = client.post('/login', data={'username':'testuser','password':'pass'})
    assert resp.status_code in (200,302)

    # logout
    resp = client.get('/logout')
    assert resp.status_code in (200,302)
```

> Note: You may need to mock or isolate the database for tests to avoid mutating the `instance/app.db` directly. Consider using a temporary SQLite DB file (e.g., `sqlite:///:memory:`) or copy the `instance/` folder for test runs.

---

## Deployment Tips 🚀

For production deployment prefer a WSGI server like Gunicorn (Linux) or Waitress (Windows).

Example Gunicorn command:

```bash
gunicorn -w 4 "app:app"
```

When deploying behind Nginx:

- Configure Nginx to handle HTTPS termination and reverse proxy to Gunicorn.
- Ensure `SECRET_KEY` is securely configured in the environment.
- Set `SESSION_COOKIE_SECURE = True` and `SESSION_COOKIE_HTTPONLY = True` (already set in `app.py`).

Docker deployment example (brief):

- Create `Dockerfile` that installs requirements, copies app, sets `FLASK_APP=app.py`, and launches via Gunicorn.
- Persist database file to a Docker volume if you want to preserve data between container restarts.

---

## Troubleshooting ⚠️

- Templates missing: If the app cannot find templates, verify `Flask(__name__, template_folder='templates')` and your working directory. In this project `app.py` uses `template_folder='templates'` and `static_folder='static'`.

- Database errors: If you get errors related to `instance/app.db`, ensure the `instance/` folder exists and has correct permissions.

- Login redirect loops: Ensure your `SECRET_KEY` is set, and check cookie behavior in browser developer tools (inspect session cookie and its attributes).

- Sessions not persisting: If `SESSION_COOKIE_SECURE` is enabled while using HTTP, cookies will not be set. Use HTTPS in production or disable that flag for local development only.

---

## Roadmap / Improvements 📈

Ideas to improve Study Hub and make it production-ready:

- Add CSRF protection using Flask-WTF.
- Add tests and CI pipelines (GitHub Actions) to run tests on push.
- Replace direct SQL with SQLAlchemy for richer data modeling and safer migrations.
- Add email-based account confirmation and password reset.
- Add user profile pages and course export/import (CSV or JSON).
- Add search and filtering of courses per user and across days.
- Add pagination and better UI/UX styling with a front-end framework (Bootstrap or Tailwind CSS).

---

## Contributing 🤝

Contributions are welcome! A suggested workflow:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Add tests and update documentation
4. Submit a pull request with a clear description of changes

Please follow best practices and do not commit secrets.

---

## License & Credits 📜

This project is provided as-is for educational purposes. Include a license file (for example MIT or Apache 2.0) if you intend to distribute or open source the code.

---

> **Need changes or extra sections?** If you want, I can add a `CONTRIBUTING.md`, sample tests for each route, a Dockerfile, or a step-by-step deployment guide for a specific host (Heroku, DigitalOcean, AWS). Just tell me which one and I’ll prepare it.

---

## Quick Reference Commands

- Create venv: `python -m venv .venv`
- Activate venv (PS): `.\.venv\Scripts\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Run dev server: `flask run`
- Inspect DB with sqlite3: `sqlite3 instance/app.db` then run `SELECT * FROM users;`

---

Thank you for using Study Hub — a small, practical app that demonstrates the essentials of building a secure and useful Flask application for study planning. If you would like, I can also:

- Add unit tests and a `pytest` configuration
- Add Docker support and a `docker-compose.yml`
- Flesh out front-end templates and add accessibility improvements

Let me know which direction you want next and I’ll prepare a follow-up change. 🚀



