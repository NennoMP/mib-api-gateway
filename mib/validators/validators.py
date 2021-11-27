import datetime
from wtforms.validators import ValidationError

# GLOBALS FOR FORM CHECKS
SPECIAL_CHARACTERS = '@#$%&*-_/'
ALLOWED_EMAILS = {'@test.com',
                  '@hotmail.com',
                  '@hotmail.it',
                  '@outlook.com',
                  '@outlook.it',
                  '@gmail.com',
                  '@gmail.it',
                  '@yahoo.com',
                  '@yahoo.it',
                  '@studenti.unipi.it',
                  '@di.unipi.it'
                  }


class EmailValidator(Exception):

    def __init__(self):
        """Email Validation."""

        self.message = "unrecognized email provider!"

    def __call__(self, form, field):
        email = field.data
        valid = False

        for e in ALLOWED_EMAILS:
            if str(email).endswith(e):
                self.message = ""
                valid = True

        if not valid:
            raise ValidationError(self.message)


class PasswordValidator(Exception):

    def __init__(self):
        """Password Validation."""

        self.message = ""

    def __call__(self, form, field):
        password = field.data
        valid = True

        # Check if upper cases
        if not any(el.isupper() for el in password):
            valid = False
            self.message = 'at least one upper case!'
        # Check if numbers
        if not any(el.isdigit() for el in password):
            valid = False
            self.message = 'at least one digit!'
        # Check if special characters
        if not any(el in SPECIAL_CHARACTERS for el in password):
            valid = False
            self.message = 'at least one special character: [@#$%&*-_/]!'

        if not valid:
            raise ValidationError(self.message)


class AgeValidator(Exception):

    def __init__(self, min_age=0, max_age=0):
        """
        Age validation.

        :param min_age: 0 means no limit
        :param max_age: 0 means no limit
        """
        self.min_age = min_age
        self.max_age = max_age

        if type(min_age) != int and type(min_age) != int:
            raise ValueError('min_age and max_age must be integers!')

        if min_age < 0 or max_age < 0:
            raise ValueError('min_age(%d) and max_age(%d) must be positive!' % (min_age, max_age))

        if min_age > max_age != 0:
            raise ValueError('max_age(%d) must be greater than min_age(%d)!' % (max_age, min_age))

        self.message = ""

    def __call__(self, form, field):
        check_year = field.data

        if check_year:
            current_year = datetime.date.today()
            difference = current_year - check_year
            years = difference.days / 365.25

            if self.max_age == 0:
                # means no upper bound
                if years < self.min_age:
                    valid = False
                    self.message = "You are too young!"
                else:
                    valid = True
            elif self.min_age == 0:
                if years > self.max_age:
                    valid = False
                    self.message = "You are too old!"
                else:
                    valid = True
            else:
                # bounds
                if years > self.max_age:
                    valid = False
                    self.message = "You are too old!"
                elif years < self.min_age:
                    valid = False
                    self.message = "You are too young!"
                else:
                    valid = True
        else:
            self.message = "Invalid date"
            valid = False

        if not valid:
            raise ValidationError(self.message)
