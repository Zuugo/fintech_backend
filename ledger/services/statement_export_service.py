import csv
from io import StringIO

from ledger.services.account_statement_service import AccountStatementService


class StatementExportService:

    @staticmethod
    def export_csv(account):

        statement = AccountStatementService.generate_statement(account)

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow(["account", statement["account"]])

        writer.writerow(["opening_balance", statement["opening_balance"]])

        writer.writerow(["closing_balance", statement["closing_balance"]])

        writer.writerow([])

        writer.writerow(
            [
                "tx_id",
                "type",
                "amount",
                "balance_after",
            ]
        )

        for transaction in statement["transactions"]:

            writer.writerow(
                [
                    transaction["tx_id"],
                    transaction["type"],
                    transaction["amount"],
                    transaction["balance_after"],
                ]
            )

        return output.getvalue()
