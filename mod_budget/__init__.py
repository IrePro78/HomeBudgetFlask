from flask import Blueprint

budget_blueprint = Blueprint('budget', __name__, template_folder='templates')

from . import routes