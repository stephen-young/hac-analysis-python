# database contains functions to manage connecting to and querying the HAC database

import pyodbc

# TODO: Look into converting pyodbc.Row to a pandas.DataFrame


def connect(db_info: dict) -> pyodbc.Connection:
    # NOTE: Use of `Trusted_Connection` may only work on Windows
    conn = pyodbc.connect(
        driver=db_info["driver"],
        server=db_info["location"],
        database=db_info["current_db"],
        Trusted_Connection=db_info["trusted_connection"],
    )

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
    conn: pyodbc.Connection, table_info: dict, start_time, end_time
) -> list[pyodbc.Row]:
    # TODO: Get type annotations for start and end times
    tag_col = table_info["tags"]
    db_name = table_info["database"]
    table_name = table_info["name"]

    sql = TAG_QUERY.format(tag_col, db_name, table_name, start_time, end_time)
    data = query(conn, sql)

    return data
