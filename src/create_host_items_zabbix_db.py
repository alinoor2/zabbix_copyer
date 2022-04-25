import sqlite3
import src.create_host_items_zabbix as crt
# import dbs as db


def create_host_db():
    pass


def create_item_db():
    pass


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM host_detailes")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_hostdeatails_by_stat(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM host_detailes WHERE stat=?", ('YES',))

    rows = cur.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    conn = create_connection("output_0_29db.sqlite")
    select_hostdeatails_by_stat(conn)