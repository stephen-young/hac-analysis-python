# database contains functions to manage connecting to and querying the HAC database

import pyodbc
from datetime import datetime

# TODO: Look into converting pyodbc.Row to a pandas.DataFrame


def handle_variant(var):
    if type(var) is bytes:
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


def query(conn: pyodbc.Connection, sql: str):
    cursor = conn.cursor()
    cursor.execute(sql)

    return cursor.fetchall()


TAG_QUERY = """
        SELECT DISTINCT({})
        FROM {}.dbo.{}
        WHERE TagTimestamp > '{}' AND TagTimestamp < '{}'
    """


def query_tag_list(
    conn: pyodbc.Connection, table_info: dict, start_time: datetime, end_time: datetime
) -> list[pyodbc.Row]:
    tag_col = table_info["tags"]
    db_name = table_info["database"]
    table_name = table_info["name"]

    sql = TAG_QUERY.format(tag_col, db_name, table_name, start_time, end_time)
    data = query(conn, sql)

    return data


INSTR_QUERY = """
        SELECT {}, {}, {}
        FROM {}.dbo.{}
        WHERE TagTimestamp > '{}' AND TagTimestamp < '{}'
    """


def query_instrument_data(
    conn: pyodbc.Connection, db_info: dict, start_time: datetime, end_time: datetime
) -> list[pyodbc.Row]:
    db_name = db_info["database"]
    table_name = db_info["name"]
    tag_col = db_info["tags"]
    value_col = db_info["values"]
    time_col = db_info["times"]
    sql = INSTR_QUERY.format(
        time_col, tag_col, value_col, db_name, table_name, start_time, end_time
    )
    data = query(conn, sql)

    return data
