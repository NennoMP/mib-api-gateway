from flask import Blueprint, abort

# This is only an utility view
utils = Blueprint('util', __name__)


@utils.route('/server_error')
def generate_server_error():
    """
    This method will generate an error.

    :return: Error 500
    """
    return abort(500)
