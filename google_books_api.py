import requests
import logging
logging.basicConfig(filename='library.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_book_info_from_barcode(barcode):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book = data["items"][0]["volumeInfo"]
            title = book.get("title", "Unknown Title")
            authors = book.get("authors", ["Unknown Author"])
            publisher = book.get("publisher", "Unknown Publisher")
            published_date = book.get("publishedDate", "Unknown Date")
            description = book.get("description", "No description available.")
            logging.info("Retrieved book information for: %s", title)
            return {
                "Title": title,
                "Authors": authors,
                "Publisher": publisher,
                "Published Date": published_date,
                "Description": description
            }
        else:
            logging.warning("No book found for barcode: %s", barcode)
            return {"Error": "No book found for this barcode."}
    else:
        logging.warning("Failed to fetch data")
        return {"Error": f"Failed to fetch data. Status code: {response.status_code}"}

if __name__ == "__main__":
    barcode = input("Enter the book barcode (ISBN): ")
    book_info = get_book_info_from_barcode(barcode)
    for key, value in book_info.items():
        print(f"{key}: {value}")
