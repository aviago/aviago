from werkzeug.security import generate_password_hash, check_password_hash
from .base import Audit
from app import db


class User(Audit):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    username = db.Column(db.String(200))
    email_address = db.Column(db.String(200))
    hash = db.Column(db.String(200))

    last_seen = db.Column(db.DateTime)
    is_suspended = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {0} for Account {1}>'.format(self.username, self.account.name)

    def update_password(self, password):
        self.hash = generate_password_hash(password)
        self.update()
        return

    def validate_password(self, password):
        if check_password_hash(self.hash, password):
            return True
        return False
