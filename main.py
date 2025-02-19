import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QFormLayout,
    QDialogButtonBox, QScrollArea, QHeaderView
)
from PyQt6.QtCore import Qt
from db_middle import *

class AddBookDialog(QDialog):
    """ Window to add a new book """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Book")
        self.layout = QFormLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.publisher_input = QLineEdit()
        self.date_input = QLineEdit()
        self.description_input = QLineEdit()

        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Author:", self.author_input)
        self.layout.addRow("Publisher:", self.publisher_input)
        self.layout.addRow("Published Date:", self.date_input)
        self.layout.addRow("Description:", self.description_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def get_data(self):
        """ Returns book details as a tuple """
        return (
            self.title_input.text(), self.author_input.text(),
            self.publisher_input.text(), self.date_input.text(),
            self.description_input.text()
        )

class BookDetailsDialog(QDialog):
    """ Window displaying book details """

    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Details")
        layout = QVBoxLayout()

        details = f"""
        <b>Title:</b> {book[1]}<br>
        <b>Author:</b> {", ".join(book[-1])}<br>
        <b>Publisher:</b> {book[2]}<br>
        <b>Published Date:</b> {book[3]}<br>
        <b>Description:</b> {book[4]}
        """
        layout.addWidget(QLabel(details))
        self.setLayout(layout)

class LibraryApp(QMainWindow):
    """ Main window of the library application """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Manager")
        self.setGeometry(100, 100, 600, 400)

        self.books = display_books()
        self.sort_order = {}

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Title", "Author"])
        self.table.setSortingEnabled(False)
        self.table.cellDoubleClicked.connect(self.open_book_details)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_books)
        
        # Adjust column widths dynamically
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.open_add_book_window)

        # Add table to scroll area
        self.scroll_area.setWidget(self.table)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.add_button)

        self.central_widget.setLayout(self.layout)
        self.populate_table()

    def populate_table(self):
        """ Populate the table with books """
        self.table.setRowCount(len(self.books))
        for row, book in enumerate(self.books):
            self.table.setItem(row, 0, QTableWidgetItem(book[1]))
            self.table.setItem(row, 1, QTableWidgetItem(", ".join(book[-1])))

    def sort_books(self, column):
        """ Sort books by column (Title or Author) """
        column_name = "title" if column == 0 else "author"

        # Reverse sorting if already sorted by the same column
        self.sort_order[column_name] = not self.sort_order.get(column_name, False)
        reverse = self.sort_order[column_name]
        self.books.sort(key=lambda x: ", ".join(x[-1]), reverse=reverse)
        self.populate_table()

    def open_add_book_window(self):
        """ Open window to add a book """
        dialog = AddBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            book_data = dialog.get_data()
            new_book = (None, book_data[0], [book_data[1]])
            self.books.append(new_book)
            add_books(book_data[0], book_data[1].split(","))
            self.populate_table()

    def open_book_details(self, row, column):
        """ Open book details when double-clicked """
        book = self.books[row]
        dialog = BookDetailsDialog(book, self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())
