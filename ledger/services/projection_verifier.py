from ledger.models import AccountProjection


class ProjectionVerifier:

    @staticmethod
    def verify(ledger):

        projection_state = {
            p.account: p.balance for p in AccountProjection.objects.all()
        }

        """
        print("LEDGER:", ledger.balances)
        print("PROJECTION:", projection_state)

        print("LEDGER TYPE:", type(ledger.balances))
        print("PROJECTION TYPE:", type(projection_state))
        """

        return ledger.balances == projection_state
