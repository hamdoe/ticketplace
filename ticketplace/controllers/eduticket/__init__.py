""" Eduticket: 기존 tintranet을 옮겨옴
"""

from flask.blueprints import Blueprint
eduticket = Blueprint('eduticket', __name__, template_folder='templates')
from . import rest, migration, list, index, sms