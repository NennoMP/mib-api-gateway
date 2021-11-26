import datetime
from wtforms.validators import ValidationError

# GLOBALS
SPECIAL_CHARACTERS = '@#$%&*-_/'


class PasswordValidator(Exception):

    def __init__(self):
        """Password Validation."""

        self.message = ""

    def __call__(self, form, field):
        password = field.data
        valid = True

        """ TODO: we could remove from yaml and put it here
            # check length
        if len(password) < 5 or len(password) > 25:
            return False"""

        # check if upper cases
        if not any(el.isupper() for el in password):
            valid = False
            self.message = 'at least one upper case!'
        # check if numbers
        elif not any(el.isdigit() for el in password):
            valid = False
            self.message = 'at least one digit!'
        # check if special characters
        elif not any(el in SPECIAL_CHARACTERS for el in password):
            valid = False
            self.message = 'at least one special character!'

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
