from datetime import datetime
from flask import g
from app import db


class Audit(db.Model):
    __abstract__ = True

    audit_created_by = db.Column(db.Integer)
    audit_updated_by = db.Column(db.Integer)
    audit_deleted_by = db.Column(db.Integer)

    audit_created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    audit_updated_on = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    audit_deleted_on = db.Column(db.DateTime)

    audit_is_deleted = db.Column(db.Boolean, default=False)

    def create(self):
        try:
            self.audit_created_by = g.user.id
        except (AttributeError, RuntimeError):
            self.audit_created_by = UserExtends.query.filter_by(name='Maintenance').first().id
        self.audit_is_deleted = False
        self.audit_created_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self):
        try:
            self.audit_updated_by = g.user.id
        except (AttributeError, RuntimeError):
            self.audit_updated_by = UserExtends.query.filter_by(name='Maintenance').first().id
        self.audit_updated_on = datetime.utcnow()
        db.session.commit()

    def delete(self):
        try:
            self.audit_deleted_by = g.user.id
        except (AttributeError, RuntimeError):
            self.audit_deleted_by = UserExtends.query.filter_by(name='Maintenance').first().id
        self.audit_deleted_on = datetime.utcnow()
        self.audit_is_deleted = True
        db.session.commit()
