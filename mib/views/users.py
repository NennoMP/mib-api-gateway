import re
from types import MethodDescriptorType
from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import (login_user, login_required, logout_user, current_user)

from mib.forms.user import UserForm, UnregisterForm, UserProfileForm
from mib.rao.user_manager import UserManager
from mib.rao.blacklist_manager import BlacklistManager
from mib.auth.user import User
from mib.decorators import admin_required
from ..utils import image_to_base64

users = Blueprint('users', __name__)


def moderate_action(target_id: int, action: str):
    """
    Utility function used to apply an action to a User object; the possible actions are Ban, Unban, Report, Reject (a report request)
    """
    
    user_id = current_user.id

    # Block
    if action == 'Block':
        response = BlacklistManager.block_user(target_id, user_id)
    # Unblock
    elif action == 'Unblock':
        response = BlacklistManager.unblock_user(target_id, user_id)
    # Ban & Unban
    elif action == 'Ban' or action == "Unban":
        response = UserManager.update_ban_user(target_id, user_id)
    # Report
    elif action == 'Report':
        response = UserManager.report_user(target_id)
    # Reject
    elif action == 'Reject':
        response = UserManager.unreport_user(target_id, user_id)

    return response


@users.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    """This method allows the creation of a new user into the database.

    Returns:
        Redirects the user into his profile page, once he's logged in
    """

    form = UserForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        firstname = form.data['firstname']
        lastname = form.data['lastname']
        date_of_birth = form.data['date_of_birth']
        date_of_birth = date_of_birth.strftime('%Y-%m-%d')
        location = form.data['location']
        response = UserManager.create_user(
            email,
            password,
            firstname,
            lastname,
            date_of_birth,
            location
        )

        json_payload = response.json()
        if response.status_code == 201:
            # Success: user created
            user = response.json()
            to_login = User.build_from_json(user["user"])
            login_user(to_login)
            return redirect(url_for('home.index', id=to_login.id))
        elif response.status_code == 403:
            # Failed: user already exists
            flash(json_payload['message'])
            return render_template('create_user.html', form=form)
        elif response.status_code == 409:
            # Failed: invalid data format
            flash(json_payload['message'])
            return render_template('create_user.html', form=form)
        else:
            flash('Unexpected response from users microservice!')
            return render_template('create_user.html', form=form)
    else:
        for fieldName, errorMessages in form.errors.items():
            for errorMessage in errorMessages:
                flash('The field %s is incorrect: %s' % (fieldName, errorMessage))

    return render_template('create_user.html', form=form)


@users.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    """This method allows:
        - display user profile information
        - update user profile information

    Returns:
        Redirects the user into his profile page
    """
    form = UserProfileForm()
    if request.method == 'GET':
        # Retrieve profile user information
        _user = UserManager.get_profile_by_id(current_user.get_id())
        # Populate user profile form
        form.firstname.data = _user.first_name
        form.lastname.data = _user.last_name
        form.email.data = _user.email
        form.location.data = _user.location
        form.bonus.data = _user.bonus
        form.profile_pic.data = _user.profile_pic

        return render_template('profile.html', form=form, user=_user)
    # POST
    elif request.method == 'POST':
        action = request.form['action']

        # Update profile picture
        if action == "Upload":
            file = form.data['profile_pic']
            format, file = image_to_base64(file)
            if format is None or file is None:
                flash('Error while updating the profile picture, make sure the file is an image')
            else:
                response = UserManager.update_profile_pic(current_user.id, format, file)
                if response.status_code == 202:
                    # Successfull: profile picture updated
                    flash('Edited profile picture')
        # Update profile info
        elif action == 'Save':
            email = form.data['email']
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            location = form.data['location']
            response = UserManager.update_user(
                current_user.get_id(),
                email,
                firstname,
                lastname,
                location
            )
            json_payload = response.json()
            if response.status_code == 200:
                # Successfull: profile info updated
                update_user = None
                update_user = User.build_from_json(json_payload['user'])
                login_user(update_user)
                flash(json_payload['message'])
                return redirect(url_for('users.profile'))
            elif response.status_code == 409:
                # Failed: profile info not updated
                flash(json_payload['message'])
                return redirect(url_for('users.profile'))
        # Update language filter
        elif action == 'toggleFilter':
            response = UserManager.update_language_filter(current_user.id)
            flash('Updated language filter')
            if response.status_code != 202:
                flash("Error while updating the language filter!")

    return redirect(url_for('users.profile'))


@users.route('/users/', methods=['GET', 'POST'])
@login_required
def _users():
    '''Manage the list of users.

        GET: show the list of users with all possible actions: 
                ban (if is admin,) or 
                report an user or
                block or unblock an user

        POST: if <action_todo> = <Report>: report the chosen user
              if <action_todo> = <Block>: block the chosen user
    '''

    if request.method == 'GET':
        is_admin = current_user.is_admin
        users = UserManager.get_users_list()
        response = BlacklistManager.get_blocked_users(current_user.id)

        _blocked_users = response.json()['blocked_users']
        action_template = 'Ban' if is_admin else 'Report'

        return render_template('users.html',
                            users=users,
                            blocked_users=_blocked_users, action=action_template)
    # POST
    # Retrieve action and target user email
    elif request.method == 'POST':
        action_todo = request.form['action']
        target_id = request.form.get('id')
        response = moderate_action(target_id, action_todo) # apply action

        json_payload = response.json()
        if response.status_code == 200 or response.status_code == 202:
            # Successfull
            flash(json_payload['message'])
        else:
            flash('Error while applying moderating action to the user')

        return redirect(url_for('users._users'))


@users.route('/moderation/', methods=['GET', 'POST'])
@login_required
@admin_required
def moderation():
    '''Manage the list of reported and banned users

        GET: show the list of reported and banned users with all possible actions: 
                - reject
                - ban
                - unban

        POST: if <action_todo> = <Reject>: reject the report
              if <action_todo> = <Ban>: ban the reported user
              if <action_todo> = <Unban>: unban the banned user
    '''
    if request.method == 'GET':
        users = UserManager.get_users_list()

        reported_users = [user for user in users if user.is_reported]
        banned_users = [user for user in users if user.is_banned]

        return render_template('moderation.html', reported_users=reported_users, banned_users=banned_users)

    # POST
    # Retrieve action and target user email
    elif request.method == 'POST':
        action_todo = request.form['action']
        target_id = request.form.get('id')
        response = moderate_action(target_id, action_todo) # apply action

        json_payload = response.json()
        if response.status_code == 202:
            # Successfull: reported
            flash(json_payload['message'])
            return redirect(url_for('users.moderation'))
        else:
            flash('Error while applying action to the user')
            return redirect(url_for('users.moderation'))


@users.route('/unregister_user/', methods=['GET', 'POST'])
@login_required
def unregister_user():
    """
        Unregister an user from the application.

        Returns:
            Redirects the user to the homepage, once unregistered (password confirmation requested)
    """
    form = UnregisterForm()
    if form.validate_on_submit():
        password = form.data['password']

        response = UserManager.unregister_user(current_user.id, password)
        if response.status_code == 202:
            # Successfull: unregistered
            logout_user()
            return redirect(url_for('home.index'))
        elif response.status_code == 401:
            # Failed: password does not match
            flash('Password does not match!')
            return render_template('unregister.html', form=form)
        else:
            flash('Error while unregistering the user!')
            return render_template('unregister.html', form=form)

    return render_template('unregister.html', form=form)