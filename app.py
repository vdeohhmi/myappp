import os, csv
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session, send_file, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

os.makedirs(app.instance_path, exist_ok=True)
USER_CSV = os.path.join(app.instance_path, 'users.csv')

# Dummy course data
COURSES = [
    {'id':1, 'title':'Intro to Python', 'description':'Learn Python basics', 'progress':0},
    {'id':2, 'title':'Web Development with Flask','description':'Build web apps', 'progress':0},
    {'id':3, 'title':'Data Science Fundamentals','description':'Pandas, NumPy, ML', 'progress':0}
]

# CSV helpers

def read_users():
    users=[]
    if os.path.exists(USER_CSV):
        with open(USER_CSV,newline='') as f:
            users=list(csv.DictReader(f))
    return users

def write_user(u,ph):
    exists=os.path.exists(USER_CSV)
    with open(USER_CSV,'a',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['username','password_hash'])
        if not exists: w.writeheader()
        w.writerow({'username':u,'password_hash':ph})

def find_user(username):
    return next((u for u in read_users() if u['username']==username),None)

# default admin
if not find_user('admin'):
    write_user('admin',generate_password_hash('comp2801'))

# Routes
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['username'], courses=COURSES)

@app.route('/courses')
def courses():
    return render_template('courses.html', courses=COURSES)

@app.route('/course/<int:id>')
def course_detail(id):
    course=next((c for c in COURSES if c['id']==id),None)
    if not course: abort(404)
    # simulate progress stored per session
    progress=session.get('progress',{})
    p=progress.get(str(id),0)
    return render_template('course_detail.html', course=course, progress=p)

@app.route('/course/<int:id>/update', methods=['POST'])
def update_progress(id):
    p=int(request.form['progress'])
    progress=session.get('progress',{})
    progress[str(id)] = p
    session['progress']=progress
    flash('Progress updated','success')
    return redirect(url_for('course_detail',id=id))

@app.route('/profile')
def profile():
    user=session.get('username')
    progress=session.get('progress',{})
    return render_template('profile.html', user=user, progress=progress, courses=COURSES)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u=request.form['username'].strip()
        p=request.form['password']
        if find_user(u): flash('Username exists','warning')
        else:
            write_user(u,generate_password_hash(p))
            flash('Registered!','success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=request.form['username'].strip(); p=request.form['password']
        user=find_user(u)
        if user and check_password_hash(user['password_hash'],p):
            session['username']=u
            flash('Welcome back!','success')
            return redirect(url_for('index'))
        flash('Invalid credentials','danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear(); flash('Logged out','info')
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if session.get('username')!='admin': abort(403)
    return render_template('admin.html', users=read_users())

@app.route('/admin/download')
def download_users():
    if session.get('username')!='admin': abort(403)
    return send_file(USER_CSV, as_attachment=True, download_name='users.csv')

if __name__=='__main__': app.run()
