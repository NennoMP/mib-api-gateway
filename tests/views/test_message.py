from random import choice, randint

from unittest.mock import Mock, patch
from flask.helpers import send_file
from .view_test import ViewTest
from faker import Faker


class TestMessage(ViewTest):
    faker = Faker('it_IT')

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestMessage, cls).setUpClass()
        

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
    def test_read_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Bonus GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'bonus': 666
                }
            )
        )

        # Message GET request
        message = self.generate_message()
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: message
            )
        )

        test_user = self.generate_user_json()

        # Sender GET request
        message = self.generate_message()
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: test_user
            )
        )

        # Recipient GET request
        message = self.generate_message()
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: test_user
            )
        )

        message_id = 1
        response = self.client.get(
            f'{self.BASE_URL}/message/{message_id}'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_read_message_user_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Bonus GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'bonus': 666
                }
            )
        )

        # Message GET request
        message = self.generate_message()
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: message
            )
        )

        message_id = 1
        response = self.client.get(
            f'{self.BASE_URL}/message/{message_id}'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_delete_message(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # Bonus GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'bonus': 666
                }
            )
        )

        # Message GET request
        message = self.generate_message()
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: message
            )
        )

        # Message DELETE request
        fake_responses.append(
            Mock(
                status_code=200,
            )
        )

        message_id = 1
        response = self.client.delete(
            f'{self.BASE_URL}/message/{message_id}'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_mailbox(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [],
                    'received': [],
                    'drafts': [],
                    'scheduled': []
                }
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/mailbox'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_mailbox_user_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [self.generate_message()],
                    'received': [self.generate_message()],
                    'drafts': [],
                    'scheduled': []
                }
            )
        )

        test_user = self.generate_user_json()

        # User GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: test_user
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/mailbox'
        )
        assert response.status_code == 200

    def test_mailbox_message_down(self):
        self.login()

        response = self.client.get(
            f'{self.BASE_URL}/mailbox'
        )
        assert response.status_code == 200


    @patch('requests.get')
    def test_calendar(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [],
                    'received': [],
                    'drafts': [],
                    'scheduled': []
                }
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/calendar'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_calendar_user_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [self.generate_message()],
                    'received': [self.generate_message()],
                    'drafts': [],
                    'scheduled': []
                }
            )
        )

        test_user = self.generate_user_json()

        # User GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: test_user
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/calendar'
        )
        assert response.status_code == 200

    def test_calendar_message_down(self):
        self.login()

        response = self.client.get(
            f'{self.BASE_URL}/calendar'
        )
        assert response.status_code == 200


    @patch('requests.get')
    def test_scheduled(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [],
                    'received': [],
                    'drafts': [],
                    'scheduled': [self.generate_message()]
                }
            )
        )

        test_user = self.generate_user_json()

        # User GET request 
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: test_user
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/scheduled'
        )
        assert response.status_code == 200

    @patch('requests.get')
    def test_scheduled_user_down(self, fake_get):
        self.login()

        fake_responses = []
        fake_get.side_effect = fake_responses

        # All messages GET request
        fake_responses.append(
            Mock(
                status_code=200,
                json=lambda: {
                    'sent': [],
                    'received': [],
                    'drafts': [],
                    'scheduled': [self.generate_message()]
                }
            )
        )

        response = self.client.get(
            f'{self.BASE_URL}/scheduled'
        )
        assert response.status_code == 200

    def test_scheduled_message_down(self):
        self.login()

        response = self.client.get(
            f'{self.BASE_URL}/scheduled'
        )
        assert response.status_code == 200


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
