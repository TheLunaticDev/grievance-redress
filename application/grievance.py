from flask import (
    Blueprint, render_template, request, current_app, session, flash
)
from datetime import date
from flask_mail import Mail, Message
import pyotp
import secrets
import sys

from application.db import get_db


bp = Blueprint('grievance', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('grievance.html')
    elif request.method == 'POST':
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

        session.clear()
        session['data'] = data
        return render_template('confirmation.html', data=session['data'])


@bp.route('/validation', methods=['GET', 'POST'])
def validation():
    hotp = pyotp.HOTP('base32secret3232')
    if request.method == 'GET':
        if session.get('otp_pos', -1) == -1:
            session['otp_pos'] = secrets.randbelow(sys.maxsize)
            print("pos: " + str(session['otp_pos']))
            otp = hotp.at(session['otp_pos'])
            print("Current otp: " + str(otp))
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

        return render_template('validation.html')

    if request.method == 'POST':
        user_otp = request.form['otp']
        print('After otp: ' + user_otp)
        print("pos: " + str(session['otp_pos']))
        print(type(user_otp))
        print(type(session['otp_pos']))
        if hotp.verify(user_otp, session['otp_pos']):
            db = get_db()
            data = session['data']
            g_id = generate_grievance_id(db)
            try:
                db.execute(
                    'INSERT INTO grievance'
                    ' (g_id, name, dept, sem, reg_no,'
                    ' roll_no, contact, email_id, grievance)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (g_id, data['name'], data['department'], data['sem'],
                     data['reg_no'], data['roll_no'], data['contact'],
                     data['email'], data['grievance'])
                )
                db.commit()
            except db.IntegrityError:
                error = "Somebody is gonna have a bad time..."
            msg = Message(
                'New Grievance',
                sender='donotreply',
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg.html = '''
            <p>A new grievance has been registered in the system.</p>
            '''
            mail = Mail()
            app = current_app
            mail.init_app(app)
            mail.send(msg)
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
