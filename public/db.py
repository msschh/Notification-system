import psycopg2
import time
from datetime import datetime
import json
import psycopg2.extras


class DataBase:
    conn = None
    def __init__(self, dbname, user, password):
        global conn
        connect_str = """dbname='{}' user='{}' host='localhost' password='{}'""".format(dbname, user, password)
        conn = psycopg2.connect(connect_str)

    def string_to_date(self, string):
        date_format1 = '%m/%d/%Y'
        date_format2 = '%Y-%m-%d'
        try:
            start = datetime.strptime(string, date_format1)
        except ValueError:
            start = datetime.strptime(string, date_format2)

        return start


    def add_news(self, dates_to_insert):
        dates = json.loads(dates_to_insert)
        text = dates['text']
        author = dates['author']
        now = datetime.now().replace(second=0, microsecond=0)
        start = self.string_to_date(dates['start_date'])
        end = self.string_to_date(dates['end_date'])

        query = """SELECT nextval('seq_news') """
        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query)
        news_id = cursor.fetchone()[0]

        cursor = conn.cursor()
        query = """INSERT INTO news (news_id, text, create_date, start_date, end_date, author)
                   VALUES (%s, %s, %s, %s, %s, %s);
                """
        cursor.execute(query, (news_id, text, now, start, end, author))
        cursor.execute('commit;')

        self.add_groups_to_news(news_id, dates['groups'])

        return news_id

    def update_news(self, dates_to_insert):
        dates = json.loads(dates_to_insert)
        id = dates['news_id']
        text = dates['text']
        start = self.string_to_date(dates['start_date'])
        end = self.string_to_date(dates['end_date'])

        cursor = conn.cursor()
        query = """UPDATE news SET text = %s, start_date = %s, end_date = %s WHERE news_id = %s;
                """
        cursor.execute(query, (text, start, end, id))
        cursor.execute('commit;')

    def read_all_news(self, group, teacher_name=None):
        '''
        return a list of dicts (all entries in news database)
        '''
        if teacher_name is not None:
            query = """SELECT news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date, 
                        to_char(end_date, 'YYYY-MM-DD') as end_date, author, (end_date >= current_date) AS activ 
                    FROM news
                    WHERE author = %s
                    ORDER BY create_date DESC;
                    """
            cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute(query, [teacher_name])
        else:
            if group is None:
                query = """SELECT news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date,
                            to_char(end_date, 'YYYY-MM-DD') as end_date, author, (end_date >= current_date) AS activ 
                        FROM news
                        ORDER BY create_date DESC;
                        """
                cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(query)
            else:
                query = """SELECT N.news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date,
                            to_char(end_date, 'YYYY-MM-DD') as end_date, author, (end_date >= current_date) AS activ 
                        FROM news N LEFT JOIN news_groups NG ON N.news_id = NG.news_id
                        WHERE NG.group_id = %s
                        ORDER BY create_date DESC;
                        """
                cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(query, [group])

        rows = cursor.fetchall()
        return rows

    def read_news(self, id):
        query = """SELECT news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date, 
                    to_char(end_date, 'YYYY-MM-DD') as end_date, author FROM news WHERE news_id = %s;"""


        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query, [id])
        news = dict(cursor.fetchone())
        news['grupe'] = self.read_group_of_news(id)
        return news

    def delete_news(self, id):
        self.delete_groups_of_news(id)
        query = """DELETE FROM news WHERE news_id = %s;"""
        cursor = conn.cursor()
        cursor.execute(query, [id])
        cursor.execute('commit')

    def read_group_of_news(self, id):
        query = """SELECT group_id FROM news_groups where news_id = %s;"""
        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query, [id])
        groups = cursor.fetchall()
        return groups

    def add_groups_to_news(self, news_id, groups_id):
        for group_id in groups_id:
            cursor = conn.cursor()
            query = """INSERT INTO news_groups (news_id, group_id) 
                       values (%s, %s);
                    """
            cursor.execute(query, [news_id, group_id])
            cursor.execute('commit;')

    def delete_groups_of_news(self, news_id):
        query = """DELETE FROM news_groups WHERE news_id = %s;"""
        cursor = conn.cursor()
        cursor.execute(query, [news_id])
        cursor.execute('commit')

    def add_user_news(self, news_id, user_email):
        cursor = conn.cursor()
        query = """SELECT count(*) 
                   FROM seen_news
                   WHERE id_news = %s AND email_user = %s;
                """
        cursor.execute(query, (news_id, user_email))

        if cursor.fetchone()[0] == 0:
            query = """INSERT INTO seen_news (id_news, email_user)
                       values (%s, %s);
                    """
            cursor.execute(query, (news_id, user_email))
            cursor.execute('commit;')

    def read_unread_news(self, group, user_email, is_teacher):
        if is_teacher:
            return []
        else:
            if group is None:
                query = """SELECT N.news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date,
                            to_char(end_date, 'YYYY-MM-DD') as end_date, author, (end_date >= current_date) AS activ 
                        FROM news N
                        WHERE (SELECT count(*) FROM seen_news UN WHERE UN.email_user = %s and UN.id_news = N.news_id) = 0
                        ORDER BY create_date DESC;
                        """
                cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(query, [user_email])
            else:
                query = """SELECT N.news_id, text, create_date, to_char(start_date, 'YYYY-MM-DD') as start_date,
                            to_char(end_date, 'YYYY-MM-DD') as end_date, author, (end_date >= current_date) AS activ 
                        FROM news N 
                        LEFT JOIN news_groups NG ON N.news_id = NG.news_id
                        WHERE NG.group_id = %s and (SELECT count(*) FROM seen_news UN WHERE UN.email_user = %s and UN.id_news = N.news_id) = 0
                        ORDER BY create_date DESC;
                        """
                cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(query, [group, user_email])

        rows = cursor.fetchall()
        return rows

    def add_token(self, grupa, token):
        query = """SELECT * FROM tokens WHERE token = %s"""
        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query, [token])

        fetched = cursor.fetchall()

        print('fetched: {}, {}'.format(fetched, token))

        if len(fetched) == 0:
            query = """INSERT INTO tokens VALUES (%s, %s);"""
        else:
            query = """UPDATE tokens SET group_id = %s WHERE token = %s;"""
        
        cursor = conn.cursor()
        cursor.execute(query, [grupa, token])
        cursor.execute('commit;')

        return {"response": "ok"}


    def get_tokens(self, grupa):
        query = """SELECT token FROM tokens WHERE group_id = %s;"""
        cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query, [grupa])
        fetched = cursor.fetchall()
        tokens = [token for [token] in fetched]
        return tokens