from ledger.engine import processor
from ledger.services.account_history_service import AccountHistoryService


class AccountStatementService:

    @staticmethod
    def generate_statement(account):

        history = AccountHistoryService.get_history(account)

        balance = processor.ledger.balances.get(account, 0)

        running_balance = 0

        statement_entries = []

        for transaction in history:

            if transaction["receiver"] == account:

                running_balance += transaction["amount"]

                statement_entries.append(
                    {
                        "tx_id": transaction["tx_id"],
                        "type": "CREDIT",
                        "amount": transaction["amount"],
                        "balance_after": running_balance,
                    }
                )

            else:

                running_balance -= transaction["amount"]

                statement_entries.append(
                    {
                        "tx_id": transaction["tx_id"],
                        "type": "DEBIT",
                        "amount": transaction["amount"],
                        "balance_after": running_balance,
                    }
                )

        return {
            "account": account,
            "opening_balance": 0,
            "closing_balance": running_balance,
            "transactions": statement_entries,
        }
