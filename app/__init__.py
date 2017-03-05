from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Server, Manager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
import logging
from logging.handlers import SMTPHandler

release_version = 'v1.5.3'
release_date = '03/03/2017'

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0", port=app.config['PORT']))

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

if not app.debug and app.config['SEND_FEEDBACK']:
    ADMINS = ['dev@exile-tek.com']
    mail_handler = SMTPHandler(app.config['SMTP_HOST'],
                               'Havana',
                               'dev@exile-tek.com', 'Havana Code Failure',
                               credentials=(app.config['SMTP_USERNAME'], app.config['SMTP_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


def do_imports(flask_app):
    from .imports import import_routes
    import_routes(flask_app)

do_imports(app)
from app.commands import *
