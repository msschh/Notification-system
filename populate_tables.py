#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
from argparse import ArgumentParser
from datetime import datetime


def connect(dbname, user, password):
    conn = None
    connect_str = """dbname='{}' user='{}' host='localhost' password='{}'""".format(dbname, user, password)
    conn = psycopg2.connect(connect_str)
    return conn


def add_entries(conn):
    # define query templates
    query_n = """INSERT INTO news values (%s, %s, %s, %s, %s, %s);"""
    query_gn = "INSERT INTO news_groups values (%s, %s);"
    seq = """SELECT nextval('seq_news') """ 

    from news_to_insert import news
    
    for n in news:
        # find the next news id
        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(seq)
        news_id = cursor.fetchone()[0]

        # insert news
        cursor = conn.cursor()
        cursor.execute(query_n, (news_id, n['text'], n['now'], n['start'], n['end'], n['author']))

        # assigne news to groups
        for group in n['groups']:
            cursor = conn.cursor()
            cursor.execute(query_gn, (news_id, group))

    # commit all insertions
    cursor = conn.cursor()
    cursor.execute('commit;')


def main(*args):
    conn = connect(*args)
    add_entries(conn)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('database')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    main(args.database, args.username, args.password)