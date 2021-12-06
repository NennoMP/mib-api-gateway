from flask_login import LoginManager

from mib.rao.user_manager import UserManager
import requests
import os
from mib.auth.user import User 


def init_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.re_login'

    @login_manager.user_loader
    def load_user(user_id: int):
        """
        We need to connect to users endpoint and load the user.
        Here we can implement the redis caching

        :param user_id: user id
        :return: the user object
        """
        
        flask_env = os.getenv('FLASK_ENV', 'None')
        if flask_env == "testing":
            json_user = {
                'id': 999,
                'email': 'email@example.com',
                'password': "Password1@",
                'is_active': True,
                'authenticated': True,
                'is_anonymous': False,
                'is_admin': True,
                'is_reported': False,
                'is_banned': False,
                'firstname': 'a',
                'lastname': 'a',
                'date_of_birth': '1970-07-07',
                'location': 'a'
            }

            return User.build_from_json(json_user)
            
        user = UserManager.get_user_by_id(user_id)
        user.authenticated = True
        return user

    return login_manager
