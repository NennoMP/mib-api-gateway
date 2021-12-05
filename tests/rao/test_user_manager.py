from unittest.mock import Mock, patch
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests

from mib.auth.user import User
from .rao_test import RaoTest


TEST_FORMAT_FILE = 'png'
TEST_BINARY_FILE = 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='


class TestUserManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestUserManager, self).setUp()
        from mib.rao.user_manager import UserManager
        self.user_manager = UserManager
        from mib import app
        self.app = app

    def generate_user(self):
        extra_data = {
            'firstname': "Mario",
            'lastname': "Rossi",
            'birthdate': TestUserManager.faker.date_of_birth(),
        }

        data = {
            'id': randint(0, 999),
            'email': TestUserManager.faker.email(),
            'is_active' : choice([True,False]),
            'is_admin': False,
            'is_reported': False,
            'is_banned': False,
            'authenticated': choice([True,False]),
            'is_anonymous': False,
            'extra': extra_data,
        }

        user = User(**data)
        return user

    @patch('mib.rao.user_manager.requests.post')
    def test_create_user(self, mock_post):
        user = self.generate_user()
        psw = TestUserManager.faker.password()
        first_name = TestUserManager.faker.first_name()
        last_name = TestUserManager.faker.last_name()
        date_of_birth = TestUserManager.faker.date_of_birth()
        location = TestUserManager.faker.city()

        mock_post.return_value = Mock(
            status_code=201,
            json = lambda:{
                'user': user,
                'status': 'success',
                'message': 'Successfully registered'
            }
        )
        response = self.user_manager.create_user(user.email,
                                            psw,
                                            first_name,
                                            last_name,
                                            date_of_birth,
                                            location
                                        )
        assert response is not None

        # Test user already exists
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=403,
            json=lambda : {
                'status': 'Already present',
                'message': 'User already exists'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.create_user(user.email,
                                            psw,
                                            first_name,
                                            last_name,
                                            date_of_birth,
                                            location
                                        )
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_id(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False,
            }
        )
        response = self.user_manager.get_user_by_id(id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_id_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_update_user(self, mock_post):
        user = self.generate_user()
        email = TestUserManager.faker.email()
        first_name = TestUserManager.faker.first_name()
        last_name = TestUserManager.faker.last_name()
        location = TestUserManager.faker.city()


        mock_post.return_value = Mock(
            status_code=200,
            json = lambda:{
                'user': user,
                'status': 'success',
                'message': 'Successfully updated'
            }
        )
        response = self.user_manager.update_user(user.id,
                                    email,
                                    first_name,
                                    last_name,
                                    location
                                )
        print("STATUS: ", response.status_code)
        assert response.status_code == 200

    @patch('mib.rao.user_manager.requests.post')
    def test_update_user_error(self, mock_post):
        email = TestUserManager.faker.email()
        first_name = TestUserManager.faker.first_name()
        last_name = TestUserManager.faker.last_name()
        location = TestUserManager.faker.city()

        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'status': 'not success',
                'message': 'Incorrect email format'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.update_user(randint(0,999),
                                    email,
                                    first_name,
                                    last_name,
                                    location
                                )
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_id(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'is_admin': False,
                'is_reported': False,
                'is_banned': False,
                'authenticated': False,
                'is_anonymous': False,
            }
        )
        response = self.user_manager.get_user_by_id(id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_id_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(
            status_code=400,
            json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_email(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'is_admin': False,
                'is_reported': False,
                'is_banned': False,
                'authenticated': False,
                'is_anonymous': False,
            }
        )
        response = self.user_manager.get_user_by_email(user.email)
        assert response is not None
    
    @patch('mib.rao.user_manager.requests.get')
    def test_get_user_by_email_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        email = TestUserManager.faker.email()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_email(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_authenticate_user(self, mock_post):        
        user = self.generate_user()
        user_data = {
            'id': user.id,
            'email': user.email,
            'is_active': False,
            'is_admin': False,
            'is_reported': False,
            'is_banned': False,
            'authenticated': False,
            'is_anonymous': False,
        }
        mock_post.return_value = Mock(
            status_code=200,
            json = lambda:{
                'user': user_data,
                'authentication': 'success',
                'message': 'Valid credentials'
            }
        )
        password = TestUserManager.faker.password()
        response = self.user_manager.authenticate_user(
            email=user.email, password=password
        )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_authenticate_user_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=400,
            json = lambda:{
                'user': None,
                'authentication': 'failure',
                'message': 'Your account is no longer active',
            }
        )
        with self.app.test_request_context ():
            with self.assertRaises(HTTPException) as http_error:
                self.user_manager.authenticate_user(
                    self.faker.email(),
                    self.faker.password()
                )
                self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_profile(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'is_admin': False,
                'is_reported': False,
                'is_banned': False,
                'authenticated': False,
                'is_anonymous': False,
            }
        )
        response = self.user_manager.get_profile_by_id(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_profile_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(
            status_code=404,
            json=lambda : {'status': 'User not present'})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_profile_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_update_profile_pic(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json = lambda:{
                'status': 'success',
                'message': 'Profile picture updated'
            }
        )
        response = self.user_manager.update_profile_pic(user.id,
                                                TEST_FORMAT_FILE,
                                                TEST_BINARY_FILE
                                            )
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_update_profile_pic_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'status': 'failed',
                'message': 'Could not update the profile picture, user not found'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.update_profile_pic(randint(0, 999),
                                            TEST_FORMAT_FILE,
                                            TEST_BINARY_FILE
                                        )
            self.assertEqual(http_error.exception.code, 500)
            
    @patch('mib.rao.user_manager.requests.post')
    def test_update_language_filter(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda:{
                'status': 'success',
                'message': 'Successfully updated language filter'
            }
        )
        response = self.user_manager.update_language_filter(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_update_language_filter_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda:{
                'status': 'failed',
                'message': 'Could not updated language filer, user not gound'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.update_language_filter(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_unregister_user(self, mock_post):
        user = self.generate_user()
        psw = TestUserManager.faker.password()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda:{
                'status': 'success',
                'message': 'Successfully unregistered'
            }
        )
        response = self.user_manager.unregister_user(user.id, psw)
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_unregister_user_error(self, mock_post):
        psw = TestUserManager.faker.password()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'status': 'User not present'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.unregister_user(randint(0, 999), psw)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_logout_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=200,
            json = lambda:{
                'authentication': 'success',
                'message': 'Successfully logout'
            }
        )
        response = self.user_manager.logout_user(user.email)
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_logout_user_error(self, mock_post):
        email = TestUserManager.faker.email()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'authentication': 'failed',
                'message': 'Failed logout'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.logout_user(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_users_list(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'users_list': [],
                'status': 'Success'
            }
        )
        response = self.user_manager.get_users_list()
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_users_list_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(
            status_code=404
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_users_list()
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_report_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda : {
                'status': 'Success',
                'message': 'Successfully reported'
            }
        )
        response = self.user_manager.report_user(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_report_user_error(self, mock_post):
        email = TestUserManager.faker.email()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'status': 'User not present'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.report_user(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_unreport_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda : {
                'status': 'Success',
                'message': 'Successfully unreported'
            }
        )
        response = self.user_manager.unreport_user(user.id, randint(0, 999))
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_unreport_user_error(self, mock_post):
        email = TestUserManager.faker.email()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=404,
            json=lambda : {
                'status': 'Failed',
                'message': 'Unauthorized action'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.unreport_user(randint(0, 999), randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.post')
    def test_update_ban_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=202,
            json=lambda : {
                'status': 'Success',
                'message': 'Successfully banned'
            }
        )
        response = self.user_manager.update_ban_user(user.id, randint(0, 999))
        assert response is not None

    @patch('mib.rao.user_manager.requests.post')
    def test_update_ban_user_error(self, mock_post):
        email = TestUserManager.faker.email()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(
            status_code=401,
            json=lambda : {
                'status': 'Failed',
                'message': 'Unauthorized action'
            }
        )
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.update_ban_user(randint(0, 999), randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)
