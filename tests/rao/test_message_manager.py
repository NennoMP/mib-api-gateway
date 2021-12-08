from unittest.mock import Mock, patch
from faker import Faker
from random import randint
from werkzeug.exceptions import NotFound, InternalServerError
import requests


from mib.models.message import Message
from .rao_test import RaoTest

class TestMessageManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestMessageManager, self).setUp()
        from mib.rao.message_manager import MessageManager
        self.message_manager = MessageManager
        from mib import app
        self.app = app

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

    @patch('requests.get')
    def test_get_message_by_id(self, fake_get):

        fake_responses = []
        fake_get.side_effect = fake_responses

        message = self.generate_message()

        fake_responses.append (Mock(
            status_code=200,
            json = lambda: message
            )
        )

        user_id = 1
        message_id = 1

        response = self.message_manager.get_message_by_id(user_id, message_id)
        assert response is not None

        # Test 404 response
        fake_responses.append (Mock(
            status_code=404
            )
        )

        user_id = 1
        message_id = 1

        with self.assertRaises(NotFound):
             self.message_manager.get_message_by_id(user_id, message_id)

        # Test Timeout response
        fake_responses.append( requests.exceptions.Timeout())

        with self.assertRaises(InternalServerError):
             self.message_manager.get_message_by_id(user_id, message_id)


    @patch('requests.delete')
    def test_delete_message_by_id(self, fake_get):

        fake_responses = []
        fake_get.side_effect = fake_responses

        fake_responses.append (Mock(
            status_code=200
            )
        )

        user_id = 1
        message_id = 1

        response = self.message_manager.delete_message_by_id(user_id, message_id)
        assert response is None

        # Test 404 response
        fake_responses.append (Mock(
            status_code=404
            )
        )

        user_id = 1
        message_id = 1

        with self.assertRaises(NotFound):
             self.message_manager.delete_message_by_id(user_id, message_id)

        # Test Timeout response
        fake_responses.append( requests.exceptions.Timeout())

        with self.assertRaises(InternalServerError):
             self.message_manager.delete_message_by_id(user_id, message_id)

    @patch('requests.put')
    def test_update_message_by_id(self, fake_get):

        message = self.generate_message()

        fake_responses = []
        fake_get.side_effect = fake_responses

        fake_responses.append (Mock(
            status_code=200
            )
        )

        user_id = 1
        message_id = 1

        response = self.message_manager.update_message(user_id, message_id, message)
        assert response is None

        # Test 404 response
        fake_responses.append (Mock(
            status_code=404
            )
        )

        user_id = 1
        message_id = 1


        with self.assertRaises(NotFound):
             self.message_manager.update_message(user_id, message_id, message)

        # Test Timeout response
        fake_responses.append( requests.exceptions.Timeout())

        with self.assertRaises(InternalServerError):
             self.message_manager.update_message(user_id, message_id, message)


    @patch('requests.get')
    def test_get_all_messages(self, fake_get):
        
        fake_responses = []
        fake_get.side_effect = fake_responses

        # Test 404 response
        fake_responses.append (Mock(
            status_code=404
            )
        )

        user_id = 1

        with self.assertRaises(NotFound):
             self.message_manager.get_all_messages(user_id)


    @patch('requests.post')
    def test_create_message(self, fake_get):

        message = self.generate_message()
        
        fake_responses = []
        fake_get.side_effect = fake_responses

        # Test 201 response
        fake_responses.append (Mock(
            status_code=201
            )
        )

        response = self.message_manager.create_message(message)
        assert response is None
