import bleach
import json
from flask import Blueprint, redirect, render_template, request
from flask_login import current_user

from .auth import login_required
#from ..background import notify
from .utils import get_argument

from mib.forms.message import MessageForm
from mib.rao.user_manager import UserManager
from mib.rao.message_manager import MessageManager
from mib.rao.blacklist_manager import BlacklistManager


messages = Blueprint('messages', __name__)


allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'img', 'video','p', 'div', 'iframe',
                'br', 'span', 'hr', 'src', 'class','font','u']

allowed_attrs = {'*': ['class','style','color'],
                 'a': ['href', 'rel'],
                 'img': ['src', 'alt','data-filename','style']}


@messages.route('/message/<int:message_id>', methods=['GET', 'DELETE'])
@login_required
def message(message_id):
    '''Allows the user to read or delete a specific message by id.

       GET: display the content of a specific message by id (censored if language_filter is ON)
       DELETE:
    '''
    bonus = UserManager.get_bonus(current_user.get_id())

    try: 
        _message = MessageManager.get_message_by_id(current_user.get_id(), message_id)
    except RuntimeError as e:
        message='ERROR contacting message microservice'
        return render_template('error.html', error=message)

    if request.method == 'GET':
        # Get sender and recipient first and last names.
        try:
            sender = UserManager.get_profile_by_id(_message.sender_id)
            recipient = UserManager.get_profile_by_id(_message.recipient_id)
            _message.sender['first_name'], _message.sender['last_name'] = sender.first_name, sender.last_name
            _message.recipient['first_name'], _message.recipient['last_name'] = recipient.first_name, recipient.last_name
        except:
            fake_name = 'Undefined'
            _message.sender['first_name'] = _message.sender['last_name'] = fake_name
            _message.recipient['first_name'] = _message.recipient['last_name'] = fake_name

        return render_template('message.html', bonus=bonus, message=_message)
    
    # DELETE
    try:
        MessageManager.delete_message_by_id(current_user.get_id(), message_id)
        if not _message.is_draft and not _message.is_delivered and bonus > 0:
            bonus -= 1
            UserManager.set_bonus(current_user.get_id(), bonus)
    except:
        message = 'Error in deleting the message'
        return render_template('error.html', error=message)

    return redirect("/mailbox")


@messages.route('/mailbox')
def mailbox():
    '''Manage the user's sent and received messages, aswell as the drafts.
       GET: display the list of drafts, sent and received messages
       POST: perform an action on drafts and messages
             if <message> in <sent_messages> AND <To> button is clicked: display information about the recipient
             if <message> in <received_messages> AND <From> button is clicked: display information about the sender
             if <message> in <draft_messages>
             if <Edit> button is clicked: allows to edit the message text, delivery_date and recipients
             if <View> button is clicked: display the message information
    '''
    id = current_user.get_id()

    # Retrieve all messages of user <id>
    try:
        sent_messages, received_messages, draft_messages, _ = MessageManager.get_all_messages(id)
    except:
        sent_messages = received_messages = draft_messages = []

    try:
        for message in sent_messages:
            recipient = UserManager.get_profile_by_id(message.recipient_id)
            message.recipient['first_name'], message.recipient['last_name'] = recipient.first_name, recipient.last_name
        for message in received_messages:
            sender = UserManager.get_profile_by_id(message.sender_id)
            message.sender['first_name'], message.sender['last_name'] = sender.first_name, sender.last_name
    except:
        fake_name = 'Undefined'
        for message in sent_messages: message.recipient['first_name'] = message.recipient['last_name'] = fake_name
        for message in received_messages: message.sender['first_name'] = message.sender['last_name'] = fake_name

    return render_template('mailbox.html', sent_messages=sent_messages,
                                           received_messages=received_messages,
                                           draft_messages=draft_messages
    )


