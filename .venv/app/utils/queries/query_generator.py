from collections import namedtuple
from typing import Dict,List

class SQLiteQueryBuilder:
    def __init__(self,table):
        self.table = table
        self.Result = namedtuple('Result', ['query', 'values'])

    def insert(self,data: Dict[str,any])-> (str,any):
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        placeholders = ', '.join(['?']* len(data))
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        return self.Result(query,values)

    def select(self, columns: List[str] = ['*'], where: Dict[str, any] = None):
        columns_str = ', '.join(columns)
        query = f"SELECT {columns_str} FROM {self.table}"
        values = tuple()

        if where:
            conditions = [f"{key} = ?" for key in where.keys()]
            values = tuple(where.values())
            conditions_str = ' AND '.join(conditions)
            query += f" WHERE {conditions_str}"
            return self.Result(query,values)

        return self.Result(query,values)

    def update(self, data: Dict[str, any], where: Dict[str, any]) -> str:
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        combined_values = list(data.values())+list(where.values())
        values = tuple(combined_values)
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        query = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
        return self.Result(query,values)

    def delete(self, where: Dict[str, any]) -> str:
        where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
        values = tuple(where.values())
        query = f"DELETE FROM {self.table} WHERE {where_clause}"
        return self.Result(query,values)

