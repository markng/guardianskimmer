SECRET_KEY = 'Make up a secret key to go here (and no sharing).'
GUARDIAN_API_KEY = 'Insert your guardian api key here.'

CACHE_BACKEND = 'dummy:///' # you'll want to change this if you don't want to hit your API limit quickly
# we're not actually using a database here, so none of this really matters anyway
DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

