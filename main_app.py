"""
Main Library Management Application
Modular structure with separate files for each functionality
Multi-database support with dynamic connection switching
"""

import streamlit as st
from sqlalchemy import text

# Import database configuration
from database_config import database_login_page, is_database_connected, get_database_connection

# Import all modules
from db_connection import db_connection
from book_management import book_management_page
from member_management import member_management_page, member_history_page
from transaction_management import transaction_management_page
from sales_management import sales_management_page
from ai_assistant_groq import ai_assistant_page

# PAGE CONFIG
st.set_page_config(page_title="LJ University Library Management", layout="wide")

# Check if database is connected
if not is_database_connected():
    database_login_page()
    st.stop()  # Stop here if not connected


# -----------------------------
# UI HEADER
# -----------------------------
st.title("Library Management System")
st.markdown("### LJ University Library Management System (Modular Version)")

# -----------------------------
# SIDEBAR NAVIGATION
# ----
st.sidebar.title("Navigation")

# Database info section
db_config = get_database_connection()
if db_config:
    st.sidebar.info(f"""
    **📊 Connected Database:**
    - **Host:** {db_config.get('host')}
    - **Database:** {db_config.get('name')}
    - **User:** {db_config.get('user')}
    """)
    
    if st.sidebar.button("🔄 Switch Database", use_container_width=True):
        st.session_state.db_config = None
        st.rerun()
    
    st.sidebar.divider()

page = st.sidebar.selectbox("Choose Page", [
    "AI Assistant",
    "Dashboard", 
    "Books", 
    "Members", 
    "Transactions", 
    "Book Sales",
    "Member History"
])

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
def dashboard_page():
    """Main dashboard with search functionality"""
    st.header("Dashboard")
    
    # Show all available databases from MySQL
    st.subheader("📚 Available Databases")
    
    # Get current database config
    db_config = get_database_connection()
    if db_config:
        st.info(f"📊 **Currently Connected:** {db_config.get('name')}")
    
    # Fetch all databases from MySQL
    try:
        from database_config import DatabaseConfig
        if db_config:
            all_dbs = DatabaseConfig.get_all_databases(
                db_config.get('host'),
                db_config.get('user'),
                db_config.get('password'),
                db_config.get('port')
            )
        else:
            all_dbs = []
        
        if all_dbs:
            st.write(f"**Found {len(all_dbs)} databases:**")
            # Display in a grid
            cols = st.columns(3)
            for idx, db_name in enumerate(all_dbs):
                with cols[idx % 3]:
                    with st.container(border=True):
                        # Add emoji based on database name
                        emoji = "�"
                        if "history" in db_name.lower():
                            emoji = "🏛️"
                        elif "programming" in db_name.lower() or "code" in db_name.lower():
                            emoji = "💻"
                        elif "novel" in db_name.lower() or "fiction" in db_name.lower():
                            emoji = "📖"
                        elif "library" in db_name.lower():
                            emoji = "📖"
                        
                        st.write(f"**{emoji} {db_name}**")
                        is_current = db_config and db_name == db_config.get('name')
                        if is_current:
                            st.caption("✅ Currently Connected")
                        else:
                            st.caption("Available")
        else:
            st.info("No databases found in MySQL server.")
    except Exception as e:
        st.error(f"Error fetching databases: {e}")
    
    st.divider()
    
    # Search functionality
    st.subheader("Search")
    search_category = st.selectbox("Search Category", ["Books", "Members", "Transactions", "Sales"])
    search_term = st.text_input("Enter search term:")
    
    if search_term:
        try:
            if search_category == "Books":
                from book_management import BookManager
                result = BookManager.search_books(search_term)
                books = result.fetchall() if result else []
                
                if books:
                    st.write(f"**Found {len(books)} books:**")
                    for book in books:
                        sale_info = f" (For Sale: ${book.sale_price})" if book.for_sale else ""
                        st.write(f"**{book.title}** by {book.author} - ISBN: {book.isbn} - Available: {book.available_copies}{sale_info}")
                else:
                    st.info("No books found.")
            
            elif search_category == "Members":
                from member_management import MemberManager
                result = MemberManager.search_members(search_term)
                members = result.fetchall() if result else []
                
                if members:
                    st.write(f"**Found {len(members)} members:**")
                    for member in members:
                        st.write(f"**{member.name}** - ID: {member.member_id} - Type: {member.member_type} - Dept: {member.department}")
                else:
                    st.info("No members found.")
            
            elif search_category == "Transactions":
                from transaction_management import TransactionManager
                result = TransactionManager.search_transactions(search_term)
                transactions = result.fetchall() if result else []
                
                if transactions:
                    st.write(f"**Found {len(transactions)} transactions:**")
                    for trans in transactions:
                        st.write(f"**ID: {trans.transaction_id}** - {trans.title} issued to {trans.name} on {trans.issue_date} - Status: {trans.status}")
                else:
                    st.info("No transactions found.")
            
            elif search_category == "Sales":
                from sales_management import SalesManager
                result = SalesManager.get_sales_history(search_term)
                sales = result.fetchall() if result else []
                
                if sales:
                    st.write(f"**Found {len(sales)} sales:**")
                    for sale in sales:
                        st.write(f"**ID: {sale.sale_id}** - {sale.title} sold on {sale.sale_date} - Amount: ${sale.price}")
                else:
                    st.info("No sales found.")
        
        except Exception as e:
            st.error(f"Database Error: {e}")


# -----------------------------
# PAGE ROUTING
# -----------------------------
if page == "AI Assistant":
    ai_assistant_page()

elif page == "Dashboard":
    dashboard_page()

elif page == "Books":
    book_management_page()

elif page == "Members":
    member_management_page()

elif page == "Transactions":
    transaction_management_page()

elif page == "Book Sales":
    sales_management_page()

elif page == "Member History":
    member_history_page()
