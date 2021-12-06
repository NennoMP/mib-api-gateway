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

    
    def generate_user(self):
        """Generates a random user, depending on the type
        Returns:
            (dict): a dictionary with the user's data
        """

        user = {
            'id': randint(0,9999),
            'email': 'email@example.com',
            'password': "Password1@",
            'is_active' : True,
            'authenticated': False,
            'is_anonymous': False,
            'is_admin': True,
            'is_reported': False,
            'is_banned': False,
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'date_of_birth': '1970-07-07',
            'location': self.faker.city()
        }
        return user
