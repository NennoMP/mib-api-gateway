from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from mib.forms.user import UserForm, UnregisterForm
from mib.rao.user_manager import UserManager
from mib.auth.user import User

users = Blueprint('users', __name__)


@users.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    """This method allows the creation of a new user into the database

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


        if response.status_code == 201:
            # in this case the request is ok!
            user = response.json()
            to_login = User.build_from_json(user["user"])
            login_user(to_login)
            return redirect(url_for('home.index', id=to_login.id))
        elif response.status_code == 200:
            # user already exists
            flash('User already exists!')
            return render_template('create_user.html', form=form)
        else:
            flash('Unexpected response from users microservice!')
            return render_template('create_user.html', form=form)
    else:
        for fieldName, errorMessages in form.errors.items():
            for errorMessage in errorMessages:
                flash('The field %s is incorrect: %s' % (fieldName, errorMessage))

    return render_template('create_user.html', form=form)


@users.route('/unregister_user/', methods=['GET', 'POST'])
@login_required
def unregister_user():
    '''
        Unregister an user from the application

        Returns:
            Redirects the user to the homepage, once unregistered (password confirmation requested)
    '''

    form = UnregisterForm()

    if form.validate_on_submit():
        password = form.data['password']

        response = UserManager.unregister_user(current_user.id, password)
        if response.status_code == 202:
            # response is ok
            logout_user()
            return redirect(url_for('home.index'))
        elif response.status_code == 401:
            # password does not match
            flash('Password does not match!')
            return render_template('unregister.html', form=form)
        else:
            flash('Error while unregistering the user!')
            return render_template('unregister.html', form=form)

    return render_template('unregister.html', form=form)

'''@users.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """

    response = UserManager.delete_user(id)
    if response.status_code != 202:
        flash("Error while deleting the user")
        return redirect(url_for('auth.profile', id=id))
        
    return redirect(url_for('home.index'))'''

