import sqlite3
from app.utils.queries.query_generator import SQLiteQueryBuilder
from app.utils.queries.query_executor import SQLiteQueryExecutor
from app.models.ngo import NGO
from app.utils.errors.custom_errors import DatabaseError, NotExistsError


class NGORepository:
    def __init__(self,db: sqlite3.Connection):
        self.db = db
        self.query_builder = SQLiteQueryBuilder('ngos')

    def get_all_ngos(self):
        try:
            with self.db:
                result = self.query_builder.select()
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                rows = cursor.fetchall()
                ngos = []
                if rows:
                    for row in rows:
                        ngos.append(NGO(
                            id = row['id'],
                            phone_no=row['phone_no'],
                            name=row['name'],
                            email=row['email'],
                            details=row['details'],
                            address=row['address']
                        ))
                return ngos

        except Exception as e:
            raise DatabaseError(str(e))

    def get_ngo_by_id(self,id: str):
        try:
            with self.db:
                where = {'id':id}
                result = self.query_builder.select(where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                row = cursor.fetchone()
                if row is None:
                    raise NotExistsError("Ngo Id does not exist")
                if row:
                    return NGO(
                        id=row['id'],
                        phone_no=row['phone_no'],
                        name=row['name'],
                        email=row['email'],
                        details=row['details'],
                        address=row['address']
                    )
                return None

        except Exception as e:
            raise DatabaseError(str(e))

    def get_ngo_by_email(self,email: str):
        try:
            with self.db:
                where = {'email':email}
                result = self.query_builder.select(where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                row = cursor.fetchone()
                if row:
                    return NGO(
                        id=row['id'],
                        phone_no=row['phone_no'],
                        name=row['name'],
                        email=row['email'],
                        details=row['details'],
                        address=row['address']
                    )
                return None

        except Exception as e:
            raise DatabaseError(str(e))

    def create_ngo(self,ngo: NGO):
        try:
            with self.db:
                data = ngo.to_dict()
                result = self.query_builder.insert(data)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])

        except Exception as e:
            raise DatabaseError(str(e))

    def delete_ngo_by_id(self,id: str):
        try:
            with self.db:
                where = {'id':id}
                result = self.query_builder.delete(where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                if cursor.rowcount == 0:
                    raise NotExistsError("Ngo Id does not exist")

        except Exception as e:
            raise DatabaseError(str(e))

    def update_ngo_by_id(self,ngo:NGO):
        try:
            with self.db:
                col = {
                    'name': ngo.name,
                    'address': ngo.address,
                    'email': ngo.email,
                    'details': ngo.details,
                    'phone_no': ngo.phone_no
                }
                where = {'id': ngo.id}
                result = self.query_builder.update(data=col,where=where)
                cursor = SQLiteQueryExecutor.execute_query(self.db, result[0], result[1])
                if cursor.rowcount == 0:
                    raise NotExistsError("Ngo Id does not exist")

        except Exception as e:
            raise DatabaseError(str(e))
