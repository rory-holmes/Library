import mysql.connector
import logging

logger = logging.getLogger(__name__)
logger.info("Setup logger")

def create_database():
  """
  Creates librarydb database and connects to it, calls create_all_tables method
  """
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkestt",
    port=3306,
  )
  cursor = db.cursor()
  logger.info("Creating database")
  try:
    cursor.execute("CREATE DATABASE librarydb")
    logger.info("Created database: librarydb")
    cursor.close()
    db.close()
    create_all_tables()
  except Exception as e:
    logger.error("Error creating db: %s", e)

def check_database_created():
  """
  Checks if librarydb database exists, connects to it and calls check_tables_created method if so, 
  otherwise creates database
  """
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkestt",
    port=3306,
  )
  cursor = db.cursor()
  cursor.execute("SHOW DATABASES LIKE 'librarydb'")
  databases = cursor.fetchall()
  cursor.close()
  db.close()

  if ("librarydb",) in databases:
    logger.info("Database already exists: librarydb")
    check_tables_created()

  else:
    logger.info("No database exists like: librarydb")
    create_database()

def check_tables_created():
  """
  Checks what tables are created, creates ones that are not
  """
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  expected_tables = {"books": create_books_table,
                      "authors": create_authors_table,
                        "bookauthors": create_bookAuthors_table,
                          "readingsession": create_session_table}
  mycursor.execute("SHOW TABLES")

  for (table,) in mycursor.fetchall():
    del expected_tables[table]
    logger.info("%s exists", table)

  for _, method in expected_tables.items():
    method()

  logger.info("All tables created")
  mycursor.close()
  mydb.close()
  
def create_books_table():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  mycursor.execute("""CREATE TABLE `Books` 
                  (`book_id` int(11) NOT NULL AUTO_INCREMENT,
                  `title` VARCHAR(255) NOT NULL, 
                  `publisher` VARCHAR(255),
                  `publishedDate` DATE,
                  `description` TEXT,
                  `special` BOOLEAN DEFAULT FALSE,
                  PRIMARY KEY (`book_id`))""")
  logger.info("Created Table: Books")
  mycursor.close()
  mydb.close()

def create_authors_table():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  mycursor.execute("""CREATE TABLE `Authors` 
                      (`author_id` int(11) NOT NULL AUTO_INCREMENT,
                      `author_name` VARCHAR(255) UNIQUE NOT NULL, 
                      PRIMARY KEY (`author_id`))""")
  logger.info("Created Table: Authors")
  mycursor.close()
  mydb.close()

def create_bookAuthors_table():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  mycursor.execute("""CREATE TABLE `BookAuthors` 
                      (`book_id` int(11) NOT NULL,
                      `author_id` int(11) NOT NULL,
                      PRIMARY KEY (book_id, author_id),
                      FOREIGN KEY (`book_id`) REFERENCES Books(book_id) ON DELETE CASCADE,
                      FOREIGN KEY (`author_id`) REFERENCES Authors(author_id) ON DELETE CASCADE)""")
  logger.info("Created Table: BookAuthors")
  mycursor.close()
  mydb.close()

def create_session_table():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  mycursor.execute("""CREATE TABLE `ReadingSession` 
                      (`session_id` int(11) NOT NULL AUTO_INCREMENT,
                      `book_id` int(11) NOT NULL,
                      `session_start` DATETIME NOT NULL,
                      `session_end` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                      PRIMARY KEY (`session_id`),
                      FOREIGN KEY (`book_id`) REFERENCES Books(book_id) ON DELETE CASCADE)""")
  logger.info("Created Table: ReadingSession")
  mycursor.close()
  mydb.close()

def create_all_tables():
  """
  Creates all tables for the librarydb
  """
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
  mycursor = mydb.cursor()
  try:
    create_books_table()
    create_authors_table()
    create_bookAuthors_table()
    create_session_table()
    mycursor.close()
    mydb.close()
  except Exception as e:
    logger.error("Error creating tables: %s", e)

