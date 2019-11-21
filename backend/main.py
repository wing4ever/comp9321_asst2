from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

# Home page
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home page')