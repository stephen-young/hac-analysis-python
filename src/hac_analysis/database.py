# database contains functions to manage connecting to and querying the HAC database

import pyodbc
from datetime import datetime
from pandas import read_sql_query, DataFrame
from sqlalchemy import create_engine, Connection
from sqlalchemy.engine import URL


def handle_variant(var):
    if type(var) is bytes:
        # Database column with variant type contains numeric types
        # (i.e., floats and ints) and the integer values are read
        # as bytes by the database engine.
        var = int.from_bytes(var, "little")
    return var


def connect(db_info: dict) -> Connection:
    # NOTE: Use of `Trusted_Connection` may only work on Windows
    connection_url = URL.create(
        "mssql+pyodbc",
        host=db_info["location"],
        database=db_info["current_db"],
        query={
            "TrustedConnection": db_info["trusted_connection"],
            "driver": db_info["driver"],
        },
    )
    engine = create_engine(connection_url)
    conn = engine.connect()
    conn.connection.add_output_converter(-16, handle_variant)

    return conn


def disconnect(conn: pyodbc.Connection):
    conn.close()


def query(conn: Connection, sql: str, params: tuple) -> DataFrame:
    result = read_sql_query(sql, conn, params=params)
    return result


# NOTE: Because the expectation is for the HAC database to be running locally
# and not connecting to a centralized database, f-strings are used for poducing
# the SQL query despite the potential for SQL injection with malicious input
# to the functions. This is mitigated some by parameterizing the timestamp
# conditions.


def query_tag_list(
    conn: Connection, table_info: dict, start_time: datetime, end_time: datetime
) -> DataFrame:
    tag = table_info["tags"]
    db = table_info["database"]
    tab = table_info["name"]
    sql = f"SELECT DISTINCT {tag} FROM {db}.dbo.{tab} WHERE TagTimestamp >= ? AND TagTimestamp <= ?"
    data = query(conn, sql, (start_time, end_time))
    return data


def query_instrument_data(
    conn: Connection, table_info: dict, start_time: datetime, end_time: datetime
) -> DataFrame:
    tag = table_info["tags"]
    db = table_info["database"]
    tab = table_info["name"]
    sql = f"SELECT TagTimestamp, {tag}, TagValue FROM {db}.dbo.{tab} WHERE TagTimestamp >= ? AND TagTimestamp <= ?"
    data = query(conn, sql, (start_time, end_time))
    return data
