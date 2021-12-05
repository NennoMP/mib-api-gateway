from faker import Faker
from wtforms.validators import ValidationError

from .validator_test import ValidatorTest


class AnonymousField:
    def __init__(self, data):
        self.data = data


class TestPasswordValidator(ValidatorTest):
    faker = Faker()

    def setUp(self):
        super(TestPasswordValidator, self).setUp()
        from mib.validators.validators import PasswordValidator

        self.password_validator = PasswordValidator

    def test_valid_call_password(self):
        pv = self.password_validator()
        valid_password = 'Valid1@'
        field = AnonymousField(valid_password)

        pv.__call__(None, field)

    def test_invalid_call_password(self):
        pv = self.password_validator()
        invalid_password = 'invalidpassword'
        field = AnonymousField(invalid_password)

        with self.assertRaises(ValidationError):
            pv.__call__(None, field)