@messages.route('/create_message', methods=['GET', 'POST'])
@login_required
def create_message():
    '''Manage the creation, reply, and the forward of messages and drafts.
       GET: Creates the form for editing/writing a message.
            If <draft_id> is specified, the corresponding draft is loaded.
            If <forw_id> is specified, the corresponding message is loaded.
            If <reply_id> is specified, the corresponding recipient is loaded.
       POST: Takes the input from the form, creates a new Message object and save it on DB:
             As draft if the <save button> is clicked, as message to send otherwise.
    '''
    form = MessageForm()
    user_id = current_user.get_id()

    if request.method == 'POST':
        error = None

        # Save the choices of recipients.
        form.users_list.choices = form.users_list.data
        if form.validate_on_submit():
            clean_text = bleach.clean(form.text_area.data, tags=allowed_tags, strip=True,
                attributes=allowed_attrs, protocols=['data'], styles='background-color'
            )

            # Save draft.
            if form.save_button.data:
                draft_message = {
                    'text': clean_text,
                    'delivery_date': str(form.delivery_date.data),
                    'sender_id': user_id,
                    'is_draft': True,
                    'recipient_id': 0
                }
                body = json.dumps({'message': draft_message})

                try:
                    # Update old draft.
                    if form.message_id_hidden.data > 0:
                        MessageManager.update_message(user_id, form.message_id_hidden.data, body)

                    # Create new draft.
                    else:
                        MessageManager.create_message(body)
                except:
                    return redirect('/mailbox')

            # Send.
            else:
                blocked_users = BlacklistManager.get_blocked_users(user_id).json()['blocked_users']
                for recipient in form.users_list.data:
                    if recipient in blocked_users:
                        continue

                    message = {
                        'text': clean_text,
                        'delivery_date': str(form.delivery_date.data),
                        'sender_id': user_id,
                        'is_draft': False,
                        'recipient_id': recipient
                    }
                    body = json.dumps({'message': message})

                    try:
                        # Sending a draft.
                        if form.message_id_hidden.data > 0:
                            MessageManager.update_message(user_id, form.message_id_hidden.data, body)
                            form.message_id_hidden.data = -1

                        # Sending a new message.
                        else:
                            MessageManager.create_message(body)
                    except:
                        return redirect('/mailbox')
         
            return redirect('/mailbox')

        else:
            error = '''
                <h3>Wrong data provided!</h3><br/>
                Rules:<br/>  
                    1. Delivery date must be in the future!<br/>
                    2. Recipient field can\'t be empty!
                '''
            # Conflict
            return render_template('/error.html', error=error), 409
    
    # GET
    else:
        form.users_list.choices = [
            (user.get_id(), user.get_email()) for user in UserManager.get_users_list()
        ]
        selected = 0

        draft_id = get_argument(request, 'draft_id', int)
        forw_id = get_argument(request, 'forw_id', int)
        reply_id = get_argument(request, 'reply_id', int)

        if draft_id is not None:
            try:
                message = MessageManager.get_message_by_id(user_id, draft_id)
            except:
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error), 403

            if not message.is_draft:
                error = '<h3>Error!</h3><br/> The message is not a draft!'
                return render_template('/error.html', error=error), 403

            form.message_id_hidden.data = message.id
            form.text_area.data = message.text
            form.delivery_date.data = message.delivery_date

        elif forw_id is not None:
            try:
                message = MessageManager.get_message_by_id(user_id, forw_id)
            except:
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error), 403

            # draft or scheduled message
            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t forward this message!'
                return render_template('/error.html', error=error), 403

            form.text_area.data = f'Forwarded: {message.text}'

        elif reply_id is not None:
            try:
                message = MessageManager.get_message_by_id(user_id,reply_id)
            except:
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error), 403

            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t reply this message!'
                return render_template('/error.html', error=error), 403

            form.text_area.data = 'Reply: '
            selected = message.sender_id

        return render_template('create_message.html', form=form, selected=selected)


@messages.route('/calendar')
@login_required
def calendar():
    '''Display a calendar with the messages scheduled to be sent in each day.

       GET: show the calendar template
    '''
    id = current_user.get_id()

    # Retrieve all messages of user <id>
    try:
        sent_messages, received_messages, _, _ = MessageManager.get_all_messages(id)
    except:
        sent_messages = received_messages = []

    try:
        for message in sent_messages:
            recipient = UserManager.get_profile_by_id(message.recipient_id)
            message.recipient['first_name'], message.recipient['last_name'] = recipient.first_name, recipient.last_name
        for message in received_messages:
            sender = UserManager.get_profile_by_id(message.sender_id)
            message.sender['first_name'], message.sender['last_name'] = sender.first_name, sender.last_name
    except:
        fake_name = 'Undefined'
        for message in sent_messages: message.recipient['first_name'] = message.recipient['last_name'] = fake_name
        for message in received_messages: message.sender['first_name'] = message.sender['last_name'] = fake_name


    sent_messages = [
        {
            'time': str(message.delivery_date),
            'cls': 'bg-orange-alt',
            'desc': f'To {message.recipient["first_name"]} {message.recipient["last_name"]}',
            'msg_id': message.id
        } for message in sent_messages
    ]

    received_messages = [
        {
            'time': str(message.delivery_date),
            'cls': 'bg-sky-blue-alt',
            'desc': f'From {message.sender["first_name"]} {message.sender["last_name"]}',
            'msg_id': message.id
        } for message in received_messages
    ]

    return render_template(
        'calendar.html',
        data=json.dumps(sent_messages + received_messages),
    )


@messages.route('/scheduled')
@login_required
def scheduled():
    '''Display the list of user's messages scheduled to be sent.

       GET: show the list of messages
    '''
    id = current_user.get_id()
    try:
        _, _, _, scheduled_messages = MessageManager.get_all_messages(id)
    except:
        scheduled_messages = []

    try:
        for message in scheduled_messages:
            recipient = UserManager.get_profile_by_id(message.recipient_id)
            message.recipient['first_name'], message.recipient['last_name'] = recipient.first_name, recipient.last_name
    except:
        fake_name = 'Undefined'
        for message in scheduled_messages: message.recipient['first_name'] = message.recipient['last_name'] = fake_name

    return render_template('schedule.html', scheduled_messages=scheduled_messages)
