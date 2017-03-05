from .base import Audit
from app import db


class User(Audit):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    username = db.Column(db.String(200))
    email_address = db.Column(db.String(200))
    hash = db.Column(db.String(200))

    is_suspended = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {0} for Account {1}>'.format(self.username, self.account.name)
