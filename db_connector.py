import os
import sqlite3

class DbConnector():
    def __init__(self, db_name: str):
        self._db_name = db_name
        self._users_table = 'users'
        self._users_table_row_names = ['login', 'password', 'first_name', 'last_name', 'role_id', 'description']
        self._events_table = 'events'
        self._events_table_row_names = ['date', 'time', 'description', 'user_id', 'doctor_id']
        self._tokens_table = 'tokens'
        self._tokens_table_row_names = ['value']
        

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
            
            # Users table
            sql = '''CREATE TABLE IF NOT EXISTS %s''' \
                  '''(id INTEGER PRIMARY KEY''' % (self._users_table)
                
            for item in self._users_table_row_names:
                sql += ', %s TEXT' % (item)
            sql += ');'

            c.execute(sql)
            print('INFO:' + str(c.fetchall()))

            # Events table
            sql = '''CREATE TABLE IF NOT EXISTS %s''' \
                  '''(id INTEGER PRIMARY KEY''' % (self._events_table)
                
            for item in self._events_table_row_names:
                sql += ', %s TEXT' % (item)
            sql += ');'

            c.execute(sql)
            print('INFO:' + str(c.fetchall()))

            # Tokens table
            sql = '''CREATE TABLE IF NOT EXISTS %s''' \
                  '''(id INTEGER PRIMARY KEY''' % (self._tokens_table)
                
            for item in self._tokens_table_row_names:
                sql += ', %s TEXT' % (item)
            sql += ');'

            c.execute(sql)
            print('INFO:' + str(c.fetchall()))


            connection.commit()

    def create_user(self, login: str, password: str, first_name: str, last_name: str,
                    role_id: int, description: str):
        if not login or not password or not first_name or not last_name \
                    or not role_id or not description:
            print('ERROR: incorrect parameters')
            return

        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()

            keysStr = ''
            valuesStr = ''
            for key in self._users_table_row_names:
                keysStr += f'{key},'
                valuesStr += '?,'
            if keysStr[-1:] == ',':
                keysStr = keysStr[:-1]
            if valuesStr[-1:] == ',':
                valuesStr = valuesStr[:-1]

            sql = f'INSERT INTO {self._users_table} ({keysStr}) VALUES({valuesStr})'
            values = [login, password, first_name, last_name, str(role_id), str(description)]
            c.execute(sql, values)
            print('INFO:' + str(c.fetchall()))
            
            connection.commit()

    def create_user_from_dict(self, user: dict):
        for row_name in self._users_table_row_names:
            if row_name not in user:
                print('ERROR: incorrect parameters')
                return

        self.create_user(user['login'], user['password'], \
                        user['first_name'], user['last_name'], \
                        int(user['role_id']), user['description'])

    def get_all_users(self):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT * FROM {self._users_table}'
            
            c.execute(sql)
            users = [dict(id=row[0], first_name=row[3], \
                            last_name=row[4], role_id=row[5], \
                            description=row[6]) for row in c.fetchall()]

            return users

    def check_exist_user(self, login: str):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT login, password FROM {self._users_table} WHERE login IS "{login}"'
            
            c.execute(sql)
            user = [dict(login=row[0], password=row[1]) for row in c.fetchall()]

            if user:
                return True
            return False

    def get_user_id_by_login(self, login: str):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT id, login, password FROM {self._users_table} WHERE login IS "{login}"'
            
            c.execute(sql)
            user = [dict(id=row[0], login=row[1], password=row[2]) for row in c.fetchall()]

            if user:
                return user[0]['id']
            return 0
    
    def get_login_by_user_id(self, user_id: int):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT id, login, password FROM {self._users_table} WHERE id IS "{user_id}"'
            
            c.execute(sql)
            user = [dict(id=row[0], login=row[1], password=row[2]) for row in c.fetchall()]

            if user:
                return user[0]['login']
            return None

    def check_valid_login_password(self, login: str, password: str):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT login, password FROM {self._users_table} WHERE login IS "{login}" AND password IS "{password}"'
            
            c.execute(sql)
            user = [dict(login=row[0], password=row[1]) for row in c.fetchall()]

            if user:
                return True
            return False

    def create_event(self, date: str, time: str, description: str, user_id: int):
        if not date or not time or not description or not user_id:
            print('ERROR: incorrect parameters')
            return

        doctor_id = self.get_user_id_by_login('g-house@gmail.com')

        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()

            keysStr = ''
            valuesStr = ''
            for key in self._events_table_row_names:
                keysStr += f'{key},'
                valuesStr += '?,'
            if keysStr[-1:] == ',':
                keysStr = keysStr[:-1]
            if valuesStr[-1:] == ',':
                valuesStr = valuesStr[:-1]

            sql = f'INSERT INTO {self._events_table} ({keysStr}) VALUES({valuesStr})'
            values = [date, time, description, str(user_id), str(doctor_id)]
            c.execute(sql, values)
            print('INFO:' + str(c.fetchall()))
            
            connection.commit()

    def create_event_from_dict(self, event: dict):
        self.create_event(event['date'], event['time'], event['description'], event['user_id'])
    
    def get_all_events(self):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT * FROM {self._events_table}'
            
            c.execute(sql)
            events = [dict(id=row[0], date=row[1], \
                            time=row[2], description=row[3], user_id=row[4], doctor_id=row[5], ) \
                            for row in c.fetchall()]

            return events
    
    def get_user_events(self, login: str):
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            users = self._users_table
            events = self._events_table

            sql = f'''SELECT {events}.id, {events}.date, {events}.time, {events}.description,
                        {events}.doctor_id
                    FROM {events}
                    INNER JOIN {users}
                    ON {events}.user_id = {users}.id
                    WHERE login = "{login}"'''            
            c.execute(sql)
            events = [dict(id=row[0], date=row[1], time=row[2], description=row[3], doctor_id=row[4]) \
                        for row in c.fetchall()]

            return events

    def add_token(self, token: str):
        if not token:
            print('ERROR: incorrect parameters')
            return
        
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()

            # sql = f'INSERT INTO {self._tokens_table} (value) VALUES({token})'
            sql = f'INSERT INTO {self._tokens_table} (value) VALUES(?)'
            c.execute(sql, [token])
            print('INFO:' + str(c.fetchall()))
            
            connection.commit()

    def get_tokens_list(self):        
        with sqlite3.connect(self._db_name) as connection:
            c = connection.cursor()
            
            sql = f'SELECT id, value FROM {self._tokens_table}'
            
            c.execute(sql)
            tokens = [dict(id=row[0], value=row[1]) for row in c.fetchall()]

            return tokens