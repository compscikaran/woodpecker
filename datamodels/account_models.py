from .db import db


class Account(db.Model):
    account_no = db.Column(
        db.Integer,
        primary_key=True
    )
    balance = db.Column(
        db.Float,
        default=0,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        nullable=False
    )
    user = db.relationship('User', backref='account',
                           uselist=False, foreign_keys=[user_id])


class User(db.Model):
    user_id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )
