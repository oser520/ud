import re
import string

def process_username(username):
    """Converts the username to lowercase, and returns a MatchObject if the
    username is valid.

    The username must begin with an alpha character, must be at least 4
    characters long, and it may only contain alphanumeric characters, dots, and
    underscores.

    Args:
        username: The username to validate.
    """
    username = username.strip().lower()
    return re.match(r'[a-z][a-z\d._]{3,35}$', username)

def process_password(password):
    """Returns true if the password is valid, false otherwise.

    The password is valid if it contains between 6 and 35 characters, at least
    one number, at least one alpha character, and no whitespace.

    Args:
        password: The password to validate.
    """
    m = re.match(r'\S{6,35}$', password)
    if not m: return False
    for c in password:
        if c in string.ascii_letters: break
    else:
        return False
    for c in password:
        if c in string.digits: return True
    return False
