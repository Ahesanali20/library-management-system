"""
Book Management Module for Library System
Handles all book-related operations: add, update, search, display
"""

import streamlit as st
from db_connection import db_connection

class BookManager:
    """Book management operations"""
    
    @staticmethod
    def search_books(search_term="", show_for_sale_only=False):
        """Search books with filters"""
        query = "SELECT * FROM books"
        params = {}
        
        if search_term:
            query += " WHERE title LIKE :search OR author LIKE :search OR isbn LIKE :search"
            params["search"] = f"%{search_term}%"
        
        if show_for_sale_only:
            if "WHERE" in query:
                query += " AND for_sale = 1"
            else:
                query += " WHERE for_sale = 1"
        
        query += " ORDER BY title"
        
        return db_connection.execute_query(query, params)
    
    @staticmethod
    def get_book_by_id(book_id):
        """Get book by ID"""
        query = "SELECT * FROM books WHERE book_id = :book_id"
        result = db_connection.execute_query(query, {"book_id": book_id})
        return result.fetchone()
    
    @staticmethod
    def update_book_quantity(book_id, total_copies, available_copies):
        """Update book quantities"""
        if available_copies > total_copies:
            st.error("Available copies cannot be more than total copies!")
            return False
        
        query = """
            UPDATE books 
            SET total_copies = :total_copies, available_copies = :available_copies
            WHERE book_id = :book_id
        """
        
        params = {
            "total_copies": total_copies,
            "available_copies": available_copies,
            "book_id": book_id
        }
        
        return db_connection.commit_changes(query, params)
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book from the database"""
        try:
            # Check if book has active transactions
            check_query = """
                SELECT COUNT(*) as count
                FROM book_transactions 
                WHERE book_id = :book_id AND status = 'Active'
            """
            result = db_connection.execute_query(check_query, {"book_id": book_id})
            count = result.fetchone().count if result else 0
            
            if count > 0:
                st.error("Cannot delete book with active transactions!")
                return False
            
            # Delete the book
            delete_query = "DELETE FROM books WHERE book_id = :book_id"
            return db_connection.commit_changes(delete_query, {"book_id": book_id})
        except Exception as e:
            st.error(f"Error deleting book: {e}")
            return False
    
    @staticmethod
    def add_book(isbn, title, author, category="", year_published=2024, 
                 total_copies=1, available_copies=1, 
                 for_sale=False, sale_price=0.0):
        """Add new book to database"""
        # Validation
        if not title or not author:
            st.error("Title and Author are required fields!")
            return False
        
        if available_copies > total_copies:
            st.error("Available copies cannot be more than total copies!")
            return False
        
        query = """
            INSERT INTO books 
            (isbn, title, author, category, year_published, 
             total_copies, available_copies, for_sale, sale_price)
            VALUES (:isbn, :title, :author, :category, :year,
                    :total, :available, :sale, :price)
        """
        
        params = {
            "isbn": isbn, "title": title, "author": author, 
            "category": category, "year": year_published,
            "total": total_copies, "available": available_copies,
            "sale": for_sale, "price": sale_price
        }
        
        return db_connection.commit_changes(query, params)
    
    @staticmethod
    def get_books_for_update():
        """Get books list for update dropdown"""
        query = "SELECT book_id, title, author, total_copies, available_copies FROM books ORDER BY title"
        return db_connection.execute_query(query)
    
    @staticmethod
    def get_available_books():
        """Get books available for issuing"""
        query = "SELECT book_id, title, author, available_copies FROM books WHERE available_copies > 0 ORDER BY title"
        return db_connection.execute_query(query)
    
    @staticmethod
    def get_books_for_sale():
        """Get books available for sale with schema detection"""
        try:
            # Try with book_id first (new schema)
            query = "SELECT book_id, title, sale_price FROM books WHERE for_sale = 1 ORDER BY title"
            return db_connection.execute_query(query)
        except:
            # Fallback to id (old schema)
            query = "SELECT id, title, sale_price FROM books WHERE for_sale = 1 ORDER BY title"
            return db_connection.execute_query(query)

def display_books():
    """Display books with search and filters"""
    st.subheader("Book Search - Book Search")
    
    search_term = st.text_input("Search books by title, author, or ISBN:")
    show_for_sale = st.checkbox("Show only books for sale")
    
    result = BookManager.search_books(search_term, show_for_sale)
    if result:
        books = result.fetchall()
        st.write(f"**Found {len(books)} books:**")
        for book in books:
            with st.expander(f"{book.title} - {book.author}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ISBN**: {book.isbn if hasattr(book, 'isbn') else 'N/A'}")
                    st.write(f"**Author**: {book.author}")
                    st.write(f"**Year Published**: {book.publication_year if hasattr(book, 'publication_year') else 'N/A'}")
                with col2:
                    st.write(f"**Category**: {book.category if hasattr(book, 'category') else 'N/A'}")
                    st.write(f"**Total Copies**: {book.total_copies}")
                    st.write(f"**Available**: {book.available_copies}")
                    if hasattr(book, 'for_sale') and book.for_sale:
                        st.write(f"**Sale Price**: ${book.sale_price}")
    else:
        st.info("No books found.")

def add_book_form():
    """Form to add new book"""
    st.subheader("Add New Book - Naya Book Jodein")
    
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            isbn = st.text_input("ISBN:")
            title = st.text_input("Book Title*:")
            author = st.text_input("Author*:")
            category = st.text_input("Category:")
            year_published = st.number_input("Year Published:", min_value=1900, max_value=2030, value=2024)
        
        with col2:
            total_copies = st.number_input("Total Copies*:", min_value=1, value=1)
            available_copies = st.number_input("Available Copies*:", min_value=0, value=1)
            for_sale = st.checkbox("Available for Sale")
            if for_sale:
                sale_price = st.number_input("Sale Price ($):", min_value=0.0, value=0.0, step=0.01)
            else:
                sale_price = 0.0
        
        if st.form_submit_button("Add Book"):
            success = BookManager.add_book(
                isbn, title, author, category, year_published,
                total_copies, available_copies,
                for_sale, sale_price
            )
            
            if success:
                st.success(f"Book '{title}' added successfully!")
                st.rerun()

def update_quantity_form():
    """Form to update book quantity"""
    st.subheader("Update Book Quantity - Book Quantity Badhayein")
    
    result = BookManager.get_books_for_update()
    books = result.fetchall() if result else []
    
    if books:
        with st.form("update_quantity_form"):
            book_options = [f"{book.book_id} - {book.title} by {book.author} (Total: {book.total_copies}, Available: {book.available_copies})" for book in books]
            selected_book = st.selectbox("Select Book to Update:", book_options)
            
            col1, col2 = st.columns(2)
            with col1:
                new_total = st.number_input("New Total Copies:", min_value=0, value=1, step=1)
            with col2:
                new_available = st.number_input("New Available Copies:", min_value=0, value=1, step=1)
            
            if st.form_submit_button("Update Quantity"):
                book_id = int(selected_book.split(" - ")[0])
                
                success = BookManager.update_book_quantity(book_id, new_total, new_available)
                
                if success:
                    st.success(f"Book quantity updated successfully!")
                    st.rerun()
    else:
        st.info("No books found to update.")

def delete_book_form():
    """Form to delete a book from library"""
    st.subheader("Delete Book - Book Delete Karein")
    
    result = BookManager.get_books_for_update()
    books = result.fetchall() if result else []
    
    if books:
        with st.form("delete_book_form"):
            book_options = [f"{book.book_id} - {book.title} by {book.author} (Available: {book.available_copies})" for book in books]
            selected_book = st.selectbox("Select Book to Delete:", book_options)
            
            st.warning("⚠️ Warning: This action cannot be undone!")
            confirm = st.checkbox("I understand and want to delete this book")
            
            if st.form_submit_button("Delete Book") and confirm:
                book_id = int(selected_book.split(" - ")[0])
                
                success = BookManager.delete_book(book_id)
                
                if success:
                    st.success("Book deleted successfully!")
                    st.rerun()
    else:
        st.info("No books found to delete.")

def book_management_page():
    """Main book management page"""
    st.header("Book Management - Book Management")
    
    # Display books
    display_books()
    
    # Add new book form
    add_book_form()
    
    # Update quantity form
    update_quantity_form()
    
    # Delete book form
    delete_book_form()
