import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from request_management import db_mysql

db = db_mysql.db
cursor = db_mysql.newCursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username  char(50) PRIMARY KEY, name VARCHAR(255),"
    "phone_number CHAR(15),"
    "password VARCHAR(150),salt VARCHAR(150),email VARCHAR(32),birth_year TINYINT, postal_code VARCHAR(32),"
    "address TEXT, weight TINYINT, gender TINYINT, height TINYINT, state TINYINT, role char(50)) ENGINE = InnoDB")

db.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS `hospital`.`api_keys` ( `api_key_id` INT NOT NULL AUTO_INCREMENT , `username` VARCHAR(50) NOT NULL\
     , `api_key` TEXT NOT NULL , `exp_date` DATETIME NULL , PRIMARY KEY (`api_key_id`)) ENGINE = InnoDB;")

db.commit()
