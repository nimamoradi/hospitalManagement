from config import database
import mysql.connector

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS `hospital`.`invoice_item` \
    ( `id` INT NOT NULL AUTO_INCREMENT , `name` CHAR(50) NOT NULL , `unit` INT NOT NULL , `origin` MEDIUMTEXT NOT NULL\
     , `patient` MEDIUMTEXT NOT NULL , `type` MEDIUMTEXT NOT NULL , `unit_price` INT NOT NULL , `date` DATETIME NOT NULL\
     , `paid` BOOLEAN NOT NULL DEFAULT FALSE , PRIMARY KEY (`id`)) ENGINE = InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;")
