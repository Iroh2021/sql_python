import psycopg2

def create_db(conn, cur):
    cur.execute('''
        create table if not exists client(
            id serial primary key,
            first_name varchar(30),
            last_name varchar(30),
            email varchar(30) unique);
        create table if not exists phone(
            id serial primary key,
            client_id integer references client(id),
            phone_number varchar(30) unique);
        ''')
    conn.commit()
    print('DB was created')

def add_client(conn, cur, first_name, last_name, email, phone_number=None):
    if phone_number:
        cur.execute('insert into client(first_name, last_name, email)values(%s, %s, %s)',
                    (first_name, last_name, email))
        cur.execute('insert into phone (phone_number)values(%s)',
                    (phone_number,))
    else:
         cur.execute('insert  into client(first_name, last_name, email) values (%s, %s, %s)',
                    (first_name, last_name, email))
    conn.commit()
    print('Client added')

def add_phone(conn, cur, client_id, phone_number):
    cur.execute('insert into phone(client_id, phone_number)values(%s, %s)', 
                    (client_id, phone_number))
    conn.commit()
    print('Phone number added')

def change_client(conn, cur, client_id, first_name=None, last_name=None, email=None):
    if first_name:
        cur.execute('update client set first_name=%s where id=%s',
                    (first_name, client_id))
    elif last_name:
        cur.execute('update client set last_name=%s where id=%s',
                    (last_name, client_id))
    elif email:
        cur.execute('update client set email=%s where id=%s',
                    (email, client_id))
    conn.commit()
    print('Client info updated')

def delete_phone(conn, cur, client_id, phone_number):
    cur.execute('delete from phone where client_id=%s and phone_number=%s',
                (client_id, phone_number))
    conn.commit()
    print('Phone number deleted')

def delete_client(conn, cur, client_id):
    cur.execute('delete from phone where client_id = %s',
            (client_id,))
    cur.execute('delete from client where id = %s',
                (client_id,))
    conn.commit()
    print('Client deleted')


def find_client(conn, cur, first_name=None, last_name=None, email=None, phone_number=None):
    cur.execute('''
        select client.*, phone.phone_number
        from client
        left join phone on client.id=phone.client_id
        where first_name=%s or last_name=%s or email=%s or phone.phone_number=%s
    ''', (first_name, last_name, email, phone_number))
    result = cur.fetchall()
    if not result and phone_number:
        cur.execute('select client.*, phone.phone_number from client join phone on client.id=phone.client_id where phone.phone_number = %s',
                    (phone_number,))
        result = cur.fetchone()
    return result
        
with psycopg2.connect(database="client", user="postgres", password="836098") as conn:
    with conn.cursor() as cur:
        create_db(conn, cur)
        add_client(conn, cur, 'Oleg', 'Ershov', 'ershovoleg18@mail.ru', '+7 905 269 29 23')
        add_client(conn, cur, 'Ivan', 'Korchnoj', 'Yolamdi@mail.ru', '+7 911 938 75 15')
        add_phone(conn, cur, 1, '+7 905 938 79 52')
        add_phone(conn, cur, 2, '+7 911 296 26 29')
        change_client(conn, cur, 1, 'Ilias', 'Polov', 'liperchat@mail.ru')
        delete_phone(conn, cur, 1, '+7 905 269 29 23')
        delete_client(conn, cur, 1)
        print(find_client(conn, cur, first_name='Ivan'))
        print(find_client(conn, cur, last_name='Korchnoj'))
        print(find_client(conn, cur, email='Yolamdi@mail.ru'))
        print(find_client(conn, cur, phone_number='+7 911 296 26 29'))
conn.close()