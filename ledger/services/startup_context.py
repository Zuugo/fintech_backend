from dataclasses import dataclass


@dataclass
class StartupContext:

    journal_position: int = 0

    replayed_transactions: int = 0

    snapshot_load: bool = False

    balances: dict | None = None

    nonces: dict | None = None

    last_hash: str | None = None
