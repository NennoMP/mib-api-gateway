import bleach
import json
from flask import Blueprint, redirect, render_template, request, abort
from flask.json import jsonify
from flask_login import current_user

#from ..access import Access
#from ..auth import login_required
#from ..background import notify
from .utils import get_argument

#from monolith.database import User, Message, BlackList, db
from mib.forms.message import MessageForm
from mib.rao.user_manager import UserManager
from mib.rao.message_manager import MessageManager

messages= Blueprint('messages', __name__)

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'img', 'video','p', 'div', 'iframe',
                'br', 'span', 'hr', 'src', 'class','font','u']

allowed_attrs = {'*': ['class','style','color'],
                 'a': ['href', 'rel'],
                 'img': ['src', 'alt','data-filename','style']}


@messages.route('/message/<int:message_id>', methods=['GET', 'DELETE'])
def message(message_id):
    '''Allows the user to read or delete a specific message by id.

       GET: display the content of a specific message by id (censored if language_filter is ON)
       DELETE: TODO
    '''
    if request.method == 'GET':

        # TODO: try except
        _message = MessageManager.get_message_by_id(current_user.get_id(), message_id)
        bonus = UserManager.get_profile_by_id(current_user.get_id()).bonus

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
    # TODO: check user bonus > 0
    MessageManager.delete_message_by_id(current_user.get_id(), message_id)
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
    # Retrieve user <id>
    id = current_user.get_id()

    # Retrieve sent messages of user <id>
    sent_messages, received_messages, draft_messages = MessageManager.get_all_messages(id)

    # TODO: get real names
    try:
        for message in sent_messages:
            recipient = UserManager.get_user_by_id(message.recipient_id)
            message.recipient['first_name'], message.recipient['last_name'] = recipient.first_name, recipient.last_name
        for message in received_messages:
            sender = UserManager.get_user_by_id(message.sender_id)
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
#@login_required
def create_message():
    #return
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
                # Update old draft.
                if form.message_id_hidden.data > 0:
                    updated_message = {
                        'text': clean_text,
                        'delivery_date': str(form.delivery_date.data),
                        'is_draft': True,
                        'recipient_id': 0
                    }
                    body = json.dumps({'message': updated_message}) 
                    MessageManager.update_message(user_id, form.message_id_hidden.data, body)  

                # Create new draft.
                else:                    
                    new_message = {
                        'text': clean_text,
                        'delivery_date': str(form.delivery_date.data),
                        'sender_id': user_id,
                        'is_draft': True,
                        'recipient_id': 0
                    }
                    body = json.dumps({'message': new_message}) 
                    MessageManager.create_message(body)

            # Send.
            else:
                #TODO: get from blacklist blocked user list per il check
                for recipient in form.users_list.data:
                    #if is_blocked(recipient):
                    #    continue

                    # send new message from draft to first recipient
                    #TODO: get message from messages where message_id= form.message_id_hidden.data
                    #TODO: post/put to messages json{con i dati seguenti} 
                    
                    if form.message_id_hidden.data > 0:
                        updated_message = {
                            'text': clean_text,
                            'delivery_date': str(form.delivery_date.data),
                            'is_draft': False,
                            'recipient_id': recipient
                        }
                        body = json.dumps({'message': updated_message}) 
                        MessageManager.update_message(user_id, form.message_id_hidden.data, body)  
                        form.message_id_hidden.data = -1

                    else:
                        #TODO: post/put to messages json{con i dati seguenti} 
                        # send new message [from draft] to [other] recipients

                        new_message = {
                            'text': clean_text,
                            'delivery_date': str(form.delivery_date.data),
                            'sender_id': user_id,
                            'is_draft': False,
                            'recipient_id': recipient
                        }
                        body = json.dumps({'message': new_message})          
                        MessageManager.create_message(body)
         
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
        selected = None

        draft_id = get_argument(request, 'draft_id', int)
        forw_id = get_argument(request, 'forw_id', int)
        reply_id = get_argument(request, 'reply_id', int)

        if draft_id is not None:

            try:
                message = MessageManager.get_message_by_id(user_id,draft_id)
            except:
                #TODO: gestione dell'internal server error microservizio
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error),403

            if not message.is_draft:
                error = '<h3>Error!</h3><br/> The message is not a draft!'
                # Forbidden
                return render_template('/error.html', error=error),403

            form.message_id_hidden.data = message.id
            form.text_area.data = message.text
            form.delivery_date.data = message.delivery_date

        elif forw_id is not None:
            #TODO: get a message per ottenere il draft nella forma json per popolare l'oggetto message
            #TODO: gestire mancata retrieve
            try:
                message = MessageManager.get_message_by_id(user_id,forw_id)
            except:
                #TODO: gestione dell'internal server error microservizio
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error),403


            # draft or scheduled message
            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t forward this message!'
                # Forbidden
                return render_template('/error.html', error=error), 403

            form.text_area.data = f'Forwarded: {message.text}'

        elif reply_id is not None:
            #TODO: get a message per ottenere il draft nella forma json per popolare l'oggetto message
            #TODO: gestire mancata retrieve
            try:
                message = MessageManager.get_message_by_id(user_id,reply_id)
            except:
                #TODO: gestione dell'internal server error microservizio
                error = '<h3>Error!</h3><br/> The message is not correct!'
                return render_template('/error.html', error=error),403

            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t reply this message!'

                # Forbidden
                return render_template('/error.html', error=error), 403

            form.text_area.data = 'Reply: '
            selected = message.sender_id

        return render_template('create_message.html', form=form, selected=selected)
