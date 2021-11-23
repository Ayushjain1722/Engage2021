from flask import Flask, render_template, redirect, url_for, request, flash
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
from flask_mail import Mail, Message
import os
import json
import logging
from datetime import datetime
from flask_apscheduler import APScheduler
from scheduler.excelToJSON import converter
import scheduler.covidCertiVerification as covidCertiVerification
from scheduler.selectionAlgo import studentSelection
from scheduler.credentials import mailingID, mailingPassword
from scheduler.config import cronTimeHour, cronTimeMinute

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
#Database for login and registration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_BINDS'] = {
    #Database for physical classes preferences for the students
    'offline': 'sqlite:///physicalClasses.db',
    #Database with student's username/email who have filled their preferences
    'filled': 'sqlite:///filled.db',
    'bulletin': 'sqlite:///bulletinboard.db'
}


#Specifying the maxium upload size of the time-table file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)
db = SQLAlchemy(app)
admin = Admin(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mailingID
app.config['MAIL_PASSWORD'] = mailingPassword
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = APScheduler()

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

#Scheduling the cron job for daily purpose

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
    #Integer field: 0 if not vaccinated, 1 if partially vaccinated and 2 if fully vaccinated
    isVaccinated = db.Column(db.Integer)

#Class for the physical classes database
class PhysicalClass(db.Model):
    __bind_key__ = 'offline'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    teacherEmail = db.Column(db.String(50))
    classCode = db.Column(db.String(10))
    className = db.Column(db.String(30))
    timeSlot = db.Column(db.String(3))
    isVaccinated = db.Column(db.Integer)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)

#Class for student's who have filled their preferences
class Filled(db.Model):
    __bind_key__ = 'filled'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

#Class for bulletin board
class Bulletin(db.Model):
    __bind_key__ = 'bulletin'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    link = db.Column(db.String(100))

#class for admin page table views
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

def scheduledTask():
    studentList, teacherList = studentSelection(User.query.all(), PhysicalClass.query.all())
    #Sending the mails to all students
    for student in studentList:
        msg = Message('Physical Classes Update', sender="engage2021ayush@gmail.com", recipients=['ayushjain1722@gmail.com'])
        msg.body = "Dear student, \nPlease find below the physical classes alotted to you for tomorrow."
        filename = student['email'] + '.csv'
        with app.open_resource(f"scheduler/mails/{filename}", "rb") as fp:   
            msg.attach(filename="classes.csv", content_type="text/plain", data=fp.read())  
        with app.app_context():
            mail.send(msg)
        os.remove(f"scheduler/mails/{filename}")
    #Sending the mails to all teachers
    for teacher in teacherList:
        msg = Message('Students list for physical classes', sender="engage2021ayush@gmail.com", recipients=[teacher['email']])
        msg.body = "Respected Professor, \nPlease find below the students list for tomorrow's physical classes."
        filename = teacher['email'] + '.csv'
        with app.open_resource(f"scheduler/mails/{filename}", "rb") as fp:
            msg.attach(filename="students.csv", content_type="text/plain", data=fp.read())
        with app.app_context():
            mail.send(msg)
        os.remove(f"scheduler/mails/{filename}")
    #Delete all entries from the physical and filled databases
    try:
        db.session.query(PhysicalClass).delete()
        db.session.query(Filled).delete()
        db.session.commit()
    except:
        db.session.rollback()

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
    isVaccinated = IntegerField('Are you vaccinated?')

#Admin tables view
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(PhysicalClass, db.session))
admin.add_view(MyModelView(Filled, db.session))
admin.add_view(MyModelView(Bulletin, db.session))

