import sqlite3

conn = sqlite3.connect(':memory:')  # создаст базу данных в оперативной памяти,удалит после завершения
# conn = sqlite3.connect('example.db')  # создат базу данных, которая не удалится после завершения

cur = conn.cursor()  # создание курсора, для работы с базой

cur.execute('CREATE TABLE users (user_id int, first_name text)')
cur.execute('INSERT INTO users VALUES (1, "Ivan")')
cur.execute('INSERT INTO users VALUES (2, "Marya")')
cur.execute('INSERT INTO users VALUES (3, "Egor")')

cur.execute('SELECT * FROM users')
print('first_try', cur.fetchall())  # выведет информацию
print('second_try', cur.fetchall())  # ничего не выведет, т.к. cur - уже пустой
cur.execute('SELECT * FROM users')  # выведет информацию
for _i in cur:
    print('first_iterator', _i)

for _i in cur:
    print('seconde_iterator', _i)


# Экранирование запросов

query_list = [
    (4, 'Artem'),
    (5, 'Dmitry'),
    (6, 'Nekita')
]

cur.executemany('INSERT INTO users VALUES (?, ?)', query_list)

cur.execute('SELECT * FROM users')
print('Select where many queries', cur.fetchall())  # выведет информацию

cur.execute('INSERT INTO users VALUES (:id, :first_name)', {'id': 7, 'first_name': 'Kolya'})
cur.execute('SELECT * FROM users')
print('Select where literal', cur.fetchall())  # выведет информацию

# Удаление

cur.execute('DELETE FROM users WHERE user_id < 3')
cur.execute('SELECT * FROM users')
print('Select after delete', cur.fetchall())

# Обновление

cur.execute('UPDATE users SET first_name="ANYA" WHERE user_id > 4')
cur.execute('SELECT * FROM users')
print('Select after update', cur.fetchall())

# Сложные запросы

cur.execute('SELECT * FROM users WHERE user_id>4')
print('1 - Select Where:', cur.fetchall())

cur.execute('SELECT user_id FROM users WHERE first_name == "Marya"')
print('2 - Select Where:', cur.fetchall())

cur.execute('SELECT user_id FROM users WHERE user_id in (1, 5, 6, 10)')
print('2 - Select Where:', cur.fetchall())

# Много запросов
cur.executescript("""
    INSERT INTO users VALUES (10, 'VALUE');
    UPDATE users SET first_name='UPDATED VALUE' WHERE user_id=10;
""")
cur.execute('SELECT * FROM users')
print('Select after exec script', cur.fetchall())


# SQL инъекции
# Не получится
try:
    user_name = f'"ANYA"; UPDATE users SET first_name="LOL";'
    print(f'SELECT * FROM users WHERE first_name = {user_name}')
    cur.execute(f'SELECT * FROM users WHERE first_name = {user_name}')
    cur.execute('SELECT * FROM users')
    print('1 - Select after ingection', cur.fetchall())
except Exception as e:
    print(f'Exception: {e}')

# Получится
user_name = f'"ANYA"; UPDATE users SET first_name="LOL";'
cur.executescript(f'SELECT * FROM users WHERE first_name = {user_name}')
cur.execute('SELECT * FROM users')
print('2 - Select after ingection', cur.fetchall())

# С экранированием
user_name = f'"ANYA"; UPDATE users SET first_name="WITH_SECURE";'
cur.execute(f'SELECT * FROM users WHERE first_name = (?)', (user_name,))
cur.execute('SELECT * FROM users')
print('3 - Select after ingection', cur.fetchall())

conn.close()
