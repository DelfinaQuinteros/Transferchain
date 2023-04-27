from flask import Blueprint, render_template
from ..blockchain.algod import get_balance

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

