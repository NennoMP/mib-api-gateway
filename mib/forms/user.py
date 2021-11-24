import wtforms as f
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email

from mib.validators.age import PasswordValidator, AgeValidator


class UserForm(FlaskForm):
    """Form created to allow the customers sign up to the application.
    This form requires all the personal information, in order to create the account.
    """

    email = EmailField(
        'Email',
        validators=[DataRequired(), Email(check_deliverability=True)]
    )

    firstname = f.StringField(
        'Firstname',
        validators=[DataRequired()]
    )

    lastname = f.StringField(
        'Lastname',
        validators=[DataRequired()]
    )

    password = f.PasswordField(
        'Password',
        validators=[DataRequired(), PasswordValidator()]
    )

    date_of_birth = DateField(
        'Birthday',
        validators=[AgeValidator(min_age=18)]
    )

    location = f.StringField(
        'Location', 
        validators=[DataRequired()]
    )

    ''' Input check: email format, valid password and valid birth date. '''
    '''    def validate_on_submit(self):
        result = super(UserForm, self).validate()

        # check email format is valid
        if not allowed_email(self.email.data):
            return [False, 'invalid email format']
        # check password requirements
        if not allowed_password(self.password.data):
            return [False, 'password must be of length between 5 and 25 and contain at least one upper case, one number and one special character!']
        # check birth date is in the past
        if not allowed_birth_date(self.date_of_birth.data):
            return [False, 'date of birth must be in the past']

        return [result, '']
'''
    display = ['email', 'firstname', 'lastname', 'password',
               'date_of_birth', 'location']


class UserProfileForm(FlaskForm):
    """Form created to allow the customers sign up to the application.
    This form requires all the personal information, in order to create the account.
    """

    email = EmailField(
        'Email',
        render_kw={"readonly": True},
        validators=[DataRequired(), Email(check_deliverability=True)]
    )

    firstname = f.StringField(
        'Firstname',
        render_kw={"readonly": True},
        validators=[DataRequired()]
    )

    lastname = f.StringField(
        'Lastname',
        render_kw={"readonly": True},
        validators=[DataRequired()]
    )


    location = f.StringField(
        'Location',
        render_kw={"readonly": True},
        validators=[DataRequired()]
    )
    
    bonus = f.StringField(
        'Bonus',
        render_kw={"readonly": True},
        validators=[DataRequired()]
    )
    display = ['firstname', 'lastname', 'email',
               'location']



class UnregisterForm(FlaskForm):
    """Form created to allowed the users unregistration from the application.
    This form requires the user password in order unregistrate the account.
    """

    password = f.PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    display = ['password']
