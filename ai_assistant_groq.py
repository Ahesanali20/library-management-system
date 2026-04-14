"""
AI Assistant using Groq API (Llama3)
Free, fast AI for Library System
"""

import streamlit as st
import os
from groq import Groq
from db_connection import db_connection

class GroqAI:
    """Groq-powered AI assistant using Llama3"""
    
    def __init__(self):
        self.client = None
        self.model = "llama-3.1-8b-instant"  # Free Llama3 model
        
    def initialize(self):
        """Initialize Groq client with API key"""
        # Priority: Session state > Environment variable
        api_key = None
        
        # Check session state first (sidebar input)
        if "groq_api_key" in st.session_state and st.session_state["groq_api_key"]:
            api_key = st.session_state["groq_api_key"]
        
        # Fall back to environment variable
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return False
        
        try:
            self.client = Groq(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Groq initialization error: {e}")
            return False
    
    def search_books(self, query):
        """Search books in database"""
        try:
            query_lower = query.lower()
            
            # Check for price queries
            import re
            # Match patterns like "under 50", "less than 50", "50 se kam", "above 50", "50 se jyada"
            if re.search(r'(\d+)\s*(price|prices|rs|rupees|\$|dollar|under|below|above|more|less|kam|jyada|zyada|se)', query_lower):
                # Extract the number
                num_match = re.search(r'(\d+)', query_lower)
                if num_match:
                    num = int(num_match.group(1))
                    
                    # Check if asking for price filtering
                    if 'price' in query_lower or 'prices' in query_lower or 'rs' in query_lower or 'rupees' in query_lower or '$' in query_lower or 'dollar' in query_lower:
                        if 'kam' in query_lower or 'less' in query_lower or 'under' in query_lower or 'below' in query_lower:
                            # Books with price less than X
                            result = db_connection.execute_query(
                                "SELECT title, author, sale_price, isbn FROM books WHERE sale_price <= :num AND for_sale = 1 LIMIT 50",
                                {"num": num}
                            )
                        elif 'jyada' in query_lower or 'zyada' in query_lower or 'more' in query_lower or 'above' in query_lower:
                            # Books with price more than X
                            result = db_connection.execute_query(
                                "SELECT title, author, sale_price, isbn FROM books WHERE sale_price >= :num AND for_sale = 1 LIMIT 50",
                                {"num": num}
                            )
                        else:
                            # Books with exact price
                            result = db_connection.execute_query(
                                "SELECT title, author, sale_price, isbn FROM books WHERE sale_price = :num AND for_sale = 1 LIMIT 50",
                                {"num": num}
                            )
                    else:
                        # Check for copy count queries
                        if 'jyada' in query_lower or 'zyada' in query_lower or 'more' in query_lower:
                            # Books with more than X copies
                            result = db_connection.execute_query(
                                "SELECT title, author, available_copies, isbn FROM books WHERE available_copies >= :num LIMIT 50",
                                {"num": num}
                            )
                        elif 'kam' in query_lower or 'less' in query_lower:
                            # Books with less than X copies
                            result = db_connection.execute_query(
                                "SELECT title, author, available_copies, isbn FROM books WHERE available_copies <= :num LIMIT 50",
                                {"num": num}
                            )
                        else:
                            # Books with exactly X copies
                            result = db_connection.execute_query(
                                "SELECT title, author, available_copies, isbn FROM books WHERE available_copies = :num LIMIT 50",
                                {"num": num}
                            )
                else:
                    # Fallback to all books if number not found
                    result = db_connection.execute_query(
                        "SELECT title, author, available_copies, isbn FROM books LIMIT 50"
                    )
            # If query is asking for all books, return all
            elif any(word in query_lower for word in ['all', 'sabhi', 'saare', 'sare', 'every', 'list', 'show', 'dikhao', 'dikhaiye']):
                result = db_connection.execute_query(
                    "SELECT title, author, available_copies, isbn FROM books LIMIT 50"
                )
            else:
                # Otherwise search by title/author
                search_term = f"%{query}%"
                result = db_connection.execute_query(
                    "SELECT title, author, available_copies, isbn FROM books WHERE title LIKE :search OR author LIKE :search LIMIT 10",
                    {"search": search_term}
                )
            
            if result:
                books = result.fetchall()
                if books:
                    response = f"**{len(books)} Books Found:**\n\n"
                    for book in books:
                        # Check if sale_price exists (for price queries)
                        if hasattr(book, 'sale_price') and book.sale_price is not None:
                            response += f"- **{book.title}** by {book.author} (ISBN: {book.isbn}, Price: ${book.sale_price})\n"
                        else:
                            response += f"- **{book.title}** by {book.author} (ISBN: {book.isbn}, Available: {book.available_copies})\n"
                    return response
                else:
                    return "**No books found in database.**"
            return "**No books found in database.**"
        except Exception as e:
            return f"**Database error:** {str(e)}"
    
    def search_members(self, query):
        """Search members in database"""
        try:
            query_lower = query.lower()
            
            # If query is asking for all members, return all
            if any(word in query_lower for word in ['all', 'sabhi', 'saare', 'sare', 'every', 'list', 'show', 'naam']):
                result = db_connection.execute_query(
                    "SELECT name, member_id, member_type, department, email FROM library_members WHERE status = 'Active' LIMIT 50"
                )
            else:
                # Otherwise search by name
                search_term = f"%{query}%"
                result = db_connection.execute_query(
                    "SELECT name, member_id, member_type, department, email FROM library_members WHERE name LIKE :search AND status = 'Active' LIMIT 10",
                    {"search": search_term}
                )
            
            if result:
                members = result.fetchall()
                if members:
                    response = f"**{len(members)} Members Found:**\n\n"
                    for member in members:
                        response += f"- **{member.name}** (ID: {member.member_id}) - {member.member_type}, {member.department}\n"
                    return response
                else:
                    return "**No active members found in database.**"
            return "**No active members found in database.**"
        except Exception as e:
            return f"**Database error:** {str(e)}"
    
    def get_mca_faculty(self):
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
                        response += f"- **{f.name}** (ID: {f.member_id}) - {f.email}\n"
                    return response
            return None
        except:
            return None
    
    def get_departments(self):
        """Get all departments from database"""
        try:
            result = db_connection.execute_query(
                "SELECT DISTINCT department FROM library_members WHERE department IS NOT NULL AND department != '' ORDER BY department"
            )
            if result:
                departments = result.fetchall()
                if departments:
                    response = f"**{len(departments)} Departments Found:**\n\n"
                    for dept in departments:
                        response += f"- **{dept.department}**\n"
                    return response
            return "**No departments found in database.**"
        except Exception as e:
            return f"**Database error:** {str(e)}"
    
    def search_members_by_department(self, department_name):
        """Search members by department"""
        try:
            search_term = f"%{department_name}%"
            result = db_connection.execute_query(
                "SELECT name, member_id, member_type, department, email FROM library_members WHERE department LIKE :search AND status = 'Active'",
                {"search": search_term}
            )
            if result:
                members = result.fetchall()
                if members:
                    response = f"**{len(members)} Members in {department_name.title()} Department:**\n\n"
                    for member in members:
                        response += f"- **{member.name}** (ID: {member.member_id}) - {member.member_type}, {member.email}\n"
                    return response
                else:
                    return f"**No members found in {department_name.title()} department.**"
            return f"**No members found in {department_name.title()} department.**"
        except Exception as e:
            return f"**Database error:** {str(e)}"
    
    def get_database_context(self):
        """Get current database context for AI"""
        try:
            # Get basic stats
            books_count = db_connection.execute_query("SELECT COUNT(*) as count FROM books")
            members_count = db_connection.execute_query("SELECT COUNT(*) as count FROM library_members WHERE status = 'Active'")
            
            # Get sample books for context
            books_sample = db_connection.execute_query("SELECT title, author, category FROM books LIMIT 5")
            # Get sample departments
            dept_sample = db_connection.execute_query("SELECT DISTINCT department FROM library_members WHERE department IS NOT NULL LIMIT 5")
            
            books_num = books_count.fetchone().count if books_count else 0
            members_num = members_count.fetchone().count if members_count else 0
            
            books_list = ""
            if books_sample:
                books_list = "\nSample Books:\n"
                for book in books_sample.fetchall():
                    books_list += f"- {book.title} by {book.author} ({book.category})\n"
            
            dept_list = ""
            if dept_sample:
                dept_list = "\nDepartments:\n"
                for dept in dept_sample.fetchall():
                    dept_list += f"- {dept.department}\n"
            
            context = f"""
You are a friendly, intelligent AI library assistant similar to Google or ChatGPT.

Current Library Database:
- Total Books: {books_num}
- Active Members: {members_num}
{books_list}
{dept_list}

Your Capabilities:
- Help users find books by title, author, subject, or category
- Help users find members by name, department, or member type
- Answer questions about library operations (issue/return books, sales, etc.)
- Provide general guidance about using the library system
- Answer in Hindi or English naturally based on user's language
- Be conversational, friendly, and helpful like ChatGPT
- If you don't have specific database information, provide general helpful guidance

Guidelines:
- Be conversational and natural in your responses
- If you can't find specific information in the database, suggest alternatives
- Keep responses helpful but concise
- Use the user's language (Hindi or English)
- Be proactive in suggesting related information
"""
            return context
        except:
            return "You are a helpful AI library assistant similar to ChatGPT."
    
    def get_response(self, user_input):
        """Get AI response using Groq Llama3"""
        if not self.client:
            if not self.initialize():
                return "**Error:** Please set your Groq API key in the sidebar to use AI features."
        
        query_lower = user_input.lower()
        
        # Only use direct database queries for very specific, structured requests
        # For everything else, use the AI model
        
        # MCA faculty - specific structured query
        if 'mca faculty' in query_lower or ('mca' in query_lower and 'faculty' in query_lower):
            mca_result = self.get_mca_faculty()
            if mca_result:
                return f"{mca_result}\n\nFor other operations, use the forms in the sidebar."
            else:
                return "No MCA faculty found in the database. You can add faculty members using the Members page."
        
        # For all other queries, use AI model with database context
        try:
            context = self.get_database_context()
            
            # Get some real data to provide to AI
            books_info = ""
            try:
                books_result = db_connection.execute_query("SELECT title, author, available_copies FROM books LIMIT 10")
                if books_result:
                    books = books_result.fetchall()
                    if books:
                        books_info = "\nRecent Books:\n"
                        for book in books:
                            books_info += f"- {book.title} by {book.author} ({book.available_copies} available)\n"
            except:
                pass
            
            members_info = ""
            try:
                members_result = db_connection.execute_query("SELECT name, department, member_type FROM library_members WHERE status = 'Active' LIMIT 10")
                if members_result:
                    members = members_result.fetchall()
                    if members:
                        members_info = "\nActive Members:\n"
                        for member in members:
                            members_info += f"- {member.name} ({member.department}, {member.member_type})\n"
            except:
                pass
            
            messages = [
                {
                    "role": "system",
                    "content": context + f"""
{books_info}
{members_info}

You are an intelligent AI assistant. When users ask about books or members:
- If they ask for specific information you have in the context, provide it
- If they ask general questions, answer helpfully using your knowledge
- Be conversational and natural like ChatGPT
- If you need to search the database for specific information, suggest they use the appropriate page
- Always be helpful and friendly
- Answer in the same language as the user (Hindi or English)
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}\n\nPlease check your Groq API key and try again."

def ai_assistant_page():
    """Main AI assistant page with Groq"""
    st.header("🤖 AI Library Assistant (Powered by Llama3)")
    
    # API Key input in sidebar
    with st.sidebar:
        st.subheader("🔑 Groq API Key")
        api_key = st.text_input("Enter your Groq API Key:", type="password", key="groq_api_key_input")
        if api_key:
            st.session_state["groq_api_key"] = api_key
            st.success("API Key saved!")
        
        st.markdown("""
**Get Free API Key:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create API Key
4. Paste it above
        
**Free Usage:**
- Llama3 8B model
- Fast inference
- No cost
        """)
    
    st.info("💡 Ask me anything about the library in Hindi or English!")
    
    # Initialize AI
    ai = GroqAI()
    
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
                    response = ai.get_response(user_input)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
