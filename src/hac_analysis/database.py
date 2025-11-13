# database contains functions to manage connecting to and querying the HAC database

import pyodbc
from datetime import datetime

# TODO: Look into converting pyodbc.Row to a pandas.DataFrame


def handle_variant(var):
    if type(var) is bytes:
        # Database column with variant type contains numeric types
        # (i.e., floats and ints) and the integer values are read
        # as bytes by the database engine.
        var = int.from_bytes(var, "little")
    return var


def connect(db_info: dict) -> pyodbc.Connection:
    # NOTE: Use of `Trusted_Connection` may only work on Windows
    conn = pyodbc.connect(
        driver=db_info["driver"],
        server=db_info["location"],
        database=db_info["current_db"],
        Trusted_Connection=db_info["trusted_connection"],
    )
    conn.add_output_converter(-16, handle_variant)

    return conn


def disconnect(conn: pyodbc.Connection):
    conn.close()


def query(conn: pyodbc.Connection, sql: str, params: tuple):
    cursor = conn.cursor()
    cursor.execute(sql, params)

    return cursor.fetchall()


# NOTE: Because the expectation is for the HAC database to be running locally
# and not connecting to a centralized database, f-strings are used for poducing
# the SQL query despite the potential for SQL injection with malicious input
# to the functions. This is mitigated some by parameterizing the timestamp
# conditions.


def query_tag_list(
    conn: pyodbc.Connection, table_info: dict, start_time: datetime, end_time: datetime
) -> list[pyodbc.Row]:
    tag = table_info["tags"]
    db = table_info["database"]
    tab = table_info["name"]
    sql = f"SELECT DISTINCT {tag} FROM {db}.dbo.{tab} WHERE TagTimestamp >= ? AND TagTimestamp <= ?"
    data = query(conn, sql, (start_time, end_time))
    return data


def query_instrument_data(
    conn: pyodbc.Connection, table_info: dict, start_time: datetime, end_time: datetime
) -> list[pyodbc.Row]:
    tag = table_info["tags"]
    db = table_info["database"]
    tab = table_info["name"]
    sql = f"SELECT TagTimestamp, {tag}, TagValue FROM {db}.dbo.{tab} WHERE TagTimestamp >= ? AND TagTimestamp <= ?"
    data = query(conn, sql, (start_time, end_time))
    return data
