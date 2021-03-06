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
            'location': self.faker.city(),
            'profile_pic': self.faker.file_path(),
            'bonus': 0
        }
        return user

    def generate_message(self):
        """Generates a random message, depending on the type
        Returns:
            (dict): a dictionary with the message's data
        """

        message = {
            'sender_id' : randint(0,9999),
            'recipient_id' : randint(0,9999),
            'text' : 'Mock',
            'delivery_date' : '2100-07-07T00:00:00Z',
            'is_draft' : False,
            'is_delivered' : False,
            'is_read' : False
        }

        return message    

    def generate_draft_message(self):
        """Generates a random message, depending on the type
        Returns:
            (dict): a dictionary with the message's data
        """

        message = {
            'sender_id' : randint(0,9999),
            'recipient_id' : randint(0,9999),
            'text' : 'Mock',
            'delivery_date' : '2100-07-07T00:00:00Z',
            'is_draft' : True,
            'is_delivered' : False,
            'is_read' : False
        }

        return message 

    def generate_delivered_message(self):
        """Generates a random message, depending on the type
        Returns:
            (dict): a dictionary with the message's data
        """

        message = {
            'sender_id' : randint(0,9999),
            'recipient_id' : randint(0,9999),
            'text' : 'Mock',
            'delivery_date' : '2100-07-07T00:00:00Z',
            'is_draft' : False,
            'is_delivered' : True,
            'is_read' : False
        }

        return message    
