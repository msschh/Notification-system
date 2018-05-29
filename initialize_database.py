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

    query = """CREATE TABLE rights(
               right_id INTEGER PRIMARY KEY,
               entity text,
               method text,
               description text
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE roles(
               role_id INTEGER PRIMARY KEY,
               name text,
               description text
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE groups(
               group_id INTEGER PRIMARY KEY,
               name text,
               description text
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE news(
               news_id INTEGER PRIMARY KEY,
               text text,
               create_date timestamp,
               start_date timestamp,
               end_date timestamp
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE roles_rights(
               role_id INTEGER REFERENCES roles(role_id),
               right_id INTEGER REFERENCES rights(right_id),
               PRIMARY KEY(role_id, right_id)
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE roles_groups(
               role_id INTEGER REFERENCES roles(role_id),
               group_id INTEGER REFERENCES groups(group_id),
               PRIMARY KEY(role_id, group_id)
               );
            """
    cursor.execute(query)

    query = """CREATE TABLE news_groups(
               news_id INTEGER REFERENCES news(news_id),
               group_id INTEGER REFERENCES groups(group_id),
               PRIMARY KEY(news_id, group_id)
               );
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