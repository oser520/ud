import hmac
import random
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

def create_salt(length=16):
    """Generate a random salt value for a password.

    Args:
        length: The lenght of the salt value, with default value of 16.
    """
    if not length:
        raise ValueError('The salt length must be a positive integer')
    ALPHABET = string.ascii_letters + string.digits
    return ''.join(random.choice(ALPHABET) for _ in range(length))

def create_psswd_hash(salt, psswd):
    """Create a hash from a salt and password.

    Args:
        salt: The salt value. Cannot be empty.
        psswd: The password value. Cannot be empty.
    """
    if not salt or not psswd:
        raise ValueError('The salt and password cannot be empty')
    return hmac.new(salt, psswd)

def is_psswd_hash(salt, psswd, hsh):
    """Verify the hash equals the hash fo the salt and password.

    Args:
        salt: The salt value. Cannot be empty.
        psswd: The password value. Cannot be empty.
        hsh: The hash value. Cannot be empty.
    """
    return hsh == hmac.new(salt, psswd)

def username_exists(username):
    """Return true if the username exists, false otherwise.

    Args:
        username: The username value.
    """
    if Account.get_by_id(username):
        return True
    return False
