#!/usr/bin/env python3
import psycopg2
from argparse import ArgumentParser
from datetime import datetime

def connect(dbname, user, password):
    conn = None
    connect_str = """dbname='{}' user='{}' host='localhost' password='{}'""".format(dbname, user, password)
    conn = psycopg2.connect(connect_str)
    return conn

def modify_tables(conn):
    cursor = conn.cursor()

    query = """ALTER TABLE news_groups
               DROP CONSTRAINT news_groups_group_id_fkey;
            """
    cursor.execute(query)

    query = "DROP TABLE roles_groups;"
    cursor.execute(query)

    query = "DROP TABLE roles_rights;"
    cursor.execute(query)

    query = "DROP TABLE groups;"
    cursor.execute(query)

    query = "DROP TABLE roles;"
    cursor.execute(query)

    query = "DROP TABLE rights;"
    cursor.execute(query)

    query = "ALTER TABLE news ADD COLUMN author text;"
    cursor.execute(query)

    query = "ALTER TABLE user_news DROP COLUMN id;"
    cursor.execute(query)

    query = "ALTER TABLE user_news RENAME COLUMN id_news TO news_id;"
    cursor.execute(query)

    cursor.execute('commit;')


def main(*args):
    conn = connect(*args)
    modify_tables(conn)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('database')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    main(args.database, args.username, args.password)