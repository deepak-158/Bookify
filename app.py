import streamlit as st
import os


st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
    }
    .sidebar .sidebar-content {
        background-color: #2C3E50;
        color: white;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .highlight {
        background-color: #EBF5FB;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .book-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

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
# Main app structure
st.markdown("<h1 style='text-align: center; color: #2C3E50; margin-bottom: 0;'>📚 Bookify</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #3498DB; margin-top: 0;'>Library Management System</h3>", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("<h1 style='color: #3498DB; text-align: left;'>OPTIONS</h1>", unsafe_allow_html=True)
   
    st.markdown("</div>", unsafe_allow_html=True)
    
    option = st.radio(
        'Menu',
        ('Add a New Book', 'Issue a Book', 'Return a Book', 
         'Delete a Book', 'Available Books', 'Issued Books'),
        label_visibility='collapsed'
    )
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #BDC3C7;'>", unsafe_allow_html=True)
    st.caption("Developed by Deepak Shukla")
    st.caption("23BCE11422")
    st.markdown("</div>", unsafe_allow_html=True)


container = st.container()

if option == 'Add a New Book':
    with container:
        st.subheader("📖 Add New Book")
        with st.form("add_book_form"):
            cols = st.columns(2)
            book_id = cols[0].text_input("Book ID")
            book_title = cols[1].text_input("Book Title")
            
            if st.form_submit_button("➕ Add Book"):
                if book_id in books:
                    st.error("❌ Book ID already exists!")
                else:
                    books[book_id] = book_title
                    save_books(books, BOOKS_FILE)
                    st.success(f"✅ Successfully added '{book_title}'!")

elif option == 'Issue a Book':
    with container:
        st.subheader("🎒 Issue Book")
        with st.expander("Issue a Book to Student", expanded=True):
            with st.form("issue_form"):
                cols = st.columns([2,1,1])
                book_id = cols[0].text_input("Book ID")
                student_name = cols[1].text_input("Student Name")
                student_id = cols[2].text_input("Student ID")
                
                if st.form_submit_button("📤 Issue Book"):
                    if book_id not in books:
                        st.error("❌ Book not found!")
                    elif book_id in issued_books:
                        st.error("⚠️ Book already issued!")
                    else:
                        issued_books[book_id] = {
                            "student_name": student_name,
                            "student_id": student_id
                        }
                        save_issued_books(issued_books, ISSUED_BOOKS_FILE)
                        st.success(f"✅ Issued '{books[book_id]}' to {student_name}")

elif option == 'Return a Book':
    with container:
        st.subheader("📥 Return Book")
        with st.form("return_form"):
            book_id = st.text_input("Enter Book ID to Return")
            
            if st.form_submit_button("🔄 Return Book"):
                if book_id not in issued_books:
                    st.error("❌ Book not issued!")
                else:
                    del issued_books[book_id]
                    save_issued_books(issued_books, ISSUED_BOOKS_FILE)
                    st.success("✅ Book returned successfully!")

elif option == 'Delete a Book':
    with container:
        st.subheader("🗑️ Delete Book")
        with st.form("delete_form"):
            book_id = st.text_input("Enter Book ID to Delete")
            
            if st.form_submit_button("❌ Delete Book"):
                if book_id not in books:
                    st.error("🚫 Book not found!")
                elif book_id in issued_books:
                    st.error("⚠️ Cannot delete issued book!")
                else:
                    del books[book_id]
                    save_books(books, BOOKS_FILE)
                    st.success("✅ Book deleted successfully!")

elif option == 'Available Books':
    with container:
        st.subheader("📚 Available Books")
        if books:
            for book_id, title in books.items():
                if book_id not in issued_books:
                    st.markdown(f"""
                    <div class="book-card">
                        <b>ID:</b> {book_id}<br>
                        <b>Title:</b> {title}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No books available in the library")

elif option == 'Issued Books':
    with container:
        st.subheader("📖 Issued Books")
        if issued_books:
            for book_id, details in issued_books.items():
                st.markdown(f"""
                <div class="book-card">
                    <b>ID:</b> {book_id}<br>
                    <b>Title:</b> {books.get(book_id, 'Unknown')}<br>
                    <b>Issued to:</b> {details['student_name']} ({details['student_id']})
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No books currently issued")