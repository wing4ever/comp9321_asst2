from flask import Blueprint, render_template, flash

main = Blueprint('main', __name__)

# Home page
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home page')