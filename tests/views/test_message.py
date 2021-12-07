from flask.helpers import send_file
from werkzeug.wrappers import Response
from .view_test import ViewTest
from faker import Faker
from unittest.mock import Mock, patch
import requests

from werkzeug.exceptions import HTTPException

class TestMessage(ViewTest):
    faker = Faker()

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestMessage, cls).setUpClass()

    @patch('mib.rao.message_manager.requests.post')
    def test_create_message(self, mock_post):
        self.login()
        message = self.generate_message()
        mock_post.return_value = Mock(
            status_code=201
        )
        response = self.client.post(
            f'{self.BASE_URL}/create_message/',
            json=message
        )
        assert response is not None

    @patch('mib.rao.message_manager.requests.get')
    @patch('mib.rao.user_manager.requests.get')
    def test_read_message(self, mock_get_message,mock_get_bonus):

        self.login()

        message = self.generate_message()
        mock_get_bonus.return_value=Mock(
            status_code=200,
            json=lambda: {
                'bonus':1
            }
        )
        mock_get_message.return_value = Mock(
            status_code=200,
            json=lambda: {
                'message': message
            }
        )
        message_id=1
        response = self.client.get(
            f'{self.BASE_URL}/message/{message_id}'
        )
        print ('***************',response.data)
        assert response is not None    

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