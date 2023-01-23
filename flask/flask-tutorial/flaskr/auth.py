import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#A Blueprint is a way to organize a group of related views and other code. 
#Rather than registering views and other code directly with an application, 
#they are registered with a blueprint.






@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('register.html') 












@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


#session is a dict that stores data across requests

#Uses of Session
#Remember each user when they log in

#The data in the Session is stored on the top of cookies and signed by the server cryptographically.

#Al comienzo de cada solicitud, si un usuario ha iniciado sesión, 
#su información debe cargarse y estar disponible para otras vistas.
#esto ultimo se lograria a traves de una session en Flask.







@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
#bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.





@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


#aca lo que se hace es limpiar la session, es decir, se borra el usuario que esta guardado
# para cada request que ocurra. Luego de que corra esta view, el load_logged_in_user correra y 
# no guardara ningun usuario en la variable user_id (ya que el mismo fue eliminado de la session).





def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


#ENDPOINTS AND URLS
#The url_for() function generates the URL to a view based on a name and arguments. 
#The name associated with a view is also called the endpoint, 
#and by default it’s the same as the name of the view function.


#para el caso del uso de BluePrints, el nombre del endpoint cambia:
# When using a blueprint, the name of the blueprint is prepended to the name of the function, 
# so the endpoint for the login function you wrote above is 'auth.login' 
# because you added it to the 'auth' blueprint.









#TEMPLATES
# Templates are files that contain static data as well as placeholders for dynamic data.
# A template is rendered with specific data to produce a final document. 
# Flask uses the Jinja template library to render templates.

#Flask uses the Jinja template library to render templates.
#Special delimiters are used to distinguish Jinja syntax from the static data in the template. 
#Anything between {{ and }} is an expression that will be output to the final document. 
#{% and %} denotes a control flow statement like if and for.

