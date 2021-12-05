from faker import Faker
from wtforms.validators import ValidationError

from .validator_test import ValidatorTest


class AnonymousField:
    def __init__(self, data):
        self.data = data


class TestEmailValidator(ValidatorTest):
    faker = Faker()

    def setUp(self):
        super(TestEmailValidator, self).setUp()
        from mib.validators.validators import EmailValidator

        self.email_validator = EmailValidator

    def test_valid_call_email(self):
        ev = self.email_validator()
        valid_email = 'valid@example.com'
        field = AnonymousField(valid_email)

        ev.__call__(None, field)

    def test_invalid_call_email(self):
        ev = self.email_validator()
        field = AnonymousField(None)

        with self.assertRaises(ValidationError):
            ev.__call__(None, field)
