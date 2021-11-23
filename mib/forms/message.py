from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import SubmitField, SelectMultipleField, IntegerField,TextAreaField
from wtforms.widgets import HiddenInput

class MessageForm(FlaskForm):
    ''' Message form during writing of message. '''
    message_id_hidden = IntegerField(widget=HiddenInput(), default=-1)
    text_area = TextAreaField('Write your message here!', id='text')
    delivery_date = DateTimeLocalField('Delivery Date', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    users_list = SelectMultipleField('Select recipients', id='users_list')
    save_button = SubmitField('Save')
    send_button = SubmitField('Send')
    display = ['text_area', 'delivery_date', 'users_list']

    ''' Input check: the delivery date chosen isn't before current time. '''
    def validate_on_submit(self):
        if self.delivery_date.data is None or self.delivery_date.data < datetime.now():
            return False
        if (self.send_button.data) and (self.users_list.data == []):
            return False

        return True