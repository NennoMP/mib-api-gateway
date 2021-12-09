from unittest.mock import Mock, patch
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import InternalServerError
import requests

from .rao_test import RaoTest


class TestBlacklistManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestBlacklistManager, self).setUp()
        from mib.rao.blacklist_manager import BlacklistManager
        self.blacklist_manager = BlacklistManager
        from mib import app
        self.app = app

    
    def generate_user_json(self):
        return {
            'id': randint(0, 999),
            'email': self.faker.email(),
            'is_active' : choice([True,False]),
            'is_admin': False,
            'is_reported': False,
            'is_banned': False,
            'authenticated': choice([True,False]),
            'is_anonymous': False,
            'first_name': "Mario",
            'last_name': "Rossi",
            'profile_pic': '',
            'location': '',
            'has_language_filter': False
        }


    @patch('requests.get')
    def test_block_user(self, fake_put):
        fake_responses = []
        fake_put.side_effect = fake_responses

        blocked_user, blocking_user = self.generate_user_json(), self.generate_user_json()

        # Blocked user GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: blocked_user
            )
        )

        # Blocking user GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: blocking_user
            )
        )

        # Test Timeout response
        fake_responses.append(requests.exceptions.Timeout())

        with self.assertRaises(InternalServerError):
            self.blacklist_manager.block_user(blocked_user['id'], blocking_user['id'])


    @patch('requests.get')
    def test_unblock_user(self, fake_put):
        fake_responses = []
        fake_put.side_effect = fake_responses

        unblocked_user = self.generate_user_json()
        unblocked_user['is_active'] = True

        # User GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: unblocked_user
            )
        )

        # Test Timeout response
        fake_responses.append(requests.exceptions.Timeout())

        with self.assertRaises(Exception):
            self.blacklist_manager.unblock_user(unblocked_user['id'], unblocked_user['id']+1)


    @patch('requests.get')
    def test_unblock_unregistered_user(self, fake_put):
        fake_responses = []
        fake_put.side_effect = fake_responses

        unregistered_user = self.generate_user_json()
        unregistered_user['is_active'] = False

        # User GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: unregistered_user
            )
        )

        # Test Timeout response
        fake_responses.append(requests.exceptions.Timeout())

        with self.assertRaises(Exception):
            self.blacklist_manager.unblock_user(unregistered_user['id'], unregistered_user['id']+1)


    @patch('requests.get')
    def test_get_blocked_users_timeout(self, fake_put):
        fake_responses = []
        fake_put.side_effect = fake_responses

        user = self.generate_user_json()

        # User GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: user
            )
        )

        # Test Timeout response
        fake_responses.append(requests.exceptions.Timeout())

        with self.assertRaises(Exception):
            self.blacklist_manager.get_blocked_users(user['id'])
