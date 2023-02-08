from flask import Blueprint
from flask.json import jsonify

root_blueprint = Blueprint('root', __name__, url_prefix='')


@root_blueprint.route('/', methods=['GET'])
def index():
    return jsonify('Hello, from Flask!')
