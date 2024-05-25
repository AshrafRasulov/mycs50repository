import asyncio
import datetime, time
from functools import wraps
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

def SQLite3(str):    
    return sqlite3.connect(str).cursor()


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# baristaloginreq
def barista_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("barista_id") is None:
            return redirect("/employlog")
        return f(*args, **kwargs)

    return decorated_function

# def checkpassword(hashpass, passit):
#     return False if len(hashpass) != 1 or not check_password_hash(passit) else True

def checkpassword(hashpass, passit):
    if len(hashpass[0]["password"]) != 1 or not check_password_hash(passit):
        return True
    return False  



def password_generate(passit):
    return generate_password_hash(passit)



def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def checkphone(phonenum):
    numstr = str(phonenum)
    for i in range(8):
        if(i == 3):
            if numstr[i] != '-':
                return False
        else:
            if not numstr[i].isnumeric():
                return False        
    return True

def withoutlogend(value):
    """Format value as USD."""
    print(value['@':])
    # return f"${value:,.2f}"





           
    
    






    
        
    
    




