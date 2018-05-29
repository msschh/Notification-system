#!/usr/bin/env python3
import psycopg2
from argparse import ArgumentParser

def connect(dbname, user, password):
    conn = None
    connect_str = """dbname='{}' user='{}' host='localhost' password='{}'""".format(dbname, user, password)
    conn = psycopg2.connect(connect_str)
    return conn

def create_tables(conn):
    cursor = conn.cursor()

    query = """ALTER TABLE news
               ALTER COLUMN start_date
               TYPE DATE;
            """
    cursor.execute(query)

    query = """ALTER TABLE news
               ALTER COLUMN end_date
               TYPE DATE;
            """
    cursor.execute(query)

    cursor.execute('commit;')


def main(*args):
    conn = connect(*args)
    create_tables(conn)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('database')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    main(args.database, args.username, args.password)