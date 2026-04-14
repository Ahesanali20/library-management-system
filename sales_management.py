"""
Sales Management Module for Library System
Handles book sales operations and payment tracking
"""

import streamlit as st
from db_connection import db_connection
from book_management import BookManager
from member_management import MemberManager

class SalesManager:
    """Sales management operations"""
    
    @staticmethod
    def sell_book(book_id, member_id=None, quantity=1):
        """Sell a book to customer"""
        try:
            # Get book details
            book = BookManager.get_book_by_id(book_id)
            if not book or not book.for_sale:
                st.error("Book not available for sale!")
                return False
            
            if book.available_copies < quantity:
                st.error(f"Not enough copies available! Only {book.available_copies} copies available.")
                return False
            
            # Calculate total price
            total_price = book.sale_price * quantity
            
            # Create sales record
            query = """
                INSERT INTO book_sales 
                (book_id, member_id, quantity, price)
                VALUES (:book_id, :member_id, :quantity, :price)
            """
            
            params = {
                "book_id": book_id, 
                "member_id": member_id, 
                "quantity": quantity, 
                "price": total_price
            }
            
            if not db_connection.commit_changes(query, params):
                return False
            
            # Update book quantity
            update_query = """
                UPDATE books 
                SET available_copies = available_copies - :quantity
                WHERE book_id = :book_id
            """
            
            return db_connection.commit_changes(update_query, {"quantity": quantity, "book_id": book_id})
            
        except Exception as e:
            st.error(f"Error selling book: {e}")
            return False
    
    @staticmethod
    def get_books_for_sale():
        """Get books available for sale"""
        return BookManager.get_books_for_sale()
    
    @staticmethod
    def get_sales_history(search_term=""):
        """Get sales history with search"""
        query = """
            SELECT bs.sale_id, b.title, bs.sale_date, bs.price, bs.quantity
            FROM book_sales bs
            JOIN books b ON bs.book_id = b.book_id
        """
        params = {}
        
        if search_term:
            query += " WHERE b.title LIKE :search"
            params["search"] = f"%{search_term}%"
        
        query += " ORDER BY bs.sale_date DESC"
        
        return db_connection.execute_query(query, params)
    
    @staticmethod
    def get_sales_summary():
        """Get sales summary statistics with schema detection"""
        try:
            # Try with price column first (new schema)
            total_sales_query = """
                SELECT SUM(price) as total_sales, COUNT(*) as total_transactions
                FROM book_sales
            """
            result = db_connection.execute_query(total_sales_query)
            summary = result.fetchone()
            
            # Books sold today
            today_sales_query = """
                SELECT COUNT(*) as today_sales
                FROM book_sales 
                WHERE DATE(sale_date) = CURDATE()
            """
            today_result = db_connection.execute_query(today_sales_query)
            today_sales = today_result.fetchone().today_sales
            
            return {
                'total_sales': summary.total_sales or 0,
                'total_transactions': summary.total_transactions or 0,
                'today_sales': today_sales or 0
            }
        except Exception as e:
            # Fallback to total_amount column (old schema)
            try:
                total_sales_query = """
                    SELECT SUM(total_amount) as total_sales, COUNT(*) as total_transactions
                    FROM book_sales 
                    WHERE payment_status = 'Paid'
                """
                result = db_connection.execute_query(total_sales_query)
                summary = result.fetchone()
                
                today_sales_query = """
                    SELECT COUNT(*) as today_sales
                    FROM book_sales 
                    WHERE DATE(sale_date) = CURDATE() AND payment_status = 'Paid'
                """
                today_result = db_connection.execute_query(today_sales_query)
                today_sales = today_result.fetchone().today_sales
                
                return {
                    'total_sales': summary.total_sales or 0,
                    'total_transactions': summary.total_transactions or 0,
                    'today_sales': today_sales or 0
                }
            except Exception as e2:
                st.error(f"Sales Summary Error: {e} / {e2}")
                return {'total_sales': 0, 'total_transactions': 0, 'today_sales': 0}

def sell_book_form():
    """Form to sell a book"""
    st.subheader("Sell Book - Book Sell")
    
    books_result = SalesManager.get_books_for_sale()
    members_result = MemberManager.get_active_members()
    books = books_result.fetchall() if books_result else []
    members = members_result.fetchall() if members_result else []
    
    if books:
        with st.form("sell_book_form"):
            book_options = [f"{book.book_id} - {book.title} (${book.sale_price})" for book in books]
            member_options = [f"{member.member_id} - {member.name}" for member in members]
            member_options.insert(0, "Non-Member Customer")
            
            selected_book = st.selectbox("Select Book:", book_options)
            selected_member = st.selectbox("Select Customer:", member_options)
            quantity = st.number_input("Quantity:", min_value=1, value=1, step=1)
            
            if st.form_submit_button("Sell Book"):
                book_id = int(selected_book.split(" - ")[0])
                
                # Get member ID if selected
                member_id = None
                if selected_member != "Non-Member Customer":
                    member_id = int(selected_member.split(" - ")[0])
                
                success = SalesManager.sell_book(
                    book_id, member_id, quantity=quantity
                )
                
                if success:
                    book = BookManager.get_book_by_id(book_id)
                    total_price = book.sale_price * quantity
                    st.success(f"Book sold successfully! Total: ${total_price}")
                    st.rerun()
    else:
        st.info("No books available for sale.")

def display_sales_history():
    """Display sales history"""
    st.subheader("Sales History - Sales History")
    
    search_term = st.text_input("Search sales:")
    
    if search_term:
        result = SalesManager.get_sales_history(search_term)
        sales = result.fetchall() if result else []
        
        if sales:
            st.write(f"**Found {len(sales)} sales:**")
            for sale in sales:
                st.write(f"**ID: {sale.sale_id}** - {sale.title} sold on {sale.sale_date} - Quantity: {sale.quantity} - Price: ${sale.price}")
        else:
            st.info("No sales found.")

def display_sales_summary():
    """Display sales summary dashboard"""
    st.subheader("Sales Summary - Sales Summary")
    
    summary = SalesManager.get_sales_summary()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sales", f"${summary['total_sales']:.2f}")
    
    with col2:
        st.metric("Total Transactions", summary['total_transactions'])
    
    with col3:
        st.metric("Today's Sales", summary['today_sales'])

def sales_management_page():
    """Main sales management page"""
    st.header("Book Sales - Book Sales")
    
    # Sales summary
    display_sales_summary()
    
    # Sell book form
    sell_book_form()
    
    # Sales history
    display_sales_history()
