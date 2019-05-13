"""
exceptions
~~~~~~~~~~~~~~~~~~~~~

An extension to provide exceptions that can be raised in fire modules and can be caught with a try/except 
"""

class FireException(Exception):
    """Base exception class for fire exceptions

    Ideally speaking, this could be caught to handle any exceptions thrown from this library.
    """
    pass

class PushError(FireException):
    r"""This exception is used when there is an error
    while trying to push to a service like pushbullet or pushover
    """
    def __init__(self, message=None, *args):
        if message is not None:
            super().__init__(message, *args)
        else:
            super().__init__(*args)