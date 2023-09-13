from flask import (
    Blueprint, render_template, request, current_app, session, flash,
    url_for, redirect
)
from datetime import date, datetime
from flask_mail import Mail, Message
import pyotp
import secrets
import sys

from grievance_redressal.db import get_db


bp = Blueprint('grievance', __name__)

course = {
    'UG': [
        'ASP', 'Bengali', 'Botany', 'Chemistry',
        'Commerce', 'Computer Science', 'Economics',
        'Education', 'Electronic Science', 'English', 'Food & Nutrition',
        'Environmental Science', 'Geography', 'Hindi', 'History',
        'Journalism & Mass Com.',
        'Mathematics', 'Philosophy', 'Physical Education', 'Physics',
        'Physiology', 'Political Science', 'Sanskrit', 'Sociology',
        'Urdu', 'Zoology',
    ],
    'PG': [
        'Commerce', 'English', 'Geography', 'Urdu',
    ],
    'General': [
        'Science', 'Arts', 'Commerce',
    ],
}

sem = ['1', '2', '3', '4', '5', '6']


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'course': request.form['course'],
            'department': request.form['department'],
            'sem': request.form['sem'],
            'reg_no': request.form['reg_no'],
            'roll_no': request.form['roll_no'],
            'contact': request.form['contact'],
            'email': request.form['email'],
            'grievance': request.form['grievance'],
        }

        error = check_input(data)

        if error is None:
            session.clear()
            session['data'] = data
            return render_template('confirmation.html', data=session['data'])
        else:
            flash(error, 'error')

    return render_template('grievance.html')


@bp.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'course': request.form['course'],
            'department': request.form['department'],
            'sem': request.form['sem'],
            'reg_no': request.form['reg_no'],
            'roll_no': request.form['roll_no'],
            'contact': request.form['contact'],
            'email': request.form['email'],
            'grievance': request.form['grievance'],
        }

        if data['name'] == '':
            data['name'] = request.form['base_name']
        if data['course'] == '':
            data['course'] = request.form['base_course']
        if data['department'] == '':
            data['department'] = request.form['base_department']
        if data['sem'] == '':
            data['sem'] = request.form['base_sem']
        if data['reg_no'] == '':
            data['reg_no'] = request.form['base_reg_no']
        if data['roll_no'] == '':
            data['roll_no'] = request.form['base_roll_no']
        if data['contact'] == '':
            data['contact'] = request.form['base_contact']
        if data['email'] == '':
            data['email'] = request.form['base_email']
        if data['grievance'] == '':
            data['grievance'] = request.form['base_grievance']

        error = check_input(data)

        if error is None:
            session.clear()
            session['data'] = data
            return render_template('confirmation.html', data=session['data'])
        else:
            flash(error, 'error')

    return redirect(url_for('grievance.edit'))


@bp.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html', data=session['data'])


@bp.route('/validation', methods=['GET', 'POST'])
def validation():
    hotp = pyotp.HOTP('base32secret3232')
    if request.method == 'GET':
        choice = request.args.get('action')
        if choice == 'Edit':
            return redirect(url_for('grievance.edit'))
        if session.get('otp_pos', -1) == -1:
            session['otp_pos'] = secrets.randbelow(sys.maxsize)
            otp = hotp.at(session['otp_pos'])
            msg = Message(
                'OTP for your grievance redressal',
                sender='donotreply',
                recipients=[session['data']['email']]
            )
            msg.html = f"""
            <p>This is your OTP to be used in our grievance redressal system.
            </p>
            <p>Please do not share this OTP with anyone else.</p>
            <h3><strong>{otp}</strong></h3>"""
            mail = Mail()
            app = current_app
            mail.init_app(app)
            mail.send(msg)
            del mail

        return render_template('validation.html')

    if request.method == 'POST':
        user_otp = request.form['otp']
        if hotp.verify(user_otp, session['otp_pos']):
            db = get_db()
            data = session['data']
            g_id = generate_grievance_id(db)
            try:
                db.execute(
                    'INSERT INTO grievance'
                    ' (g_id, name, dept, course,'
                    ' sem, reg_no, roll_no,'
                    ' contact, email_id, grievance,'
                    ' datetime, status)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (g_id, data['name'], data['department'], data['course'],
                     data['sem'], data['reg_no'], data['roll_no'],
                     data['contact'], data['email'], data['grievance'],
                     datetime.now(), 'New')
                )
                db.commit()
            except db.IntegrityError:
                error = "Somebody is gonna have a bad time..."
            msg = Message(
                'New Grievance',
                sender='donotreply',
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg.html = f'''
            <p>A new grievance has been registered in the system.</p>
            <p>Grievance Id: { g_id }</p>
            '''
            mail = Mail()
            app = current_app
            mail.init_app(app)
            mail.send(msg)
            del mail
            session.clear()
            return render_template('final.html', g_id=g_id)
        else:
            return render_template('validation.html')

    flash(error, 'error')


def generate_grievance_id(db):
    today = date.today()
    day = str(today)[:4]
    day = day + str(today)[5:7]
    day = day + str(today)[8:]
    prefix = 'G' + day
    prefix_l = prefix + '%'
    code = db.execute(
        'SELECT COUNT(g_id) FROM grievance'
        ' WHERE g_id LIKE ?',
        (prefix_l,)
    ).fetchone()[0]
    code = code + 1
    code = prefix + str(code)
    return code


def check_name(data):
    if not data['name']:
        return 'You need to provide your name.'
    return None


def check_course(data):
    if not data['course']:
        return 'You need to provide your current course type.'
    elif data['course'] not in course.keys():
        return 'The course type you provided doesn\'t match our options.'
    return None


def check_department(data):
    if not data['department']:
        return 'You need to provide your department.'
    elif data['department'] not in course[data['course']]:
        return 'The department you provided doesn\'t match our options.'
    return None


def check_sem(data):
    if not data['sem']:
        return 'You need to provide your current semester'
    elif data['sem'] not in sem:
        return 'The semester you provided doesn\'t match our options.'
    return None


def check_reg_no(data):
    if not data['reg_no']:
        return 'You need to provide your registration number.'
    try:
        int(data['reg_no'])
    except ValueError:
        return 'Your registration number should only contain numbers.'
    if len(data['reg_no']) < 10:
        return 'Your registration number length is not enough.'
    elif data['reg_no'][:3] != '107':
        return 'Your registration number is not from our college.'
    return None


def check_roll_no(data):
    if not data['roll_no']:
        return 'You need to provide your roll number.'
    try:
        int(data['roll_no'])
    except ValueError:
        return 'Your roll number should only contain numbers.'
    if len(data['roll_no']) < 4:
        return 'Your roll number length is not enough.'
    return None


def check_contact(data):
    if not data['contact']:
        return 'You need to provide your contact information.'
    return None


def check_mail(data):
    if not data['email']:
        return 'You need to provide your email address.'
    return None


def check_grievance(data):
    if not data['grievance']:
        return 'You should have a grievance message'
    if len(data['grievance']) > 500:
        return 'Your grievance text cannot be larger than 500 characters.'
    return None


def check_input(data):
    error = check_name(data)
    if error:
        return error
    error = check_course(data)
    if error:
        return error
    error = check_department(data)
    if error:
        return error
    error = check_sem(data)
    if error:
        return error
    error = check_reg_no(data)
    if error:
        return error
    error = check_roll_no(data)
    if error:
        return error
    error = check_contact(data)
    if error:
        return error
    error = check_mail(data)
    if error:
        return error
    error = check_grievance(data)
    if error:
        return error

    return None
