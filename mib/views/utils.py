from flask import Blueprint, abort

# This is only an utility view
utils = Blueprint('util', __name__)

def get_argument(request, arg, type):
    '''Utility function to retrieve an argument and checking its type.'''
    try:
        return request.args.get(arg, type=type)
    except:
        return None


@utils.route('/server_error')
def generate_server_error():
    """
    This method will generate an error.

    :return: Error 500
    """
    return abort(500)


