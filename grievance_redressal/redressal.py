from flask import (
    Blueprint, render_template, request,
    current_app, flash, g, redirect,
    url_for, session,
)
from datetime import date, datetime
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
import functools
import click

from grievance_redressal.db import get_db


bp = Blueprint('redressal', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('redressal.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if not (user and check_password_hash(user['password'], password)):
            error = 'Incorrect username or password!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('redressal.manage'))

        flash(error, category='error')
    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('redressal.login'))


def add_redressal(data, db):
    redressal = {}
    for d in data:
        r = db.execute(
            'SELECT * FROM redressal'
            ' WHERE g_id=?',
            (d['g_id'],)
        ).fetchall()
        redressal[d['g_id']] = r

    return redressal


@bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    db = get_db()
    data = db.execute(
        'SELECT * FROM grievance'
        ' WHERE status = \'New\''
        ' UNION'
        ' SELECT * FROM grievance'
        ' WHERE status = \'Ongoing\''
    ).fetchall()
    redressal = add_redressal(data, db)
    error = None
    if request.method == 'GET':
        return render_template('manage.html', data=data, redressal=redressal)
    if request.method == 'POST':
        redress = request.form.getlist('redressal_text')[0]
        r_date = request.form.getlist('redressal_date')[0]
        state = request.form.getlist('redressal_state')[0]
        g_id = request.form.getlist('g_id')[0]
        r_id = generate_redressal_id(db)
        try:
            db.execute(
                'INSERT INTO redressal'
                ' (r_id, g_id, schedule, redressal, datetime)'
                ' VALUES (?, ?, ?, ?, ?)',
                (r_id, g_id, r_date, redress, datetime.now())
            )
            db.execute(
                'UPDATE grievance SET status=?'
                ' WHERE g_id=?',
                (state, g_id)
            )
            db.commit()
        except db.IntegrityError:
            error = "Somebody is gonna have a bad time..."
        target_mail = db.execute(
            'SELECT email_id FROM grievance'
            ' WHERE g_id = ?',
            (g_id,)
        ).fetchone()[0]
        msg = Message(
            'A reply has been received from BGC Grievance system.',
            sender='donotreply',
            recipients=[target_mail]
        )
        msg.html = f'''
        <p>This is a reply for grievance with grievance id {g_id}.</p>
        <p>Your grievance has been marked as {state}.</p>
        <p>Here is the redressal text for your grievance.</p>
        { redress }
        <hr />
        <p>Thank you for using this service.</p>
        <p>If you have any more problem you can open up a new grievance.</p>
        '''

        mail = Mail()
        app = current_app
        mail.init_app(app)
        mail.send(msg)
        del mail

        return render_template('manage.html', data=data, redressal=redressal)

    flash(error, 'error')


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    db = get_db()
    data = db.execute(
        'SELECT * FROM grievance'
        ' WHERE status=\'New\''
    ).fetchall()
    redressal = add_redressal(data, db)
    return render_template('manage.html', data=data, redressal=redressal)


@bp.route('/ongoing', methods=['GET', 'POST'])
@login_required
def ongoing():
    db = get_db()
    data = db.execute(
        'SELECT * FROM grievance'
        ' WHERE status=\'Ongoing\''
    ).fetchall()
    redressal = add_redressal(data, db)
    return render_template('manage.html', data=data, redressal=redressal)


@bp.route('/resolved', methods=['GET', 'POST'])
@login_required
def resolved():
    db = get_db()
    data = db.execute(
        'SELECT * FROM grievance'
        ' WHERE status=\'Resolved\''
    ).fetchall()
    redressal = add_redressal(data, db)
    return render_template('manage.html', data=data, redressal=redressal)


@bp.route('/spam', methods=['GET', 'POST'])
@login_required
def spam():
    db = get_db()
    data = db.execute(
        'SELECT * FROM grievance'
        ' WHERE status=\'Spam\''
    ).fetchall()
    redressal = add_redressal(data, db)
    return render_template('manage.html', data=data, redressal=redressal)


@click.command('register')
@click.argument('username')
@click.argument('password')
def register_user(username, password):
    db = get_db()

    if not (username and password):
        click.echo('Usage: [command] register username password')
        return

    try:
        db.execute(
            'INSERT INTO user (username, password)'
            ' VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
    except db.IntegrityError:
        click.echo(f'User {username} is already registered.')
    else:
        click.echo('Successfully registered ' + str(username))


def init_app(app):
    app.cli.add_command(register_user)


def generate_redressal_id(db):
    today = date.today()
    day = str(today)[:4]
    day = day + str(today)[5:7]
    day = day + str(today)[8:]
    prefix = 'R' + day
    prefix_l = prefix + '%'
    code = db.execute(
        'SELECT COUNT(r_id) FROM redressal'
        ' WHERE r_id LIKE ?',
        (prefix_l,)
    ).fetchone()[0]
    code = code + 1
    code = prefix + str(code)
    return code
