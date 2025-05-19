import os
import csv
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)
USER_CSV = os.path.join(app.instance_path, 'users.csv')

# --- Helper Functions ---
def read_users():
    """Read users from CSV into a list of dicts."""
    users = []
    if os.path.exists(USER_CSV):
        with open(USER_CSV, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    return users


def write_user(username, password_hash):
    """Append a new user to the CSV."""
    file_exists = os.path.exists(USER_CSV)
    with open(USER_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username','password_hash'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'username': username, 'password_hash': password_hash})


def find_user(username):
    """Return user dict or None."""
    for user in read_users():
        if user['username'] == username:
            return user
    return None

# --- Create default admin if missing ---
if not find_user('admin'):
    # Password is 'comp2801'
    admin_hash = generate_password_hash('comp2801')
    write_user('admin', admin_hash)

# --- Routes ---
@app.route('/')
def index():
    user = session.get('username')
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if find_user(username):
            flash('Username already exists', 'warning')
        else:
            pw_hash = generate_password_hash(password)
            write_user(username, pw_hash)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = find_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
```python
import os
import csv
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# Ensure instance folder exists
os.makedirs(os.path.join(app.instance_path), exist_ok=True)
USER_CSV = os.path.join(app.instance_path, 'users.csv')

# --- Helper Functions ---
def read_users():
    """Read users from CSV into a list of dicts."""
    users = []
    if os.path.exists(USER_CSV):
        with open(USER_CSV, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    return users


def write_user(username, password_hash):
    """Append a new user to the CSV."""
    file_exists = os.path.exists(USER_CSV)
    with open(USER_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username','password_hash'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'username': username, 'password_hash': password_hash})


def find_user(username):
    """Return user dict or None."""
    for user in read_users():
        if user['username'] == username:
            return user
    return None

# --- Routes ---
@app.route('/')
def index():
    user = session.get('username')
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if find_user(username):
            flash('Username already exists', 'warning')
        else:
            pw_hash = generate_password_hash(password)
            write_user(username, pw_hash)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = find_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
