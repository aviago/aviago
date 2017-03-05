from app import manager, app, db
from app.models.user import User
from app.models.account import Account
from urllib.parse import unquote
import random
import hashlib


def generate_api_key():
    return hashlib.sha224(str(random.getrandbits(256))).hexdigest()


@manager.command
def seed_db():
    acct = Account.query.filter_by(name='Internal').first()
    if acct:
        quit('DB contents already exist, Cannot seed')

    accounts = [
        {'name': 'Internal', 'is_suspended': False},
    ]

    # Internal Users
    internal_users = [
        {'username': 'QueueRunner', 'email_address': 'queuerunner@exile-tek.com', 'is_admin': True},
        {'username': 'Admin', 'email_address': 'admin@exile-tek.com', 'is_admin': True},
        {'username': 'Maintenance', 'email_address': 'maintenance@exile-tek.com', 'is_admin': True}
    ]

    # Reserved Users
    for i in range(1, 10):
        internal_users.append({
            'username': 'Reserved {0}'.format(i),
            'email_address': 'Reserved {0}'.format(i),
            'is_admin': False
        })

    # Add the accounts
    for item in accounts:
        account = Account()
        for key, value in item.items():
            setattr(account, key, value)
        db.session.add(account)
    db.session.commit()

    internal_account = Account.query.filter_by(name='Internal').first()
    for item in internal_users:
        item['account_id'] = internal_account.id
        user = User()
        for key, value in item.items():
            setattr(user, key, value)
        db.session.add(user)
    db.session.commit()

    print('DB seeded successfully')
    return


@manager.command
def list_routes():
    """Lists all routes known to this application"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)
    for line in sorted(output):
        print(line)
