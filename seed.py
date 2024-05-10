from connect import create_connection, database
from faker import Faker
import random

fake = Faker()

def fake_users(conn, num_users):
    cursor = conn.cursor()
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email))
    conn.commit()

def fake_status(conn):
    cursor = conn.cursor()
    statuses = [('new',), ('in progress',), ('completed',)]
    for status in statuses:
        cursor.execute("INSERT OR IGNORE INTO status (name) VALUES (?)", status)
    conn.commit()

def fake_tasks(conn, num_tasks, num_users, num_status):
    cursor = conn.cursor()
    for _ in range(num_tasks):
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.randint(1, num_status)
        user_id = random.randint(1, num_users) if num_users > 0 else None
        cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)", (title, description, status_id, user_id))
    conn.commit()

if __name__ == '__main__':
    num_users = 6
    num_tasks = 12
    

    with create_connection(database) as conn:
        if conn is not None:
            fake_users(conn, num_users)
            fake_status(conn)
            fake_tasks(conn, num_tasks, num_users, 3)
        else:
            print("Error! cannot create the database connection.")