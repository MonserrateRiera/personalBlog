from flask import session, redirect, url_for, render_template
from functools import wraps


def tryLogin(username:str, password:str) -> str:
    if username == "admin" and password == "admin":

        session['username'] = username
        print("login successful")
        return True
    else:
        return False
    
def tryLogout():
    session.pop('username', None)

def loginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return render_template("forbidden.html"), 403
        elif session.get('username') != "admin":
            return render_template("forbidden.html"), 403
        return f(*args, **kwargs)  # si está logueado, ejecuta la función original
    return decorated_function  # devuelve la nueva función "protegida"