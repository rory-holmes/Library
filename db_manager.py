import logging
import mysql.connector

logging.basicConfig(filename='library.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="darkestt",
      port=3306,
      database="librarydb"
    )
mycursor = mydb.cursor()

def add_book_with_author(title, authors, publisher=None, publishedDate=None, description=None, special=False):
    """
    Adds a book and author if they don't exist, and links them in the BookAuthors table.
    """
    try:
        # Check if the book already exists
        book_query = """SELECT book_id FROM Books WHERE title = %s"""
        mycursor.execute(book_query, (title,))
        book_result = mycursor.fetchone()

        if book_result:
            book_id = book_result[0]
            logger.info(f"Book '{title}' already exists with ID {book_id}.")
        else:
            # Insert the book
            insert_book(title, publisher, publishedDate, description, special)
            mycursor.execute(book_query, (title,))
            book_id = mycursor.fetchone()[0]  # Retrieve the new book's ID
            logger.info(f"Inserted new book '{title}' with ID {book_id}.")

        for author_name in authors:
            # Check if the author already exists
            author_query = """SELECT author_id FROM Authors WHERE author_name = %s"""
            mycursor.execute(author_query, (author_name,))
            author_result = mycursor.fetchone()

            if author_result:
                author_id = author_result[0]
                logger.info(f"Author '{author_name}' already exists with ID {author_id}.")
            else:
                # Insert the author
                insert_author(author_name)
                mycursor.execute(author_query, (author_name,))
                author_id = mycursor.fetchone()[0]  # Retrieve the new author's ID
                logger.info(f"Inserted new author '{author_name}' with ID {author_id}.")

            # Check if the book-author relationship already exists
            book_author_query = """SELECT * FROM BookAuthors WHERE book_id = %s AND author_id = %s"""
            mycursor.execute(book_author_query, (book_id, author_id))
            book_author_result = mycursor.fetchone()

            if not book_author_result:
                # Insert into BookAuthors table
                insert_book_author(book_id, author_id)
                logger.info(f"Linked book '{title}' with author '{author_name}'.")
            else:
                logger.info(f"Book '{title}' is already linked to author '{author_name}'.")

    except Exception as e:
        logger.error(f"Error in adding book with author: {e}")

