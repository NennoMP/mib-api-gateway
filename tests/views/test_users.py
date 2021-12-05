from werkzeug.wrappers import Response
from .view_test import ViewTest
from faker import Faker
from unittest.mock import Mock, patch
import requests

from werkzeug.exceptions import HTTPException

class TestUser(ViewTest):
    faker = Faker()

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user(self, mock_post):
        response = self.client.get(
            self.BASE_URL+'/create_user/'
        )
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=201,
            json=lambda: {
                'user': user,
                'status': 'success',
                'message': 'Successfully registered',
            }
        )
        response = self.client.post(
            self.BASE_URL+'/create_user/',
            json=user
        )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user_error_exists_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=403, json=lambda: {'message': 'user already exists'})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                response = self.client.post(
                    self.BASE_URL+'/create_user/',
                    json=user
                )
                assert response is not None
    
    @patch('mib.rao.user_manager.requests.post')
    def test_create_user_error_invalid_data(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=409, json=lambda: {'message': 'invalid data format'})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                response = self.client.post(
                    self.BASE_URL+'/create_user/',
                    json=user
                )
                assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_reported(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                'status': 'success',
                'users_list': user
                }
        )
        
        response = self.client.get(
            self.BASE_URL+'/reported_users/',
            json=user
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_unregister(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success'
            }
        )

        response = self.client.post(
            self.BASE_URL+'/unregister_user/',
            json=user
        )

        assert response is not None




    @patch('mib.rao.user_manager.requests.post')
    def test_user_login(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                'user': user,
                'authentication': 'success'
            }
        )
        
        response = self.client.post(
            self.BASE_URL+'/login',
            json=user
        )

        assert response is not None
        return user


        
