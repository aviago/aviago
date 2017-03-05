from .base import Audit
from app import db, app


class Account(Audit):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    is_suspended = db.Column(db.Boolean, default=False)
    credit_limit = db.Column(db.Integer, default=app.config['DEFAULT_CREDIT_LIMIT'])
    credit_balance = db.Column(db.Integer, default=0)

    users = db.relationship('User', backref='account', lazy='dynamic')

    def __repr__(self):
        return '<Account {0}>'.format(self.name)