def insert_book(title, publisher=None, publishedDate=None, description=None, finished=False, special=False):
    """
    Inserts a book into the Books table.
    """
    try:
        query = """INSERT INTO Books (title, publisher, publishedDate, description, finished, special) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        mycursor.execute(query, (title, publisher, publishedDate, description, finished, special))
        mydb.commit()
        logger.info(f"Inserted book: {title}")
        return ("Book added: %s", title)
    except Exception as e:
        logger.error(f"Error inserting book {title}: {e}")
        return e

def insert_author(author_name):
    """
    Inserts an author into the Authors table.
    """
    try:
        query = """INSERT INTO Authors (author_name) VALUES (%s)"""
        mycursor.execute(query, (author_name,))
        mydb.commit()
        logger.info(f"Inserted author: {author_name}")
    except Exception as e:
        logger.error(f"Error inserting author {author_name}: {e}")

def insert_book_author(book_id, author_id):
    """
    Associates a book with an author in the BookAuthors table.
    """
    try:
        query = """INSERT INTO BookAuthors (book_id, author_id) VALUES (%s, %s)"""
        mycursor.execute(query, (book_id, author_id))
        mydb.commit()
        logger.info(f"Inserted relationship: Book {book_id} - Author {author_id}")
    except Exception as e:
        logger.error(f"Error associating book {book_id} with author {author_id}: {e}")

def insert_reading_session(book_id, session_start, session_end=None):
    """
    Inserts a reading session into the ReadingSession table.
    """
    try:
        query = """INSERT INTO ReadingSession (book_id, session_start, session_end) 
                   VALUES (%s, %s, %s)"""
        mycursor.execute(query, (book_id, session_start, session_end))
        mydb.commit()
        logger.info(f"Inserted reading session for book {book_id}")
    except Exception as e:
        logger.error(f"Error inserting reading session for book {book_id}: {e}")

def get_all_books():
    """
    Retrieves all books from the Books table.
    """
    try:
        query = """SELECT * FROM Books"""
        mycursor.execute(query)
        books = mycursor.fetchall()
        logger.info("Retrieved books")
        return books
    except Exception as e:
        logger.error(f"Error retrieving books: {e}")
        return []

def get_all_authors():
    """
    Retrieves all authors from the Authors table.
    """
    try:
        query = """SELECT * FROM Authors"""
        mycursor.execute(query)
        authors = mycursor.fetchall()
        logger.info("Retrieved authors")
        return authors
    except Exception as e:
        logger.error(f"Error retrieving authors: {e}")
        return []

def get_reading_sessions():
    """
    Retrieves all reading sessions.
    """
    try:
        query = """SELECT * FROM ReadingSession"""
        mycursor.execute(query)
        sessions = mycursor.fetchall()
        logger.info("Retrieved reading sessions")
        return sessions
    except Exception as e:
        logger.error(f"Error retrieving reading sessions: {e}")
        return []

def get_books_sorted_by_name():
    """
    Retrieves books sorted alphabetically by title.
    """
    try:
        query = """SELECT * FROM Books ORDER BY title ASC"""
        mycursor.execute(query)
        books = mycursor.fetchall()
        logger.info("Retrieved books sorted by name")
        return books
    except Exception as e:
        logger.error(f"Error sorting books by name: {e}")
        return []

def get_books_sorted_by_author():
    """
    Retrieves books sorted by author name.
    """
    try:
        query = """SELECT Books.* FROM Books 
                   JOIN BookAuthors ON Books.book_id = BookAuthors.book_id
                   JOIN Authors ON BookAuthors.author_id = Authors.author_id
                   ORDER BY Authors.author_name ASC"""
        mycursor.execute(query)
        books = mycursor.fetchall()
        logger.info("Retrieved books sorted by author")
        return books
    except Exception as e:
        logger.error(f"Error sorting books by author: {e}")
        return []
    
def get_books_with_authors():
    """
    Retrieves all books with authors, with authors returned as a list for each book.
    """
    try:
        query = """SELECT Books.*, Authors.author_id, Authors.author_name 
                   FROM Books
                   JOIN BookAuthors ON Books.book_id = BookAuthors.book_id
                   JOIN Authors ON BookAuthors.author_id = Authors.author_id
                   ORDER BY Books.title ASC"""
        
        mycursor.execute(query)
        rows = mycursor.fetchall()
        books_with_authors = {}
        
        # Organize the results so that each book has a list of authors
        for row in rows:
            book_id = row[0]
            author_name = row[-1]

            if book_id not in books_with_authors:
                row = row[:-1]
                row += ([],)
                books_with_authors[book_id] = row
            
            books_with_authors[book_id][-1].append(author_name)
        
        logger.info("Retrieved all books with authors")
        return list(books_with_authors.values())
    
    except Exception as e:
        logger.error(f"Error retrieving books with authors: {e}")
        return []


def get_books_sorted_by_recent_sessions():
    """
    Retrieves books sorted by most recent reading session.
    """
    try:
        query = """SELECT Books.* FROM Books 
                   JOIN ReadingSession ON Books.book_id = ReadingSession.book_id
                   ORDER BY ReadingSession.session_end DESC"""
        mycursor.execute(query)
        books = mycursor.fetchall()
        logger.info("Retrieved books sorted by recent sessions")
        return books
    except Exception as e:
        logger.error(f"Error sorting books by recent sessions: {e}")
        return []

def get_book_by_title(title):
    """
    Retrieves a specific book based on its title.
    Returns a dictionary with book details or None if not found.
    """
    try:
        query = """SELECT * FROM Books WHERE title = %s"""
        mycursor.execute(query, (title,))
        book = mycursor.fetchone()

        if book:
            book_data = {
                "book_id": book[0],
                "title": book[1],
                "publisher": book[2],
                "publishedDate": book[3],
                "description": book[4],
                "special": bool(book[5])
            }
            logger.info(f"Retrieved book: {book_data}")
            return book_data
        else:
            logger.info(f"Book '{title}' not found in database.")
            return None

    except Exception as e:
        logger.error(f"Error retrieving book '{title}': {e}")
        return None

def mark_book_as_finished(book_id):
    """
    Updates the 'finished' status of a book to True.
    """
    try:
        # Check if the book exists
        query_check = "SELECT book_id FROM Books WHERE book_id = %s"
        mycursor.execute(query_check, (book_id,))
        book = mycursor.fetchone()

        if book:
            # Update the book's finished status
            query_update = "UPDATE Books SET finished = %s WHERE book_id = %s"
            mycursor.execute(query_update, ("True", book_id))
            mydb.commit()
            logger.info(f"Book with ID {book_id} marked as finished.")
        else:
            logger.info(f"No book found with ID {book_id}. Nothing updated.")

    except Exception as e:
        logger.error(f"Error updating book status: {e}")
