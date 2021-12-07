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
            'extra': {
                'firstname': "Mario",
                'lastname': "Rossi",
                'birthdate': self.faker.date_of_birth(),
            }
        }


    # @patch('mib.rao.message_manager.requests.post')
    # def test_create_message(self, mock_post):
    #     self.login()
    #     message = self.generate_message()
    #     mock_post.return_value = Mock(
    #         status_code=201
    #     )
    #     response = self.client.post(
    #         f'{self.BASE_URL}/create_message/',
    #         json=message
    #     )
    #     assert response is not None


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
