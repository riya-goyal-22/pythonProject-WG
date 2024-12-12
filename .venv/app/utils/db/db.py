import sqlite3
import threading
import app.config.config as config

#singleton db connection
class DB_Instance:
    _connection = None
    _lock = threading.Lock()

    @classmethod
    def get_connection(cls)-> sqlite3.Connection:
        if cls._connection is None:
            with cls._lock:
                if cls._connection is None:
                    cls._connection = sqlite3.connect(config.DB_ADDRESS,check_same_thread=False)
                    cls._connection.row_factory = sqlite3.Row

        return cls._connection