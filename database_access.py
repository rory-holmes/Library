import mysql.connector
import logging

def create_database():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkestt",
    port=3306,
  )
  mycursor = mydb.cursor()
  try:
    mycursor.execute("CREATE DATABASE librarydb")
    logging.info("Created librarydb")
  except Exception as e:
    logging.error(f"Error creating db: {e}")

def connectdb():
  global mycursor
  try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
    logging.info(f"Connected: {mydb.is_connected()}")
    mycursor = mydb.cursor()
  except Exception as e:
    logging.error(f"Error connecting to librarydb: {e}")
  
def create_tables():
  mycursor.exectute("""CREATE TABLE `books` 
                    (`book_id` int(11) NOT NULL AUTO_INCREMENT,
                    `name` VARACHAR(255) NOT NULL, 
                    `author_id` int(11) NOT NULL,
                    `series_id` VARCHAAR(255),
                    `special` enum('T','F'),
                    `session_id` int(11),
                    PRIMARY KEY (`book_id`),
                    FOREIGN KEY (`author_id`),
                    FOREIGN KEY (`session_id`),
                    FOREIGN KEY (`series_id`))""")
  mycursor.exectute("""CREATE TABLE `author` 
                    (`author_id` int(11) NOT NULL AUTO_INCREMENT,
                    `author_name` VARACHAR(255) NOT NULL, 
                    PRIMARY KEY (`author_id`))""")
  mycursor.exectute("""CREATE TABLE `series` 
                    (`series_id` int(11) NOT NULL AUTO_INCREMENT,
                    `series_name` VARACHAR(255) NOT NULL, 
                    PRIMARY KEY (`series_id`))""")
  mycursor.exectute("""CREATE TABLE `session` 
                    (`session_id` int(11) NOT NULL AUTO_INCREMENT,
                    `book_id` int(11) NOT NULL,
                    PRIMARY KEY (`session_id`),
                    FOREIGN KEY (`book_id`))""")
connectdb()
