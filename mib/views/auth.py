from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from mib.forms import LoginForm
from mib.rao.user_manager import UserManager

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login(re=False):
    """Allows the user to log into the system.

    Args:
        re (bool, optional): boolean value that describes whenever
        the user's session is new or needs to be reloaded. Defaults to False.

    Returns:
        Redirects the view to the personal page of the user
    """

    form = LoginForm()
    if form.is_submitted():
        email, password = form.data['email'], form.data['password']
        user, message = UserManager.authenticate_user(email, password)
        if user is None:
            # User is not authenticated or has been banned
            flash(message)
        else:
            # User is authenticated
            login_user(user)
            return redirect(url_for('home.index'))

    return render_template('login.html', form=form, re_login=re)


@auth.route('/relogin')
def re_login():
    """Method that is being called after the user's session is expired."""
    return login(re=True)


@auth.route('/logout')
@login_required
def logout():
    """This method allows the users to log out of the system.

    Returns:
        Redirects the view to the home page
    """
    response = UserManager.logout_user(current_user.email)

    if response.status_code == 200:
        logout_user()
    else:
        flash('Error while logging out the user')
        
    return redirect(url_for('home.index'))

