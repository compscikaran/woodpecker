import datamodels as dm


def calculate_interest():
    try:
        accounts = dm.db.session.query(dm.Account).all()
        for account in accounts:
            interest_rate = account.aer
            transaction = dm.Transaction()
            transaction.account = account
            transaction.transaction_type = 'Interest'
            transaction.amount = interest_rate*account.balance
            dm.db.session.add(transaction)
            account.balance = (1 + interest_rate)*account.balance

        dm.db.session.commit()
    except (KeyError, TypeError):
        dm.db.session.rollback()
        print('Interest Calculation Failed')


def recheck_balance():
    accounts = dm.db.session.query(dm.Account).all()
    for account in accounts:
        transactions = dm.db.session.query(dm.Transaction) \
            .filter(dm.Transaction.account_no == account.account_no).amount.all()
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == 'Withdrawal':
                balance -= transaction.amount
            else:
                balance += transaction.amount
        if account.balance != balance:
            account.balance = balance
