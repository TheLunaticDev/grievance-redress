from flask import Blueprint, render_template


bp = Blueprint('grievance', __name__)


@bp.route('/')
def index():
    return render_template('grievance.html')
