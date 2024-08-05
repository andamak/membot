import sqlite3
import os, datetime as dt
from dotenv import load_dotenv

load_dotenv()

ADMIN_CHAT_ID = os.getenv('chat_id')
name_db = 'membot.db'

def write_la(chat_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    date_now = dt.datetime.now()
    cursor.execute('update users set last_act = ? where chat_id = ?', (date_now, chat_id))
    connection.commit()
    connection.close()


def sel_orgs(user_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    if check_adm_user(user_id):
        cursor.execute('select * from orgs')
    else:
        cursor.execute('select * from orgs where id in (select org_id from orgs_acc where user_id = ?)', (user_id,))
    orgs = cursor.fetchall()
    connection.close()
    return orgs


def sel_orgs_for_subs():
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    cursor.execute('select * from orgs where id in (select org_id from subs  group by org_id)')
    orgs = cursor.fetchall()
    connection.close()
    return orgs


def check_subs(org_id, user_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()  
    cursor.execute('select * from subs where org_id = ? and user_id = ?', (org_id, user_id))
    subs = cursor.fetchall()
    connection.close()
    if subs:
        return True
    else:
        return False


def get_subs():
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()  
    cursor.execute('''select subs.user_id, subs.org_id, orgs.brief_name_en, subs.orders, users.chat_id, orgs.full_name 
                   from subs, orgs, users where subs.user_id=users.id and subs.org_id = orgs.id''')
    subs = cursor.fetchall()
    connection.close()
    return subs


def upd_subs(user_id, cnt_orders, org_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()  
    #date_now = dt.datetime.now()
    cursor.execute('update subs set orders = ? where user_id = ? and org_id = ?', (cnt_orders, user_id, org_id))
    connection.commit()
    connection.close()


def add_sub(org_id, user_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()  
    date_now = dt.datetime.now()
    cursor.execute('insert into subs (org_id, user_id, date_reg) values (?, ?, ?)', (org_id, user_id, date_now))
    connection.commit()
    connection.close()


def del_sub(org_id, user_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()  
    cursor.execute('delete from subs where org_id = ? and user_id = ?', (org_id, user_id))
    connection.commit()
    connection.close() 
    

def check_user(chat_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    # Проверяем есть ли такой пользователь
    cursor.execute('select * from users where chat_id = ?', (chat_id,))
    users = cursor.fetchall()
    connection.close()
    if users:
        return users[0][0]
    else:
        return 0
    

def get_users():
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()   
    cursor.execute('select * from users')
    users = cursor.fetchall()
    connection.close()    
    return users


def check_adm_chat(chat_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    # Проверяем на супер админа
    cursor.execute('select * from users where is_admin = 1 and chat_id = ?', (chat_id,))
    users = cursor.fetchall()
    connection.close()
    if users:
        return True
    else:
        return False


def check_adm_user(user_id):
    connection = sqlite3.connect(name_db)    
    cursor = connection.cursor()
    # Проверяем на супер админа
    cursor.execute('select * from users where is_admin = 1 and id = ?', (user_id,))
    users = cursor.fetchall()
    connection.close()
    if users:
        return True
    else:
        return False

def create_user(first_name, last_name, full_name, chat_id, is_premium, language_code):
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()
    date_reg = dt.datetime.now()
    is_admin = 0
    cursor.execute('''INSERT INTO users (first_name, last_name, full_name, chat_id, is_premium, language_code, date_reg, is_admin) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (first_name, last_name, full_name, chat_id, is_premium, language_code, date_reg, is_admin)) 
    connection.commit()
    connection.close()


def create_database():
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   first_name TEXT, 
                   last_name TEXT, 
                   full_name TEXT,
                   chat_id INTEGER, 
                   is_premium INTEGER, 
                   language_code TEXT,
                   date_reg DATETIME, 
                   last_act DATETIME,
                   is_admin INTEGER DEFAULT 0
                   )
                   ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS content (
                   id INTEGER PRIMARY KEY, 
                   brief_name_ru TEXT, 
                   brief_name_en TEXT,
                   full_name TEXT,
                   type_of_content integer,
                   year_creation TEXT,
                   is_serial integer
                   )
                   ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS serial_list (
                   id INTEGER PRIMARY KEY, 
                   id_serial INTEGER,
                   season INTEGER,
                   episode INTEGER,
                   name_en INTEGER, 
                   name_ru TEXT,
                   date_out TEXT
                   )
                   ''')   

    cursor.execute('''CREATE TABLE IF NOT EXISTS status_list (
                   id INTEGER PRIMARY KEY, 
                   status_name_ru TEXT,
                   status_name_en TEXT
                   )
                   ''')   

    cursor.execute('''CREATE TABLE IF NOT EXISTS content_list (
                   id INTEGER PRIMARY KEY, 
                   content_name_ru TEXT,
                   content_name_en TEXT
                   )
                   ''')  
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS content_status ( 
                   user_id INTEGER,
                   content_id INTEGER,
                   status_id INTEGER,
                   date_change DATETIME
                   )
                   ''')  

    cursor.execute('''CREATE TABLE IF NOT EXISTS serial_status ( 
                   user_id INTEGER,
                   serial_id INTEGER,
                   status_id INTEGER,
                   date_change DATETIME
                   )
                   ''')  

    cursor.execute('''CREATE TABLE IF NOT EXISTS status_log ( 
                   user_id INTEGER,
                   content_id INTEGER DEFAULT 0 NOT NULL,
                   serial_id INTEGER DEFAULT 0 NOT NULL,
                   old_status_id INTEGER,
                   new_status_id INTEGER,
                   date_change DATETIME
                   )
                   ''')  

    cursor.execute('''CREATE TABLE IF NOT EXISTS score_table ( 
                   user_id INTEGER,
                   content_id INTEGER DEFAULT 0 NOT NULL,
                   serial_id INTEGER DEFAULT 0 NOT NULL,
                   score INTEGER,
                   feedback INTEGER,
                   date_change DATETIME
                   )
                   ''')  

    connection.commit()
    connection.close()


#Create superuser
def init_db(ADMIN_CHAT_ID):
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()
    first_name = 'admin'
    last_name = 'admin' 
    full_name = 'admin admin'
    chat_id = ADMIN_CHAT_ID
    is_premium  = 1 
    language_code = 'ru'
    date_reg = dt.datetime.now()
    is_admin =1  
    cursor.execute('''INSERT INTO users (first_name, last_name, full_name, chat_id, is_premium, language_code, date_reg, is_admin) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (first_name, last_name, full_name, chat_id, is_premium, language_code, date_reg, is_admin)) 
    connection.commit()
    connection.close()


# Заполняем статусы и типы контента
def init_db_defa():
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()
    cursor.execute('delete from status_list')
    statuss = [['Новый','New'], ['Смотрю','inAction'], ['След','Next'], ['Просмотрен','Done']]
    for status in statuss:
        cursor.execute('''INSERT INTO status_list (status_name_ru, status_name_en) 
                       VALUES (?,?)''', (status[0], status[1]))
        connection.commit()

    cursor.execute('delete from content_list')
    contents = [['Сериал','Serial'], ['Фильм','Film'], ['Книга','Book'], ['Комикс','Comics']]
    for content in contents:
        cursor.execute('''INSERT INTO content_list (content_name_ru, content_name_en) 
                       VALUES (?,?)''', (content[0], content[1]))
        connection.commit()
    
    connection.close()


def start_sel():
    chat_id = 6939795801
    chat_id = 124723377

    brief_name_ru = 'СШ'
    brief_name_en = get_org_ru(chat_id, brief_name_ru)
    if brief_name_en == 'not_found':
        print('не найдены варианты')
    else:
        print(brief_name_en)
    

def main():
    create_database()
    init_db(ADMIN_CHAT_ID)
    init_db_defa()
    #start_sel()
    #print(check_subs(1,1))
    # orgs = sel_orgs_for_subs()
    # print(orgs)
    # dorg ={}
    # for org in orgs:
    #     dorg.update({org[0]:org[1]})
    # print(dorg)
    # print(dorg[1])

if __name__ == '__main__':
    main()
