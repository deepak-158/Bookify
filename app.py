import streamlit as st
import os

BOOKS_FILE = 'data/books.txt'
ISSUED_BOOKS_FILE = 'data/issued_books.txt'

os.makedirs('data', exist_ok=True)

def load_books(file):
    books = {}
    if os.path.exists(file):
        with open(file, 'r') as f:
            for line in f:
                book_id, book_title = line.strip().split(',')
                books[book_id] = book_title
    return books

def save_books(books, file):
    with open(file, 'w') as f:
        for book_id, book_title in books.items():
            f.write(f"{book_id},{book_title}\n")

def load_issued_books(file):
    issued_books = {}
    if os.path.exists(file):
        with open(file, 'r') as f:
            for line in f:
                book_id, student_name, student_id = line.strip().split(',')
                issued_books[book_id] = {"student_name": student_name, "student_id": student_id}
    return issued_books

def save_issued_books(issued_books, file):
    with open(file, 'w') as f:
        for book_id, info in issued_books.items():
            f.write(f"{book_id},{info['student_name']},{info['student_id']}\n")

books = load_books(BOOKS_FILE)
issued_books = load_issued_books(ISSUED_BOOKS_FILE)

st.title("Library Management System")
st.sidebar.title("VIT BHOPAL UNIVERSITY")
st.sidebar.subheader("Central Library ")
option = st.sidebar.radio(
    'Choose an option',
    ('Add a New Book', 'Issue a Book', 'Return a Book', 'Delete a Book', 'Display Available Books', 'Display Issued Books')
)
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
st.sidebar.info("DEEPAK SHUKLA \n 23BCE11422")

left_col, middle_col, right_col = st.columns([1, 2, 1])

if option == 'Add a New Book':
    with middle_col:
        st.header("Add a New Book")
        book_title = st.text_input("Book Title")
        book_id = st.text_input("Book ID")

        if st.button("Add Book"):
            if book_id in books:
                st.error("Book ID already exists!")
            else:
                books[book_id] = book_title
                save_books(books, BOOKS_FILE)
                st.success(f"Book '{book_title}' added successfully!")

elif option == 'Issue a Book':
    with middle_col:
        st.header("Issue a Book")
        issue_book_id = st.text_input("Enter Book ID to Issue")
        student_name = st.text_input("Student Name")
        student_id = st.text_input("Student ID")

        if st.button("Issue Book"):
            if issue_book_id not in books:
                st.error("Book ID not found!")
            elif issue_book_id in issued_books:
                st.error("Book is already issued!")
            else:
                issued_books[issue_book_id] = {"student_name": student_name, "student_id": student_id}
                save_issued_books(issued_books, ISSUED_BOOKS_FILE)
                st.success(f"Book '{books[issue_book_id]}' issued to '{student_name}'!")

elif option == 'Return a Book':
    with middle_col:
        st.header("Return a Book")
        return_book_id = st.text_input("Enter Book ID to Return")

        if st.button("Return Book"):
            if return_book_id not in issued_books:
                st.error("Book ID not found in issued books!")
            else:
                del issued_books[return_book_id]
                save_issued_books(issued_books, ISSUED_BOOKS_FILE)
                st.success("Book returned successfully!")

elif option == 'Delete a Book':
    with middle_col:
        st.header("Delete a Book")
        delete_book_id = st.text_input("Enter Book ID to Delete")

        if st.button("Delete Book"):
            if delete_book_id not in books:
                st.error("Book ID not found!")
            elif delete_book_id in issued_books:
                st.error("Book is currently issued and cannot be deleted!")
            else:
                del books[delete_book_id]
                save_books(books, BOOKS_FILE)
                st.success(f"Book with ID '{delete_book_id}' deleted successfully!")

elif option == 'Display Available Books':
    st.header("Available Books")
    if books:
        for book_id, title in books.items():
            if book_id not in issued_books:
                st.write(f"ID: {book_id}, Title: {title}")
    else:
        st.write("No books available.")

elif option == 'Display Issued Books':
    st.header("Issued Books")
    if issued_books:
        for book_id, info in issued_books.items():
            st.write(f"ID: {book_id}, Title: {books[book_id]}, Issued to: {info['student_name']} (ID: {info['student_id']})")
    else:
        st.write("No books issued.")
