import re

def process_username(username):
    """Converts the username to lowercase, and returns a MatchObject if the
    username is valid.

    The username must begin with an alpha character, must be at least 4
    characters long, and it may only contain alphanumeric characters, dots, and
    underscores.

    Args:
        username: The username to validate.
    """
    return re.search(r'^[a-z][a-z\d._]{3,35}', username.lower())
