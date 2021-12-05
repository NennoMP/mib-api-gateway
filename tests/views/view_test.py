import unittest
from faker import Faker
from random import choice, randint

from unittest.mock import Mock, patch
import requests
from werkzeug.exceptions import HTTPException

class ViewTest(unittest.TestCase):
    faker = Faker()

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from mib import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        from mib.rao.user_manager import UserManager
        cls.user_manager = UserManager

    def login_test_user(self):
        """
        Simulate the customer login for testing the views with @login_required
        :return: customer
        """
        user = self.generate_user()

        return user
    
    def generate_user(self):
        """Generates a random user, depending on the type
        Returns:
            (dict): a dictionary with the user's data
        """

        data = {
            'id': randint(0,999),
            'email': self.faker.email(),
            'password': self.faker.password(),
            'is_active' : choice([True,False]),
            'is_admin': False,
            'is_reported': False,
            'is_banned': False,
            'authenticated': False,
            'is_anonymous': False,
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'date_of_birth': self.faker.date(),
            'location': self.faker.city()
        }
        return data

    @patch('mib.rao.user_manager.requests.post')
    def test_login(self, mock_post):
        user = self.login_test_user()
        mock_post.return_value = Mock(
            status_code=200,
            json = lambda:{
                'user': user,
                'authentication': 'success'
            }
        )
        response = self.client.post(
            self.BASE_URL+'/login',
            json=user
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_login(self, mock_post):
        user = self.login_test_user()
        mock_post.return_value = Mock(
            status_code=201,
            json = lambda:{
                'user': user,
                'status': 'success',
                'message': 'Successfully registered',
            }
        )
        response = self.client.post(
            self.BASE_URL +'/create_user/',
            json=user
        )

        assert response is not None