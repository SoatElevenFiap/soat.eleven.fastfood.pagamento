from abc import ABC


class RepositoryAdapter(ABC):
    def __init__(self, table: str) -> None:
        self.table = table
