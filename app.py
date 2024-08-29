from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_timetable.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., admin, faculty, student

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)
    day = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        course_name = request.form['course_name']
        day = request.form['day']
        time = request.form['time']
        room = request.form['room']
        new_schedule = Schedule(course_name=course_name, day=day, time=time, room=room)
        db.session.add(new_schedule)
        db.session.commit()
        flash('Class schedule added!')
        return redirect(url_for('schedule'))

    schedules = Schedule.query.all()
    return render_template('schedule.html', schedules=schedules)

@app.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_announcement = Announcement(title=title, content=content)
        db.session.add(new_announcement)
        db.session.commit()
        flash('Announcement added!')
        return redirect(url_for('announcements'))

    announcements = Announcement.query.all()
    return render_template('announcements.html', announcements=announcements)

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    # Attendance functionality can be expanded here
    return render_template('attendance.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
