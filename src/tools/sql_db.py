import os
from typing import List, Dict, Any
import pyodbc
from dotenv import load_dotenv

load_dotenv()


class SQLDatabaseConnetor:
    def __init__(self) -> None:
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        username = os.getenv("SQL_USERNAME")
        password = os.getenv("SQL_PASSWORD")
        driver = "{ODBC Driver 18 for SQL Server}"
        self.connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
        self.connection = None

    def _connect(self) -> None:
        try:
            self.connection = pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            self.connection = None
            raise Exception(f"Error connecting to database: {e}")

    def _execute_query(self, query: str) -> List[Dict[str, Any]]:
        if not self.connection:
            raise Exception("Database connection is not established.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = {columns[i]: value for i, value in enumerate(row)}
                results.append(row_dict)
            return results
        except Exception as e:
            raise Exception(f"Error executing query: {e}")

    def _close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        else:
            raise Exception("Connection is not established.")


def describe_tables_schema(table_names: str) -> List[Dict[str, Any]]:
    """
    Get the schema of the identified tables
    """
    db = SQLDatabaseConnetor()
    db._connect()
    # split table names by comma and include "" to each table name
    table_names = ",".join([f"'{table.strip()}'" for table in table_names.split(",")])
    query = f"SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ({table_names});"
    results = db._execute_query(query)
    db._close_connection()
    return results


def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return the results
    """
    db = SQLDatabaseConnetor()
    db._connect()
    results = db._execute_query(query)
    db._close_connection()
    return results
