"""
Simple AI Assistant - Google-like responses for Library System
"""

import streamlit as st
from sqlalchemy import text
from db_connection import db_connection

class SimpleAI:
    """Simple Google-like AI assistant"""
    
    @staticmethod
    def search_books(query):
        """Search books in database"""
        try:
            search_term = f"%{query}%"
            result = db_connection.execute_query(
                "SELECT title, author, available_copies FROM books WHERE title LIKE :search OR author LIKE :search LIMIT 5",
                {"search": search_term}
            )
            if result:
                books = result.fetchall()
                if books:
                    response = "**Books Found:**\n\n"
                    for book in books:
                        response += f"**{book.title}** by {book.author} (Available: {book.available_copies})\n"
                    return response
            return None
        except:
            return None
    
    @staticmethod
    def search_members(query):
        """Search members in database"""
        try:
            search_term = f"%{query}%"
            result = db_connection.execute_query(
                "SELECT name, member_id, member_type, department FROM library_members WHERE name LIKE :search AND status = 'Active' LIMIT 5",
                {"search": search_term}
            )
            if result:
                members = result.fetchall()
                if members:
                    response = "**Members Found:**\n\n"
                    for member in members:
                        response += f"**{member.name}** ({member.member_id}) - {member.member_type}, {member.department}\n"
                    return response
            return None
        except:
            return None
    
    @staticmethod
    def get_mca_faculty():
        """Get MCA faculty members"""
        try:
            result = db_connection.execute_query(
                "SELECT name, member_id, email FROM library_members WHERE department LIKE '%MCA%' AND member_type = 'Faculty' AND status = 'Active'"
            )
            if result:
                faculty = result.fetchall()
                if faculty:
                    response = "**MCA Faculty Members:**\n\n"
                    for f in faculty:
                        response += f"**{f.name}** ({f.member_id}) - {f.email}\n"
                    return response
            return None
        except:
            return None
    
    @staticmethod
    def get_response(user_input):
        """Get Google-like response"""
        query_lower = user_input.lower()
        
        # Check for MCA faculty
        if 'mca faculty' in query_lower or 'mca' in query_lower and 'faculty' in query_lower:
            mca_result = SimpleAI.get_mca_faculty()
            if mca_result:
                return f"{mca_result}\n\n**For operations, use the forms in the sidebar.**"
            else:
                return "**No MCA faculty found.** Use 'Members' page to add faculty members."
        
        # Check for book searches
        if any(word in query_lower for word in ['book', 'books', 'kitab', 'search', 'find', 'available']):
            book_result = SimpleAI.search_books(user_input)
            if book_result:
                return f"{book_result}\n\n**To issue any book, use 'Issue Book' form in sidebar.**"
            else:
                return "**No books found.** Try searching with book title or author name.\n\n**Example:** 'Introduction to Algorithms' or 'Computer Science'"
        
        # Check for member searches
        if any(word in query_lower for word in ['member', 'members', 'student', 'faculty', 'teacher']):
            member_result = SimpleAI.search_members(user_input)
            if member_result:
                return f"{member_result}\n\n**Use 'Members' page for member management.**"
            else:
                return "**No members found.** Try searching with member name.\n\n**Example:** 'Rahul' or 'faculty'"
        
        # Check for issue/return operations
        if any(word in query_lower for word in ['issue', 'leni', 'borrow', 'take']):
            return "**To issue a book:**\n\n1. Go to 'Transactions' page\n2. Use 'Issue Book' form\n3. Select book and member\n4. Click 'Issue Book'\n\n**Need help finding a book? Ask me!**"
        
        if any(word in query_lower for word in ['return', 'wapis', 'give back']):
            return "**To return a book:**\n\n1. Go to 'Transactions' page\n2. Use 'Return Book' form\n3. Select active transaction\n4. Click 'Return Book'"
        
        # Check for sales
        if any(word in query_lower for word in ['sell', 'sale', 'buy', 'purchase', 'price']):
            return "**For book sales:**\n\n1. Go to 'Book Sales' page\n2. Select book and customer\n3. Choose payment method\n4. Click 'Sell Book'"
        
        # Check for help
        if any(word in query_lower for word in ['help', 'kaise', 'how', 'guide']):
            return """**Library System Help:**

**Books:**
- Search: Ask me "Computer Science books"
- Issue: Use 'Transactions' > 'Issue Book'
- Return: Use 'Transactions' > 'Return Book'

**Members:**
- Search: Ask me "faculty members" or "students"
- Add: Use 'Members' page
- History: Use 'Member History' page

**Sales:**
- Sell books: Use 'Book Sales' page

**Ask me anything in Hindi or English!**"""
        
        # Default response
        return """**How can I help you?**

**Try asking:**
- "MCA faculty members"
- "Computer Science books"
- "How to issue a book?"
- "Available books"
- "Help"

**I understand Hindi and English!**"""

def ai_assistant_page():
    """Main AI assistant page"""
    st.header("AI Library Assistant")
    
    st.info("Google-like Assistant - Ask me anything about the library!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = SimpleAI.get_response(user_input)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
