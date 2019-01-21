from request_management import db_mysql

db = db_mysql.db
cursor = db_mysql.newCursor()

cursor.execute("CREATE TABLE IF NOT EXISTS prescription (docter_id char(50) NOT NULL , id int(10) PRIMARY KEY NOT NULL , patient_id char(50) NOT NULL , `date` DATETIME);")
