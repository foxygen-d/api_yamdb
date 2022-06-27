import csv, sqlite3


con = sqlite3.connect('/home/foxygen/Dev/api_yamdb/api_yamdb/db.sqlite3') # поменять на путь до вашей БД
cur = con.cursor()
cur.execute("CREATE TABLE users (id, username, email, role, bio, first_name, last_name);") # название таблицы в БД и колонки прописать вручную

with open('api_yamdb/static/data/users.csv','r') as fin: # поменять на путь до файла csv
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['username'], i['email'], i['role'], i['bio'], i['first_name'], i['last_name']) for i in dr] # названия колонок

cur.executemany("INSERT INTO users (id, username, email, role, bio, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db) # название таблицы в БД и колонки прописать вручную
con.commit()
con.close()
