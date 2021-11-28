import functools

from flask_login import LoginManager, current_user

login_manager = LoginManager()

def admin_required(func):
    '''Manage the authorizations of admin users (decorator).'''
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        if not current_user.is_admin:
            #return error if not admin
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required