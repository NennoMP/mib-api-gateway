#import bleach
import json
from flask import Blueprint, redirect, render_template, request, abort
#from flask_login import current_user

#from ..access import Access
#from ..auth import login_required
#from ..background import notify
#from ..utils import get_argument

#from monolith.database import User, Message, BlackList, db
#from mib.forms import MessageForm

messages= Blueprint('messages', __name__)

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'img', 'video','p', 'div', 'iframe',
                'br', 'span', 'hr', 'src', 'class','font','u']

allowed_attrs = {'*': ['class','style','color'],
                 'a': ['href', 'rel'],
                 'img': ['src', 'alt','data-filename','style']}


@messages.route('/create_message', methods=['GET', 'POST'])
#@login_required
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
                # Update old draft.
                if form.message_id_hidden.data > 0:
                    #TODO: get message from messages where message_id= form.message_id_hidden.data
                    #TODO: post/put to messages json{con i dati seguenti}  
                    message = retrieve_message(form.message_id_hidden.data)
                    message.text = clean_text
                    message.delivery_date = form.delivery_date.data
                    message.sender_id = user_id
                    message.recipient_id = 0


                # Create new draft.
                else:
                    #TODO: post/put to messages json{con i dati seguenti} 
                    new_message = Message()
                    new_message.text = clean_text
                    new_message.delivery_date = form.delivery_date.data
                    new_message.sender_id = user_id
                    new_message.recipient_id = 0

            # Send.
            else:
                #TODO: get from blacklist blocked user list per il check
                for recipient in form.users_list.data:
                    if is_blocked(recipient):
                        continue

                    # send new message from draft to first recipient
                    #TODO: get message from messages where message_id= form.message_id_hidden.data
                    #TODO: post/put to messages json{con i dati seguenti} 
                    if form.message_id_hidden.data > 0:
                        message = retrieve_message(form.message_id_hidden.data)
                        message.is_draft = False
                        message.text = clean_text
                        message.delivery_date = form.delivery_date.data
                        message.sender_id = user_id
                        message.recipient_id = recipient
                        form.message_id_hidden.data = -1
                    else:
                        #TODO: post/put to messages json{con i dati seguenti} 
                        # send new message [from draft] to [other] recipients
                        new_message = Message()
                        new_message.text = clean_text
                        new_message.delivery_date = form.delivery_date.data
                        new_message.is_draft = False
                        new_message.sender_id = user_id
                        new_message.recipient_id = recipient
            #TODO: mailbox page sull'APIgateway per la retrieve dei messaggi "sent, received,draft" 
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
        #TODO: get from users la users_list per popolare il form
        form.users_list.choices = [
            #TODO: popolare choices con lista users
            (user.get_id(), user.get_email()) for user in get_users()
        ]
        selected = None

        draft_id = get_argument(request, 'draft_id', int)
        forw_id = get_argument(request, 'forw_id', int)
        reply_id = get_argument(request, 'reply_id', int)

        if draft_id is not None:
            #TODO: get a message per ottenere il draft nella forma json per popolare l'oggetto message
            #TODO: gestire mancata retrieve
            message = retrieve_message(draft_id)
            #TODO: decidere come gestire questa funzione
            is_sender_or_recipient(message, user_id)

            if not message.is_draft:
                error = '<h3>Error!</h3><br/> The message is not a draft!'
                # Forbidden
                return render_template('/error.html', error=error),403

            form.message_id_hidden.data = message.get_id()
            form.text_area.data = message.get_text()
            form.delivery_date.data = message.get_delivery_date()

        elif forw_id is not None:
            #TODO: get a message per ottenere il draft nella forma json per popolare l'oggetto message
            #TODO: gestire mancata retrieve
            message = retrieve_message(forw_id)
            is_sender_or_recipient(message, user_id)

            # draft or scheduled message
            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t forward this message!'

                # Forbidden
                return render_template('/error.html', error=error), 403

            form.text_area.data = f'Forwarded: {message.get_text()}'

        elif reply_id is not None:
            #TODO: get a message per ottenere il draft nella forma json per popolare l'oggetto message
            #TODO: gestire mancata retrieve
            message = retrieve_message(reply_id)
            is_sender_or_recipient(message, user_id)

            if message.is_draft or not message.is_delivered:
                error = '<h3>Error!</h3><br/> you can\'t reply this message!'

                # Forbidden
                return render_template('/error.html', error=error), 403

            form.text_area.data = 'Reply: '
            selected = message.get_sender()

        return render_template('create_message.html', form=form, selected=selected)