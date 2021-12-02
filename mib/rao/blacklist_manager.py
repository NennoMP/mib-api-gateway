import requests

from flask import abort, jsonify

from mib import app
from .user_manager import UserManager


def exists_user(user):
    return not(user is None or not user.is_active or user.is_banned)


class BlacklistManager:
    BLACKLIST_ENDPOINT = app.config['BLACKLIST_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    

    @classmethod
    def block_user(cls, target_id: int, user_id: int):
        """
        This method contacts the users microservice
        and blocks an user for the source user
        :param user_id: id of the user blocking
        :param target_id: id of the user being blocked
        :return: User blocked
        """

        # Check if users exist
        UserManager.get_user_by_id(target_id)
        UserManager.get_user_by_id(user_id)

        payload = dict(blocking_id=user_id, blocked_id=target_id)
        try:
            url = "%s/blacklist" % (cls.BLACKLIST_ENDPOINT)
            response = requests.put(url,
                                    json=payload,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def unblock_user(cls, target_id: int, user_id: int):
        """
        This method contacts the users microservice
        and blocks an user for the source user
        :param user_id: id of the user blocking
        :param target_id: id of the user being blocked
        :return: User blocked
        """

        # Check if users exist
        target = UserManager.get_user_by_id(target_id) # User to be blocked
        if not exists_user(target):
            response = {
                'status': 'failed',
                'message': 'user cannot be unblocked',
            }
            return jsonify(response), 409
        
        payload = dict(blocking_id=user_id, blocked_id=target_id)
        try:
            url = "%s/blacklist" % (cls.BLACKLIST_ENDPOINT)
            response = requests.post(url,
                                    json=payload,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response


    
    @classmethod
    def get_blocked_users(cls, user_id: int):
        """
        This method contacts the users microservice
        and retrives all the blocked users
        :param user_id: id of the user
        :return: Blocked users list
        """

        # Check if user exist
        UserManager.get_user_by_id(user_id)

        try:
            url = "%s/blocked_users/%s" % (cls.BLACKLIST_ENDPOINT, 
                                        str(user_id))
            response = requests.get(url,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response
