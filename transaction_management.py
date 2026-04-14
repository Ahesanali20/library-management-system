"""
Transaction Management Module for Library System
Handles book issue, return, and renewal operations
"""

import streamlit as st
from datetime import datetime, timedelta
from db_connection import db_connection
from book_management import BookManager
from member_management import MemberManager

class TransactionManager:
    """Transaction management operations"""
    
    @staticmethod
    def issue_book(book_id, member_id, days=7):
        """Issue a book to a member"""
        try:
            # Check book availability
            book = BookManager.get_book_by_id(book_id)
            if not book or book.available_copies <= 0:
                st.error("Book not available for issue!")
                return False
            
            # Update book availability
            update_query = """
                UPDATE books 
                SET available_copies = available_copies - 1 
                WHERE book_id = :book_id AND available_copies > 0
            """
            if not db_connection.commit_changes(update_query, {"book_id": book_id}):
                return False
            
            # Create transaction record
            transaction_query = """
                INSERT INTO book_transactions 
                (book_id, member_id, status)
                VALUES (:book_id, :member_id, 'Active')
            """
            
            params = {
                "book_id": book_id, 
                "member_id": member_id
            }
            
            return db_connection.commit_changes(transaction_query, params)
            
        except Exception as e:
            st.error(f"Error issuing book: {e}")
            return False
    
    @staticmethod
    def return_book(transaction_id):
        """Return a book"""
        try:
            # Get transaction details
            trans_query = """
                SELECT book_id, member_id 
                FROM book_transactions 
                WHERE transaction_id = :transaction_id AND status = 'Active'
            """
            result = db_connection.execute_query(trans_query, {"transaction_id": transaction_id})
            
            if not result:
                st.error("Invalid transaction!")
                return False
            
            trans = result.fetchone()
            
            # Update book availability
            update_query = """
                UPDATE books 
                SET available_copies = available_copies + 1 
                WHERE book_id = :book_id
            """
            if not db_connection.commit_changes(update_query, {"book_id": trans.book_id}):
                return False
            
            # Update transaction
            transaction_query = """
                UPDATE book_transactions 
                SET return_date = CURRENT_TIMESTAMP, status = 'Returned'
                WHERE transaction_id = :transaction_id
            """
            
            return db_connection.commit_changes(transaction_query, {"transaction_id": transaction_id})
            
        except Exception as e:
            st.error(f"Error returning book: {e}")
            return False
    
    @staticmethod
    def get_active_transactions():
        """Get all active transactions with dynamic schema detection"""
        try:
            # Try with transaction_id first (new schema)
            query = """
                SELECT bt.transaction_id, b.title, lm.name, bt.issue_date, bt.return_date
                FROM book_transactions bt
                JOIN books b ON bt.book_id = b.book_id
                JOIN library_members lm ON bt.member_id = lm.member_id
                WHERE bt.status = 'Active'
                ORDER BY bt.issue_date
            """
            return db_connection.execute_query(query)
        except:
            # Fallback to id (old schema)
            query = """
                SELECT bt.id, b.title, lm.name, bt.issue_date, bt.return_date
                FROM book_transactions bt
                JOIN books b ON bt.book_id = b.book_id
                JOIN library_members lm ON bt.member_id = lm.member_id
                WHERE bt.status = 'Active'
                ORDER BY bt.issue_date
            """
            return db_connection.execute_query(query)
    
    @staticmethod
    def search_transactions(search_term=""):
        """Search transactions with dynamic schema detection"""
        try:
            # Try with transaction_id first (new schema)
            query = """
                SELECT bt.transaction_id, b.title, lm.name, bt.issue_date, bt.return_date, bt.status
                FROM book_transactions bt
                JOIN books b ON bt.book_id = b.book_id
                JOIN library_members lm ON bt.member_id = lm.member_id
            """
            params = {}
            
            if search_term:
                query += " WHERE bt.status LIKE :search OR b.title LIKE :search OR lm.name LIKE :search"
                params["search"] = f"%{search_term}%"
            
            query += " ORDER BY bt.issue_date DESC"
            
            return db_connection.execute_query(query, params)
        except:
            # Fallback to id (old schema)
            query = """
                SELECT bt.id, b.title, lm.name, bt.issue_date, bt.return_date, bt.status
                FROM book_transactions bt
                JOIN books b ON bt.book_id = b.book_id
                JOIN library_members lm ON bt.member_id = lm.member_id
            """
            params = {}
            
            if search_term:
                query += " WHERE bt.status LIKE :search OR b.title LIKE :search OR lm.name LIKE :search"
                params["search"] = f"%{search_term}%"
            
            query += " ORDER BY bt.issue_date DESC"
            
            return db_connection.execute_query(query, params)

def issue_book_form():
    """Form to issue a book"""
    st.subheader("Issue Book - Book Issue")
    
    books_result = BookManager.get_available_books()
    members_result = MemberManager.get_active_members()
    books = books_result.fetchall() if books_result else []
    members = members_result.fetchall() if members_result else []
    
    if books and members:
        with st.form("issue_book_form"):
            book_options = [f"{book.book_id} - {book.title} by {book.author} ({book.available_copies} available)" for book in books]
            member_options = [f"{member.member_id} - {member.name}" for member in members]
            
            selected_book = st.selectbox("Select Book:", book_options)
            selected_member = st.selectbox("Select Member:", member_options)
            days = st.number_input("Number of Days:", min_value=1, value=7, step=1)
            
            if st.form_submit_button("Issue Book"):
                book_id = int(selected_book.split(" - ")[0])
                member_id = int(selected_member.split(" - ")[0])
                
                success = TransactionManager.issue_book(book_id, member_id, days)
                
                if success:
                    st.success("Book issued successfully!")
                    st.rerun()
    else:
        st.warning("No available books or active members found.")

def return_book_form():
    """Form to return a book"""
    st.subheader("Return Book - Book Return")
    
    active_trans_result = TransactionManager.get_active_transactions()
    active_transactions = active_trans_result.fetchall() if active_trans_result else []
    
    if active_transactions:
        with st.form("return_book_form"):
            transaction_options = [
                f"{trans.transaction_id} - {trans.title} issued to {trans.name} (Issued: {trans.issue_date})" 
                for trans in active_transactions
            ]
            selected_transaction = st.selectbox("Select Transaction to Return:", transaction_options)
            
            if st.form_submit_button("Return Book"):
                transaction_id = int(selected_transaction.split(" - ")[0])
                
                success = TransactionManager.return_book(transaction_id)
                
                if success:
                    st.success("Book returned successfully!")
                    st.rerun()
    else:
        st.info("No active transactions found.")

def display_transactions():
    """Display transaction search results"""
    st.subheader("Search Transactions - Transaction Search")
    
    search_term = st.text_input("Enter search term:")
    
    if search_term:
        result = TransactionManager.search_transactions(search_term)
        transactions = result.fetchall() if result else []
        
        if transactions:
            st.write(f"**Found {len(transactions)} transactions:**")
            for trans in transactions:
                st.write(f"**ID: {trans.transaction_id}** - {trans.title} issued to {trans.name} on {trans.issue_date} - Status: {trans.status}")
        else:
            st.info("No transactions found.")

def transaction_management_page():
    """Main transaction management page"""
    st.header("Transaction Management - Transaction Management")
    
    # Issue book form
    issue_book_form()
    
    # Return book form
    return_book_form()
    
    # Display transactions
    display_transactions()
