import wtforms as f

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

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

    profile_pic = FileField(
                    validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpg'], 'Images only!')])

    display = ['firstname', 'lastname', 'email',
               'location', 'bonus', 'profile_pic']


class UnregisterForm(FlaskForm):
    """Form created to allowed the users unregistration from the application.
    This form requires the user password in order unregistrate the account.
    """

    password = f.PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    display = ['password']
