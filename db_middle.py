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
    books = get_books_with_authors()
    return books

def add_books(title, author):
    add_book_with_author(title, author)

def loop_books():
    with open('books.txt') as topo_file:
        for line in topo_file:
            if len(line) > 2:
                l = line.split(" / ")
                author, title = l[0], l[1]
                add_books(title, [author])
            
if __name__ == "__main__":
    
    loop_books()