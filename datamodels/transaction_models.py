from .db import db, transaction_type_enum
import datetime


class Transaction(db.Model):
    transaction_id = db.Column(
        db.Integer,
        primary_key=True
    )
    account_no = db.Column(
        db.Integer,
        db.ForeignKey('account.account_no'),
        nullable=False,
    )
    amount = db.Column(
        db.Float,
    )
    transaction_type = db.Column(
        transaction_type_enum
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )
    account = db.relationship('Account', backref='transaction',
                              uselist=False, foreign_keys=[account_no])
