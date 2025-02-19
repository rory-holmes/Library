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
  

connectdb()
