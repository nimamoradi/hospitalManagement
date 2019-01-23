import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username  char(50) PRIMARY KEY, name VARCHAR(255),"
    "phone_number CHAR(15),"
    "password VARCHAR(150),salt VARCHAR(150),email VARCHAR(32),birth_year TINYINT, postal_code VARCHAR(32),"
    "address TEXT, weight TINYINT, gender TINYINT, height TINYINT, state TINYINT, role char(50)) ENGINE = InnoDB")

mydb.commit()

mycursor.execute(
    "CREATE TABLE IF NOT EXISTS `hospital`.`api_keys` ( `api_key_id` INT NOT NULL AUTO_INCREMENT , `username` VARCHAR(50) NOT NULL\
     , `api_key` TEXT NOT NULL , `exp_date` DATETIME NULL , PRIMARY KEY (`api_key_id`)) ENGINE = InnoDB;")

mydb.commit()
