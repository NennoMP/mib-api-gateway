from flask.helpers import send_file
from werkzeug.wrappers import Response
from .view_test import ViewTest
from faker import Faker
from unittest.mock import Mock, patch
import requests

from werkzeug.exceptions import HTTPException

# Utils for testing upload of profile picture
TEST_PATH_FILE = 'mib/tests/static/images/test.png'


class TestUser(ViewTest):
    faker = Faker()

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user(self, mock_post):
        response = self.client.get(
            f'{self.BASE_URL}/create_user/'
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
            f'{self.BASE_URL}/create_user/',
            json=user
        )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user_error_exists_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=403, json=lambda: {'message': 'user already exists'})
        with self.app.test_request_context():
            response = self.client.post(
                f'{self.BASE_URL}/create_user/',
                json=user
            )
            assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user_error_invalid_data(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=409, json=lambda: {'message': 'invalid data format'})
        with self.app.test_request_context():
            response = self.client.post(
                f'{self.BASE_URL}/create_user/',
                json=user
            )
            assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user_error(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=404
        )
        with self.app.test_request_context():
            response = self.client.post(
                f'{self.BASE_URL}/create_user/',
                json=user
            )
            assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_profile(self, mock_get):
        user = self.test_user_login()
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['firstname'],
                'last_name': user['lastname'],
                'date_of_birth': user['date_of_birth'],
                'location': user['location'],
                'bonus': user['bonus'],
                'profile_pic': user['profile_pic'],
                'is_active': user['is_active'],
                'authenticated': user['authenticated'],
                'is_anonymous': user['is_anonymous'],
                'is_admin': user['is_admin'],
                'is_reported': user['is_reported'],
                'is_banned': user['is_banned']
            }
        )
        response = self.client.get(
            f'{self.BASE_URL}/profile/'
        )
        
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_profile(self, mock_post):

        # Upload profile picture error
        data = {
            'action': 'Upload',
            'profile_pic': TEST_PATH_FILE
        }
        mock_post.return_value = Mock(
            status_code=404,
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update profile info error
        user = self.test_user_login()
        data = {
            'action': 'Save',
            'email': self.faker.email(),
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'location': self.faker.city()
        }
        mock_post.return_value = Mock(
            status_code=409,
            json=lambda: {
                'user': user,
                'status': 'success',
                'message': 'Successfully updated'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update profile info
        user = self.test_user_login()
        data = {
            'action': 'Save',
            'email': self.faker.email(),
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'location': self.faker.city()
        }
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                'user': user,
                'status': 'success',
                'message': 'Successfully updated'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update language filter error
        data = {
            'action': 'toggleFilter',
        }
        mock_post.return_value = Mock(
            status_code=404,
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update language filter
        data = {
            'action': 'toggleFilter',
        }
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success',
                'message': 'Successfully updated language filter'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_profile_error(self, mock_post):

        # Update profile info error
        user = self.test_user_login()
        data = {
            'action': 'Save',
            'email': self.faker.email(),
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'location': self.faker.city()
        }
        mock_post.return_value = Mock(
            status_code=409,
            json=lambda: {
                'user': user,
                'status': 'success',
                'message': 'Successfully updated'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update language filter error
        data = {
            'action': 'toggleFilter',
        }
        mock_post.return_value = Mock(
            status_code=404,
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

        # Update language filter
        data = {
            'action': 'toggleFilter',
        }
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success',
                'message': 'Successfully updated language filter'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/profile/', 
            data=data
        )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_users(self, mock_post):
        # Success
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Report'
        }
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success',
                'message': 'Successfully reported'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/users/',
            data=data
        )

        assert response is not None

        # Error
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Report'
        }
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda: {
                'status': 'User not found'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/users/',
            data=data
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_users_error(self, mock_post):

        # Error
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Report'
        }
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda: {
                'status': 'User not found'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/users/',
            data=data
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_reported(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                'status': 'success',
                'users_list': []
                }
        )
        response = self.client.get(
            f'{self.BASE_URL}/moderation/',
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_reported(self, mock_get):
        # Reject
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Reject'
        }
        mock_get.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'Success',
                'message': 'Successfully unreported'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/moderation/',
            data=data
        )
        assert response is not None

        # Ban
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Ban'
        }
        mock_get.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success',
                'message': 'Successfully banned'
            }
        )
        response = self.client.post(
            f'{self.BASE_URL}/moderation/',
            data=data
        )
        assert response is not None

        # Error
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Reject'
        }
        mock_get.return_value = Mock(
            status_code=404
        )
        response = self.client.post(
            f'{self.BASE_URL}/moderation/',
            data=data
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_post_reported_error(self, mock_get):

        # Error
        user = self.test_user_login()
        data = {
            'id': user['id'],
            'action': 'Reject'
        }
        mock_get.return_value = Mock(
            status_code=404
        )
        response = self.client.post(
            f'{self.BASE_URL}/moderation/',
            data=data
        )

        assert response is not None

    
    @patch('mib.rao.user_manager.requests.post')
    def test_unregister(self, mock_post):
        self.client.get(
            f'{self.BASE_URL}/unregister_user/',
        )

        user = self.test_user_login()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda: {
                'status': 'success'
            }
        )
        
        response = self.client.post(
            f'{self.BASE_URL}/unregister_user/',
            json=user
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_unregister_invalid_password(self, mock_post):
        user = self.test_user_login()
        mock_post.return_value = Mock(
            status_code=401,
            json=lambda: {
                'status': 'failed'
            }
        )
        
        response = self.client.post(
            f'{self.BASE_URL}/unregister_user/',
            json=user
        )

        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_unregister_error(self, mock_post):
        user = self.test_user_login()
        
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda: {
                'status': 'User not present'
            }
        )
        
        response = self.client.post(
            f'{self.BASE_URL}/unregister_user/',
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
            f'{self.BASE_URL}/login',
            json=user
        )

        assert response is not None
        return user

    @patch('mib.rao.user_manager.requests.post')
    def test_user_logout(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                'authentication': 'success',
                'message': 'Successfully logout'
            }
        )

        response = self.client.get(
            f'{self.BASE_URL}/logout'
        )

        assert response is not None
