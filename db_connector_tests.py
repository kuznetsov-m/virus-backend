import json
from db_connector import DbConnector

connector = DbConnector('sample.db')

connector.create_user('m-wazowski@gmail.com', '1234', \
                        'Mike', 'Wazowski', 2, 'User description text')
connector.create_user('g-house@gmail.com', '1234', \
                        'Gregory', 'House', 1, 'Unconventional, misanthropic medical genius')
print(connector.check_exist_user('g-house@gmail.com'))
print(connector.check_exist_user('not_exist@mail.ru'))
print(connector.check_valid_login_password('g-house@gmail.com', '1234'))
print(connector.check_valid_login_password('g-house@gmail.com', '54321'))

connector.create_event(None, None, None, None)
connector.create_event('123', None, None, None)
connector.create_event('123', '123', None, None)
connector.create_event('123', '123', '123', None)

connector.create_event("05.05.2020", '15:00', 'event description', 1)
connector.create_event("05.05.2020", '12:00', 'my description', 1)
connector.create_event("06.05.2020", '12:00', 'event description', 1)
connector.create_event("10.05.2020", '13:00', 'consilium', 2)

print('get_user_events()')
events = connector.get_user_events('m-wazowski@gmail.com')
print(f'{len(events)}: {json.dumps(events)}')

print('get_all_events()')
events = connector.get_all_events()
print(f'{len(events)}: {json.dumps(events)}')