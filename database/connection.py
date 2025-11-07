import pyodbc
from config import DB_CONNECTION_STRING

def get_connection():
    return pyodbc.connect(DB_CONNECTION_STRING)
