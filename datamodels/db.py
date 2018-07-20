from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import datetime

db = SQLAlchemy()


class PrimitiveAttributes:
    timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now(),
        nullable=False
    )
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )


transaction_type = ('Deposit', 'Withdrawal', 'Interest')
transaction_type_enum = Enum(*transaction_type, name='transaction_type_enum')
