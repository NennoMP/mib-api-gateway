import requests

from flask import abort

from mib import app
from mib.models.message import Message


class MessageManager: 

    MESSAGES_ENDPOINT = app.config['MESSAGES_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_message_by_id(cls, user_id: int, message_id: int):
        """
        This method retrieves a message by its id from the message microservice
        """

        try:
            response = requests.get(f"{cls.MESSAGES_ENDPOINT}/message/{user_id}/{message_id}",
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                message = Message(**json_payload)
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message