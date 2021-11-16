from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
import json
from datetime import datetime
from excelToJSON import converter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
#Database for login and registration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
#Database for physical classes preferences for the students
app.config['SQLALCHEMY_BINDS'] = {
    'offline': 'sqlite:///physicalClasses.db',
    'filled': 'sqlite:///filled.db'
}
#Database with student's username/email who have filled their preferences..

#Specifying the maxium upload size of the time-table file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)
db = SQLAlchemy(app)
admin = Admin(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#For uploading of Time table file
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
#Make a directory if uploads does not exist
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Allowed extensions for the upload of time table.
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Class for user database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    rollNumber = db.Column(db.String(10), unique=True)
    branch = db.Column(db.String(10))
    groupNumber = db.Column(db.String(3))
    degree = db.Column(db.String(5))
    year = db.Column(db.String(4))
    isVaccinated = db.Column(db.Boolean)

#Class for the physical classes database
class PhysicalClass(db.Model):
    __bind_key__ = 'offline'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    teacherEmail = db.Column(db.String(50))
    classCode = db.Column(db.String(10))
    className = db.Column(db.String(30))
    timeSlot = db.Column(db.String(3))

#Class for student's who have filled their preferences
class Filled(db.Model):
    __bind_key__ = 'filled'
    email = db.Column(db.String(50), primary_key=True)

#class for admin page table views
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    rollNumber = StringField('Roll Number', validators=[InputRequired(), Length(min=9, max=10)])
    branch = StringField('Branch (e.g: COE, BT, ECE)', validators=[InputRequired(), Length(min=2, max=6)])
    groupNumber = StringField('Group Number (e.g: 1, 2, 3)', validators=[InputRequired(), Length(min=1, max=3)])
    degree = StringField('Degree (e.g: ug, pg)', validators=[InputRequired(), Length(min=2, max=5)])
    year = IntegerField('Year (e.g: 1, 2, 3, 4)', validators=[InputRequired()])
    isVaccinated = BooleanField('Are you vaccinated?')

#Admin tables view
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(PhysicalClass, db.session))
admin.add_view(MyModelView(Filled, db.session))

#Remove GET and POST methods from this route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file in files:
                if file and allowed_file(file.filename):
                    # filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'TimeTable.xlsx'))
        
        converter(UPLOAD_FOLDER + '/TimeTable.xlsx')
        return render_template('/index.html')
    return render_template('/upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Look for admin login..
        if form.username.data == 'admin' and form.password.data == 'adminpass':
            user = User.query.filter_by(username='admin').first()
            login_user(user, remember=form.remember.data)
            return redirect('/admin')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/dashboard')
        return '<h1> Invalid username or password! </h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, 
                        email=form.email.data, 
                        password=hashed_password,
                        rollNumber=form.rollNumber.data,
                        branch=form.branch.data,
                        groupNumber=form.groupNumber.data,
                        degree=form.degree.data,
                        year=form.year.data,
                        isVaccinated=form.isVaccinated.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New User has been created..! </h1>'
    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():  
    with open('./TimeTableDB.json') as f:
        data = json.load(f)
    timeTable = []
    #Getting the time table data from the json file for this user's batch number
    for entry in data:
        # Check if the degree and year matches..
        if current_user.degree == entry['degree'] and current_user.year == entry['year']:
            for batch in entry['time_table_data']:
                #Check if batch number and branch matches
                if current_user.branch == batch['branch'] and current_user.groupNumber == batch['batchNumber']:
                    #Now according to the day, showcase the time table..
                    dayNumber = datetime.today().weekday() + 2
                    #Need to show the next day's time-table, so showcase that
                    if dayNumber == 1:
                        timeTable = batch['timeTable']['monday']
                    elif dayNumber == 2:
                        timeTable = batch['timeTable']['tuesday']
                    elif dayNumber == 3:
                        timeTable = batch['timeTable']['wednesday']
                    elif dayNumber == 4:
                        timeTable = batch['timeTable']['thursday']
                    elif dayNumber == 5:
                        timeTable = batch['timeTable']['friday']
                    elif dayNumber == 6:
                        timeTable = batch['timeTable']['saturday']
                    else:
                        # timeTable = batch['timeTable']['monday']
                        timeTable.append("Enjoy your holiday!")
    alreadyFilled = Filled.query.filter_by(email=current_user.email).first() is not None 
    if alreadyFilled:
        return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="true")
    #If the student fills the preferences
    if request.method == "POST":
        preferences = request.form.getlist('preference[]')
        #See if student wants to attend offline/physical classes, then add his/her info to the database
        for idx, preference in enumerate(preferences):
            if preference == 'offline':
                student_entry = PhysicalClass(
                    email = current_user.email,
                    teacherEmail = timeTable[idx]['teacher_email'],
                    classCode = timeTable[idx]['class_code'],
                    className = timeTable[idx]['class_name'],
                    timeSlot = timeTable[idx]['timeSlot']
                )
                db.session.add(student_entry)
                db.session.commit()
        
        #Add the student's id to the database
        filled = Filled(email=current_user.email)
        db.session.add(filled)
        db.session.commit()
        return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="true")
        # return f"<h1>{preferences}</h1><h2>These preferences have been added to the database</h2>"
    return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="false")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)