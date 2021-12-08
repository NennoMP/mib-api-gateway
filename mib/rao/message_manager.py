import requests

from flask import abort

from mib import app
from mib.models.message import Message
from datetime import datetime


class MessageManager: 
    MESSAGES_ENDPOINT = app.config['MESSAGES_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']


    @classmethod
    def get_message_by_id(cls, user_id: int, message_id: int):
        '''
        This method retrieves a message by its id from the message microservice
        '''
        try:
            response = requests.get(f'{cls.MESSAGES_ENDPOINT}/message/{user_id}/{message_id}',
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()

            if response.status_code == 200:
                json_payload['delivery_date'] = datetime.strptime(json_payload['delivery_date'], '%Y-%m-%dT%H:%M:%SZ')
                message = Message(**json_payload)
            elif response.status_code == 404:
                return abort(404)     
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message


    @classmethod
    def delete_message_by_id(cls, user_id: int, message_id: int):
        '''
        This method deletes a message by its id from the message microservice
        '''
        try:
            response = requests.delete(f'{cls.MESSAGES_ENDPOINT}/message/{user_id}/{message_id}',
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
           
            if response.status_code == 200:
                return
            elif response.status_code == 404:
                return abort(404)    
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)


    @classmethod
    def get_all_messages(cls, user_id: int):
        '''
        This method get all messages by its id from the message microservice
        '''
        try:
            response = requests.get(f'{cls.MESSAGES_ENDPOINT}/message/{user_id}/messages',
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)

            if response.status_code == 200:
                json_payload = response.json()
                sent = [Message(**args) for args in json_payload['sent']]
                received = [Message(**args) for args in json_payload['received']]
                drafts = [Message(**args) for args in json_payload['drafts']]
                scheduled = [Message(**args) for args in json_payload['scheduled']]
                return sent, received, drafts, scheduled

            elif response.status_code == 404:
                return abort(404)    
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)  


    @classmethod
    def update_message(cls,user_id, message_id, message):
        '''
        This method retrieves a message by its id from the message microservice
        '''
        try:
            response = requests.put(f'{cls.MESSAGES_ENDPOINT}/message/{user_id}/{message_id}', 
                                    data=message,
                                    headers = {'Content-type': 'application/json'},
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)

            if response.status_code == 200:
                return   
            elif response.status_code == 404:
                return abort(404)        
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)              


    @classmethod
    def create_message(cls, message):
        '''
        This method retrieves a message by its id from the message microservice
        '''
        try:
            response = requests.post(f'{cls.MESSAGES_ENDPOINT}/message', 
                                    data=message,
                                    headers = {'Content-type': 'application/json'},
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)

            if response.status_code == 201:
                return   
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
