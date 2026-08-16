from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
import logging
from jinja2 import TemplateNotFound
from cs50 import SQL
import os
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.update(
        SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only"),
        DEBUG = False,
        SESSION_COOKIE_SECURE = True,
        SESSION_COOKIE_HTTPONLY = True,
    )
    return app

app = create_app()

print("app.root_path =", app.root_path)
print("app.template_folder =", app.template_folder)
db = SQL("sqlite:///instance/app.db")
db.execute("CREATE TABLE IF NOT EXISTS courses (day TEXT NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, links TEXT, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    rows = db.execute("SELECT id, name, password FROM users WHERE id = ?", int(user_id))
    if not rows:
        return None
    r = rows[0]
    return User(r['id'], r['name'], r['password'])

@app.route('/')
@login_required
def index():
    if request.method == "GET":
        try:
            user=current_user
            courses=db.execute("SELECT name, description, links, day FROM courses WHERE user_id = ?", current_user.id)
            return render_template('home.html', user=user, courses=courses)
        except TemplateNotFound as e:
            logging.exception("Template not found: %s", e)
            return f"Template not found: {e}", 500

@app.route('/delete', methods=["POST"])
@login_required
def delete():
    course_name = request.form.get("courseName")
    if not course_name:
        return "Course name not provided", 400
    db.execute("DELETE FROM courses WHERE name = ? AND user_id = ?", course_name, current_user.id)
    return redirect(url_for('index'))

@app.route('/submit', methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "GET":
        try:
            edit_name = request.args.get("edit") or request.args.get("courseName")
            if edit_name:
                course = db.execute("SELECT name, description, links, day FROM courses WHERE name = ? AND user_id = ?", edit_name, current_user.id)
                if course:
                    return render_template('submit.html', course=course[0], originalName=course[0]['name'])
                else:
                    return "Course not found", 404
            return render_template('submit.html')
        except TemplateNotFound as e:
            logging.exception("Template not found: %s", e)
            return f"Template not found: {e}", 500
    if request.method == "POST":
        course_name = request.form.get("courseName")
        course_description = request.form.get("courseDescription")
        course_day = request.form.get("courseDay")
        course_links = request.form.get("courseLinks")
        original_name = request.form.get("originalName")
        if not course_links:
            course_links = "N/A"
        if not course_name or not course_description or not course_day:
            return "Please fill out all required fields", 400
        if course_day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            return "Invalid day of the week", 400
        if len(course_name) > 100:
            return "Course name too long", 400
        if course_name in ["N/A", "None", "null", "undefined"]:
            return "Invalid course name", 400
        elif course_name.strip() == "":
            return "Course name cannot be empty", 400
        if original_name:
            db.execute("UPDATE courses SET day = ?, name = ?, description = ?, links = ? WHERE name = ? AND user_id = ?", course_day, course_name, course_description, course_links, original_name, current_user.id)
        else:
            existing = db.execute("SELECT name FROM courses WHERE name = ? AND user_id = ?", course_name, current_user.id)
            if existing:
                db.execute("UPDATE courses SET description = ?, day = ?, links = ? WHERE name = ? AND user_id = ?", course_description, course_day, course_links, course_name, current_user.id)
            else:
                db.execute("INSERT INTO courses (day, name, description, links, user_id) VALUES (?, ?, ?, ?, ?)", course_day, course_name, course_description, course_links, current_user.id)
        return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        try:
            return render_template('register.html')
        except TemplateNotFound as e:
            logging.exception("Template not found: %s", e)
            return f"Template not found: {e}", 500
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        conf = request.form.get("confirm_password")
        if not name or not password or not conf:
            return "Please fill out all fields", 400
        if password != conf:
            return "Passwords do not match", 400
        existing = db.execute("SELECT name FROM users WHERE name = ?", name)
        if existing:
            return "Username already taken", 400
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO users (name, password) VALUES (?, ?)", name, hashed)
        return render_template('login.html')
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        try:
            return render_template('login.html')
        except TemplateNotFound as e:
            logging.exception("Template not found: %s", e)
            return f"Template not found: {e}", 500
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        if not name or not password:
            return "Please fill out all fields", 400
        user = authenticate(name, password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return f"Invalid username or password", 401

def authenticate(name, password):
    rows = db.execute("SELECT id, name, password FROM users WHERE name = ?", name)
    if not rows:
        return None
    r = rows[0]
    if check_password_hash(r['password'], password) and r['name'] == name:
        return User(r['id'], r['name'], r['password'])
    return None
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
