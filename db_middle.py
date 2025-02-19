import logging
from db_manager import *
from google_books_api import *
import time    

bookOne = {
    "Title": "The Front Runner",
    "Authors": ["Elsie Silver", "Rory Holmes"],
    "Publisher": "Simon & Schuster",
    "Published Date": None,
    "Description": "Something boring"
            }

def add_book():
    barcode = input("Add book barcode: ")
    #book_info = get_book_info_from_barcode(barcode)
    book_info = bookOne
    print(book_info)
    add_book_with_author(book_info['Title'], book_info['Authors'], book_info['Publisher'], book_info['Published Date'], book_info['Description'])

def display_books():
    books = get_books_sorted_by_name()
    for book in books:
        print(books)

if __name__ == "__main__":
    
    display_books()