import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql:///app'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WTF_CSRF_ENABLED = True
#Make this a more secure key
SECRET_KEY = 'secret'
