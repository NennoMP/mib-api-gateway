import json
import requests

from datetime import date
from requests.exceptions import Timeout

from flask_login import (logout_user)
from flask import abort
from werkzeug import exceptions

from mib import app
from mib.auth.user import User


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """

        try:
            response = requests.get("%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id)),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                # user is authenticated
                user = User.build_from_json(json_payload)
            else:
                raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def get_profile_by_id(cls, user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user profile by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """

        try:
            response = requests.get("%s/profile/%s" % (cls.USERS_ENDPOINT, str(user_id)),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                # user is authenticated
                user = User.build_from_json(json_payload)
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def update_profile_pic(cls, user_id: int, format: str, file):
        """
        This method contacts the users microservice
        to allowed the users to update their profile
        picture
        :param user_id: the user id
        :param file: the new profile picture
        :return: profile picture updated
        """

        try:
            url = "%s/profile/%s/profile_picture" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.post(url, 
                                    json={
                                        'format': format,
                                        'file': file
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_language_filter(cls, user_id: int):
        """
        This method contacts the users microservice
        to allow the users to update the language filter
        :param user_id: the user id
        :return: language filter updated
        """

        try:
            url = "%s/profile/%s/language_filter" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.post(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def get_user_by_email(cls, user_email: str):
        """
        This method contacts the users microservice
        and retrieves the user object by user email.
        :param user_email: the user email
        :return: User obj with email=user_email
        """

        try:
            response = requests.get("%s/user_email/%s" % (cls.USERS_ENDPOINT, user_email),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def create_user(cls,
                    email: str, password: str,
                    firstname: str, lastname: str,
                    date_of_birth, location: str):
        try:
            url = "%s/user" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     json={
                                        'email': email,
                                        'password': password,
                                        'firstname': firstname,
                                        'lastname': lastname,
                                        'date_of_birth': date_of_birth,
                                        'location': location
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_user(cls, user_id: int, email: str, firstname: str, lastname: str, location: str):
        """
        This method contacts the users microservice
        to allow the users to update their profiles
        :param email: the user email
        :param firstname: the user firstname
        :param lastname: the user lastname
        :param location: the user location
        :param user_id: the customer id
        :return: User updated
        """
        try:
            url = "%s/profile/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.post(url,
                                    json={
                                        'email': email,
                                        'firstname': firstname,
                                        'lastname': lastname,
                                        'location': location
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                    )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def unregister_user(cls, user_id: int, password: str):
        """
        This method contacts the users microservice
        to unregister the account of the user
        :param user_id: the user id
        :return: User updated
        """

        payload = dict(password=password)
        try:
            url = "%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.post(url,
                                        json=payload,
                                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> User:
        """
        This method authenticates the user trough users AP
        :param email: user email
        :param password: user password
        :return: None if credentials are not correct, User instance if credentials are correct.
        """

        payload = dict(email=email, password=password)
        try:
            print('trying response....')
            response = requests.post('%s/authenticate' % cls.USERS_ENDPOINT,
                                     json=payload,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )
            print('received response....')
            json_response = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # We can't connect to Users MS
            return abort(500)

        if response.status_code == 401 or response.status_code == 403:
            # User is not authenticated or has been banned
            return None, json_response['message']
        elif response.status_code == 200:
            user = User.build_from_json(json_response['user'])
            return user, ''
        else:
            raise RuntimeError(
                'Microservice users returned an invalid status code %s, and message %s'
                % (response.status_code, json_response['error_message'])
            )

    @classmethod
    def logout_user(cls, email: str):
        """
        This method logout the user trough users AP
        :param email: user email
        :return: None if errors occur.
        """

        payload = dict(email=email)
        try:
            print('trying response....')
            response = requests.post('%s/logout' % cls.USERS_ENDPOINT,
                                     json=payload,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )
            print('received response....')
            json_response = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # We can't connect to Users MS
            return abort(500)
        if response.status_code == 200:
            return response
        else:
            raise RuntimeError(
                'Microservice users returned an invalid status code %s, and message %s'
                % (response.status_code, json_response['message'])
            )

    @classmethod
    def get_users_list(cls):
        """
        This method contacts the users microservice
        and retrieves the list of user objects.
        :return: User obj list
        """

        try:
            response = requests.get("%s/users/" % (cls.USERS_ENDPOINT),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            
            if response.status_code == 200:
                users_list = [User.build_from_json(user) for user in json_payload['users_list']]

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return users_list

    @classmethod
    def get_bonus(cls, user_id: int):
        """
        This method contacts the users microservice
        to get the bonus of the user
        :param user_id: id of the user
        :return: bonus if success, -1 otherwise
        """

        try:
            url = "%s/profile/%s/bonus" % (cls.USERS_ENDPOINT,
                                            str(user_id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        
        json_payload = response.json()
        return json_payload['bonus']
        
    @classmethod
    def set_bonus(cls, user_id: int, bonus):
        """
        This method contacts the users microservice
        to set the bonus of the user
        :param user_id: id of the user
        :return: bonus
        """
        payload = dict(bonus=bonus)
        try:
            url = "%s/profile/%s/bonus" % (cls.USERS_ENDPOINT,
                                           str(user_id))

            response = requests.post(url,
                                     json=payload, 
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
            
        
        return response



    @classmethod
    def report_user(cls, target_id: int):
        """
        This method contacts the users microservice
        and reports a specific user
        :param target_id: id of the user to report
        :return: User reported
        """

        try:
            url = "%s/users/%s/report_user" % (cls.USERS_ENDPOINT,
                                            str(target_id))
            response = requests.post(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def unreport_user(cls, target_id: int, user_id: int):
        """
        This method contacts the users microservice
        and reject a report of a specific user
        :param user_email: email of the user to unreport
        :return: User unreported
        """

        payload = dict(user_id=user_id)
        try:
            url = "%s/users/%s/unreport_user" % (cls.USERS_ENDPOINT,
                                            str(target_id))
            response = requests.post(url,
                                    json=payload,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_ban_user(cls, target_id: int, user_id: int):
        """
        This method contacts the users microservice
        and (un)bans an user.
        :param dest_user_email: email of the user being (un)banned
        :param src_user_id: id of the admin (un)banning
        :return: User (un)banned
        """

        payload = dict(user_id=user_id)
        try:
            url = "%s/users/%s/update_ban_user" % (cls.USERS_ENDPOINT,
                                                str(target_id))
            response = requests.post(url,
                                    json=payload,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

