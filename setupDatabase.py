import mysql.connector
import logging

def create_database():
  logging.info("Creating database")
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkestt",
    port=3306,
  )
  mycursor = mydb.cursor()
  try:
    mycursor.execute("CREATE DATABASE librarydb")
    logging.info("Created database {librarydb}")
  except Exception as e:
    logging.error(f"Error creating db: {e}")

def check_database_created():
  mycursor.execute("SHOW DATABASES LIKE 'librarydb'")
  if "librarydb" in mycursor:
    logging.info("Database {librarydb} already exists")
  else:
    logging.info("No database like {librarydb} exists")

def check_tables_created():
  expected_tables = {"Books": create_books_table,
                      "Authors": create_authors_table,
                        "BookAuthors": create_bookAuthors_table,
                          "ReadingSession": create_session_table}
  mycursor.execute("SHOW TABLES")
  for table in mycursor:
    expected_tables.pop(table)
    logging.info(f"{table} exists")
  for _, method in expected_tables:
    method()
    
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
  
def create_books_table():
  mycursor.exectute("""CREATE TABLE `Books` 
                  (`book_id` int(11) NOT NULL AUTO_INCREMENT,
                  `title` VARCHAR(255) NOT NULL, 
                  `publisher` VARCHAR(255),
                  `publishedDate` DATE,
                  `description` TEXT,
                  `special` BOOLEAN DEFAULT FALSE,
                  PRIMARY KEY (`book_id`))""")
  logging.info("Created {Books} Table")

def create_authors_table():
    mycursor.exectute("""CREATE TABLE `Authors` 
                      (`author_id` int(11) NOT NULL AUTO_INCREMENT,
                      `author_name` VARCHAR(255) UNIQUE NOT NULL, 
                      PRIMARY KEY (`author_id`))""")
    logging.info("Created {Authors} Table")

def create_bookAuthors_table():
  mycursor.exectute("""CREATE TABLE `BookAuthors` 
                      (`book_id` int(11) NOT NULL,
                      `author_id` int(11) NOT NULL,
                      PRIMARY KEY (book_id, author_id),
                      FOREIGN KEY (`book_id`) REFERENCES Books(book_id) ON DELETE CASCADE,
                      FOREIGN KEY (`author_id`) REFERENCES Authors(author_id) ON DELETE CASCADE)""")
  logging.info("Created {BookAuthors} Table")

def create_session_table():
  mycursor.exectute("""CREATE TABLE `ReadingSession` 
                      (`session_id` int(11) NOT NULL AUTO_INCREMENT,
                      `book_id` int(11) NOT NULL,
                      `session_start` DATETIME NOT NULL,
                      `session_end` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                      PRIMARY KEY (`session_id`),
                      FOREIGN KEY (`book_id`) REFERENCES Books(book_id) ON DELETE CASCADE)""")
  logging.info("Created {ReadingSession} Table")

def create_all_tables():
  try:
    create_books_table()
    create_authors_table()
    create_bookAuthors_table()
    create_session_table()
  except Exception as e:
    logging.error(f"Error creating tables: {e}")

