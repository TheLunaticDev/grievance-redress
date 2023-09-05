from flask import Blueprint, render_template, request
# from flask_mail import Mail, Message


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
        # msg = Message(
        #    "Your Request for Grievance Submission has been recorded",
        #    sender='donotreply',
        #    recipients=[email]
        # )
        # msg.body = 'Thank you for your response.'
        # mail = Mail()
        # app = current_app
        # mail.init_app(app)
        # mail.send(msg)'
        return render_template('confirmation.html', data=data)