#Remove GET and POST methods from this route
@app.route('/', methods=['GET', 'POST'])
def index():
    dictFormat = []
    for obj in Bulletin.query.all():
        dictFormat.append({'title': obj.__dict__['title'], 'link': obj.__dict__['link']})
    return render_template('index.html', notices=dictFormat)

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
        flash('Time table uploaded successfully')
        return render_template('/upload.html')
    return render_template('/upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Look for admin login..
        if form.username.data == 'admin' and form.password.data == User.query.filter_by(username=form.username.data).first().password:
            user = User.query.filter_by(username='admin').first()
            login_user(user, remember=form.remember.data)
            return redirect('/admin')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/dashboard')
        flash('Invalid username or password !')
        return redirect('/login')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
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
                            isVaccinated=0)
            db.session.add(new_user)
            db.session.commit()
            flash('New User Created!')
            return redirect('/login')
    except:
        flash('One or more entries already exists in the database. Please enter your details carefully.')
        return redirect('/signup')
    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():  
    with open('scheduler/TimeTableDB.json') as f:
        data = json.load(f)
    timeTable = []
    #Getting the time table data from the json file for this user's batch number
    for entry in data:
        # Check if the degree and year matches..
        if current_user.degree == entry['degree'] and current_user.year == entry['year']:
            for batch in entry['time_table_data']:
                #Check if batch number and branch matches
                if current_user.branch == batch['branch'] and str(current_user.groupNumber).strip() == str(batch['batchNumber']).strip():
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
                        timeTable = batch['timeTable']['monday']
                    elif dayNumber == 5:
                        timeTable = batch['timeTable']['friday']
                    elif dayNumber == 6:
                        timeTable = batch['timeTable']['saturday']
                    else:
                        timeTable = batch['timeTable']['monday']
                        # timeTable.append("Enjoy your holiday!")
                        # timeTable = []
    if len(timeTable) == 0:
        flash("No classes for tomorrow!")
    #Insert time checking code here
    alreadyFilled = Filled.query.filter_by(email=current_user.email).first() is not None 
    timeNow = datetime.now()
    #If time for filling is over, don't allow any more submissions
    if timeNow.hour >= cronTimeHour and timeNow.minute >= cronTimeMinute:
        alreadyFilled = True
    if alreadyFilled:
        flash("You have already filled your preferences or time for filling is over!")
        return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="true", vaccinationStatus=current_user.isVaccinated)
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
                    timeSlot = timeTable[idx]['timeSlot'],
                    isVaccinated = current_user.isVaccinated
                )
                db.session.add(student_entry)
                db.session.commit()
        
        #Add the student's id to the database
        filled = Filled(email=current_user.email)
        db.session.add(filled)
        db.session.commit()
        return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="true", vaccinationStatus=int(current_user.isVaccinated))
        # return f"<h1>{preferences}</h1><h2>These preferences have been added to the database</h2>"
    return render_template('dashboard.html', name=current_user.username, timeTable=timeTable, alreadyFilled="false", vaccinationStatus=int(current_user.isVaccinated))

@app.route('/covid_verify', methods=["GET", "POST"])
@login_required
def covid_verify():
    if request.method == "POST":
        beneficiary_id = request.form.get('beneficiary_id')
        priority = covidCertiVerification.priority(beneficiary_id)
        flash("Vaccination status updated")
        flash(f"Status: {covidCertiVerification.getStatus(beneficiary_id)}")
        user_vaccination = User.query.filter_by(username=current_user.username).first()
        user_vaccination.isVaccinated = priority
        db.session.commit()
        return redirect('/dashboard')
    else:
        return render_template('covid_verify.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#Error handlers: Commonly encountered errors which are possible in the application
@app.errorhandler(400)
def not_found(e):
    return render_template('error.html', error=e, code=400), 400
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e, code=404), 404
@app.errorhandler(403)
def not_found(e):
    return render_template('error.html', error=e, code=403), 403
@app.errorhandler(500)
def not_found(e):
    return render_template('error.html', error=e, code=500), 500
@app.errorhandler(502)
def not_found(e):
    return render_template('error.html', error=e, code=502), 502
@app.errorhandler(503)
def not_found(e):
    return render_template('error.html', error=e, code=503), 503
@app.errorhandler(504)
def not_found(e):
    return render_template('error.html', error=e, code=504), 504

if __name__ == '__main__':
    logging.basicConfig(filename="logs.log", level=logging.DEBUG)
    scheduler.add_job(id='Scheduled task', func=scheduledTask, trigger='cron', hour=cronTimeHour, minute=cronTimeMinute)
    scheduler.start()    
    app.run(debug=True, use_reloader=False)