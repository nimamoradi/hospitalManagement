from request_management import db_mysql

db = db_mysql.db
cursor = db_mysql.newCursor()

cursor.execute("CREATE TABLE IF NOT EXISTS patient (username char(50) ,FOREIGN KEY (username) REFERENCES users(username)   ON UPDATE CASCADE   ON DELETE RESTRICT)")