import sqlite3
from app.utils.queries.query_generator import SQLiteQueryBuilder
from app.utils.queries.query_executor import SQLiteQueryExecutor
from app.models.user import User
from app.utils.errors.custom_errors import DatabaseError


class UserRepository:
    def __init__(self, database: sqlite3.Connection):
        self.db = database
        self.query_builder = SQLiteQueryBuilder('users')

    def create_user(self, user: User):
        try:
            with self.db:
                data = user.to_dict()
                result = self.query_builder.insert(data)
                SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])

        except Exception as e:
            raise DatabaseError(str(e))

    def get_user_by_id(self, id: str):
        try:
            with self.db:
                where = {'id': id}
                result = self.query_builder.select(where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                res = cursor.fetchone()
                if res:
                    return User(
                        id=res['id'],
                        name=res['name'],
                        email=res['email'],
                        password=res['password'],
                        phone_no=res['phone_no'],
                        address=res['address'],
                        role=res['role']
                    )
                return None

        except Exception as e:
            raise DatabaseError(str(e))

    def get_user_by_email(self, email: str):
        try:
            with self.db:
                where = {'email': email}
                result = self.query_builder.select(where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                res = cursor.fetchone()
                if res:
                    return User(
                        id=res['id'],
                        name=res['name'],
                        email=res['email'],
                        password=res['password'],
                        phone_no=res['phone_no'],
                        address=res['address'],
                        role=res['role']
                    )
                return None

        except Exception as e:
            raise DatabaseError(str(e))
