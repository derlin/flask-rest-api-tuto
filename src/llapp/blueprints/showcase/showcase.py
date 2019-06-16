from flask import Blueprint, render_template

bp_showcase = Blueprint('showcase', __name__, template_folder='.')


@bp_showcase.route('/', methods=['GET'])
def index():
    return render_template('showcase.html')
