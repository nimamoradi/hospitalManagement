import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS laboratorian (username char(50) ,FOREIGN KEY (username) REFERENCES users(username)   ON UPDATE CASCADE   ON DELETE RESTRICT)")

mycursor.execute("CREATE TABLE `hospital`.`labratory` ( `id` INT NOT NULL AUTO_INCREMENT , `doctor` VARCHAR NOT NULL , `patient` VARCHAR NOT NULL , `type` TEXT NOT NULL , `result` TEXT NOT NULL , `paid` BOOLEAN NOT NULL , `desc` TEXT NOT NULL , PRIMARY KEY (`id `)) ENGINE = InnoDB;")
