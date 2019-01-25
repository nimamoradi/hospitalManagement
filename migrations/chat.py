import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS `hospital`.`messages` ( `id` INT NOT NULL AUTO_INCREMENT , `sender` MEDIUMTEXT NOT NULL REFERENCES users(username)\
    , `reciever` MEDIUMTEXT NOT NULL REFERENCES users(username) , `message` TEXT NOT NULL , `date` DATETIME NOT NULL , `seen` BOOLEAN NOT NULL\
  , PRIMARY KEY (`id`)) ENGINE = InnoDB;")  
