from db_connector import DbConnector

connector = DbConnector('sample.db')

connector.create_user('m-wazowski@gmail.com', '1234', \
                        'Mike', 'Wazowski', 2, 'User description text')
connector.create_user('g-house@gmail.com', '1234', \
                        'Gregory', 'House', 1, 'Unconventional, misanthropic medical genius')

connector.create_event(None, None, None, None)
connector.create_event('123', None, None, None)
connector.create_event('123', '123', None, None)
connector.create_event('123', '123', '123', None)

connector.create_event("123", '456', 'text text', 55)
connector.create_event("234", '41212356', 'text asdtext', 44)

events = connector.get_all_events()
print(events)