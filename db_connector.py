import os
import sqlite3

class DbConnector():
    def __init__(self, db_name: str):
        self._db_name = db_name
        self._events_table = 'events'

        self._create_db()

    def _create_db(self):
        if os.path.isfile(self._db_name):
            try:
                os.remove(self._db_name)

                f = open(self._db_name, 'w+')
            except IOError:
                print('ERROR: db not created')
            finally:
                f.close()

        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            rowNames = ['date', 'time', 'description', 'user_id']

            sql = '''CREATE TABLE IF NOT EXISTS %s''' \
                  '''(id INTEGER PRIMARY KEY''' % (self._events_table)
                
            for item in rowNames:
                sql += ', %s TEXT' % (item)
            sql += ');'

            c.execute(sql)
            print('INFO:' + str(c.fetchall()))

            connection.commit()

    def create_event(self, date: str, time: str, description: str, user_id: int):
        if not date or not time or not description or not user_id:
            print('ERROR: incorrect parameters')
            return

        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()

            keys = ['date', 'time', 'description', 'user_id']
            keysStr = ''
            for key in keys:
                keysStr += f'{key},'
            if keysStr[-1:] == ',':
                keysStr = keysStr[:-1]

            sql = f'INSERT INTO {self._events_table} ({keysStr}) VALUES(?, ?, ?, ?)'
            values = [date, time, description, str(user_id)]
            c.execute(sql, values)
            print('INFO:' + str(c.fetchall()))
            
            connection.commit()
    
    def get_all_events(self):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT * FROM {self._events_table}'
            
            c.execute(sql)
            events = [dict(date=row[0], time=row[1], description=row[2], user_id=row[3] ) for row in c.fetchall()]

            return events
