from flask import session, redirect, url_for, render_template
from functools import wraps

class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def try_login(username: str, password: str) -> bool:
        """
        Attempts to log in a user by validating their credentials.

        Args:
            username (str): The username provided by the user.
            password (str): The password provided by the user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        # Replace this with a proper user validation mechanism (e.g., database lookup)
        if username == "admin" and password == "admin":
            session['username'] = username
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    @staticmethod
    def try_logout() -> bool:
        """
        Logs out the current user by removing their session data.
        """
        session.pop('username', None)
        return True

    @staticmethod
    def login_required(f):
        """
        Decorator to protect routes that require authentication.

        Args:
            f (function): The function to protect.

        Returns:
            function: The wrapped function that checks authentication.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return render_template("forbidden.html"), 403
            elif session.get('username') != "admin":
                return render_template("forbidden.html"), 403
            return f(*args, **kwargs)  
        return decorated_function