from random import choice, randint

from flask import json
from unittest.mock import Mock, patch
from flask.helpers import send_file
from .view_test import ViewTest
from faker import Faker


class TestCreateMessage(ViewTest):
    faker = Faker('it_IT')

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestCreateMessage, cls).setUpClass()
        

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
    def test_edit_draft_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_draft_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?draft_id=1'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_edit_draft_message_message_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?draft_id=1'
        )
        assert response.status_code == 403

    @patch('requests.get')
    def test_edit_not_draft_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?draft_id=1'
        )
        assert response.status_code == 403


    @patch('requests.get')
    def test_edit_forw_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_delivered_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?forw_id=1'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_edit_forw_message_message_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?forw_id=1'
        )
        assert response.status_code == 403

    @patch('requests.get')
    def test_edit_not_forw_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?forw_id=1'
        )
        assert response.status_code == 403


    @patch('requests.get')
    def test_edit_reply_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_delivered_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?reply_id=1'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_edit_reply_message_message_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?reply_id=1'
        )
        assert response.status_code == 403

    @patch('requests.get')
    def test_edit_not_reply_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Users list GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'users_list': []
                }
            )
        )

        # Message GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_message()
            )
        )
        
        response = self.client.get(
            f'{self.BASE_URL}/create_message?reply_id=1'
        )
        assert response.status_code == 403


    def test_save_new_message(self):
        self.login()

        message = {
            'text_area': 'text',
            'delivery_date': '2022-10-10T08:00',
            'save_button':'Save'
        }
        
        response = self.client.post(
            f'{self.BASE_URL}/create_message',
            data=json.dumps(message), 
            content_type='application/json'
        )
        assert response.status_code == 302


    @patch('requests.get')
    def test_send_new_message(self, fake_get):
        self.login()

        message = {
            'text_area': 'text',
            'delivery_date': '2022-10-10T08:00',
            'users_list': ['2']
        }

        fake_responses = []
        fake_get.side_effect = fake_responses

        # User GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: self.generate_user()
            )
        )

        # Blacklist GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'blocked_users' : []}
            )
        )
        
        response = self.client.post(
            f'{self.BASE_URL}/create_message',
            data=json.dumps(message), 
            content_type='application/json'
        )
        assert response.status_code == 302


    @patch('mib.rao.user_manager.requests.post')
    def login(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                'user': user,
                'authentication': 'success'
            }
        )
        
        response = self.client.post(
            f'{self.BASE_URL}/login',
            json=user
        )

        assert response is not None
        return user