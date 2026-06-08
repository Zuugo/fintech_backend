from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from ledger.services.account_statement_service import AccountStatementService


class PDFStatementService:

    @staticmethod
    def generate_pdf(account):

        statement = AccountStatementService.generate_statement(account)

        buffer = BytesIO()

        document = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                f"Account Statement - {account}",
                styles["Title"],
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph(
                f"Opening Balance: " f"{statement['opening_balance']}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"Closing Balance: " f"{statement['closing_balance']}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 20))

        data = [
            ["TRANSACTION ID", "TYPE", "AMOUNT", "BALANCE AFTER"],
        ]

        for transaction in statement["transactions"]:

            data.append(
                [
                    transaction["tx_id"],
                    transaction["type"],
                    str(transaction["amount"]),
                    str(transaction["balance_after"]),
                ]
            )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )

        elements.append(table)

        document.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf
