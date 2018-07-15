from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

transaction_type = ('Deposit', 'Withdrawal', 'Interest')
transaction_type_enum = Enum(*transaction_type, name='transaction_type_enum')
