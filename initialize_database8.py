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

    query = """ALTER TABLE user_news
               DROP COLUMN id
            """
    cursor.execute(query)

    query = """DELETE FROM user_news a
               WHERE a.ctid <> (SELECT min(b.ctid)
                                FROM user_news b
                                WHERE a.email_user = b.email_user
                                AND a.id_news = b.id_news);
            """
    cursor.execute(query)

    query = """ALTER TABLE user_news
               ADD CONSTRAINT seen PRIMARY KEY (email_user, id_news);
            """
    cursor.execute(query)

    query = """ALTER TABLE user_news
               RENAME TO seen_news;
            """
    cursor.execute(query)

    query = "DROP SEQUENCE seq_roles;"
    cursor.execute(query)

    query = "DROP SEQUENCE seq_groups;"
    cursor.execute(query)

    query = "DROP SEQUENCE seq_rights;"
    cursor.execute(query)

    query = "DROP SEQUENCE seq_user_news;"
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