import sqlite3
from typing import Self


class DatabaseInterface:
    """An interface with GuideDatabase.db."""
    _DATABASE_PATH = "resources/GuideDatabase.db"       # Path from main.py
    _INSTANCE: Self = None

    def __init__(self):
        self.connection: sqlite3.Connection | None = None
        try:
            self.connection = sqlite3.connect(DatabaseInterface._DATABASE_PATH)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise Exception(str(e))

        self.cursor: sqlite3.Cursor | None = None
        if self.connection is not None:
            self.cursor = self.connection.cursor()

    @classmethod
    def get_cursor(cls) -> sqlite3.Cursor:
        """Returns the cursor for the database connection."""
        if DatabaseInterface._INSTANCE is None:
            DatabaseInterface._INSTANCE = DatabaseInterface()

        return DatabaseInterface._INSTANCE.cursor

    @classmethod
    def close_connection(cls) -> None:
        """Closes the database connection."""
        if DatabaseInterface._INSTANCE is None:
            return

        DatabaseInterface._INSTANCE.connection.close()
