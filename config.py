import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'secret_key'

TITLE = "Merchandise Tracker"

# Mail Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
# MAIL_DEBUG = app.debug
MAIL_USERNAME = 'account@gmail.com'
MAIL_PASSWORD = 'gmailPassword'
MAIL_DEFAULT_SENDER = "account@gmail.com"
# MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND = app.testing
MAIL_ASCII_ATTACHMENTS = False

# User API URL
USER_PORT = "8085"
USER_HOST = "localhost"
USER_TEMPLATE = "http://{}:{}"
USER_URL = USER_TEMPLATE.format(USER_HOST, USER_PORT)

# Items API URL
ITEMS_PORT = "8090"
ITEMS_HOST = "localhost"
ITEMS_TEMPLATE = "http://{}:{}"
ITEMS_URL = ITEMS_TEMPLATE.format(ITEMS_HOST, ITEMS_PORT)

del os

if __name__ == '__main__':
    print(USER_URL)
