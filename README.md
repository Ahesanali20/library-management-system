# Library Management System with AI Assistant

A comprehensive library management system with AI-powered conversational interface, built for LJ University. Features intelligent search, natural language processing, and automated assistance using Groq's Llama3 model.

## Overview

The Library Management System combines traditional library operations with modern AI capabilities, providing users with a conversational interface to search books, manage members, track transactions, and get intelligent assistance.

## Key Features

### AI-Powered Capabilities
- **Natural Language Interface**: Chat with the AI assistant in Hindi or English
- **Intelligent Search**: Google-like conversational search with contextual understanding
- **AI Integration**: Powered by Groq's Llama3 model (free, fast inference)
- **Database-Aware**: AI has context of library database for intelligent responses

### Library Management
- **Book Management**: Complete CRUD operations for book inventory with pricing
- **Member Management**: User registration and department-based organization
- **Transaction Tracking**: Issue/return operations with automated tracking
- **Sales Integration**: Book purchasing functionality with payment tracking
- **Multi-Database Support**: Switch between different library databases

### Technical Features
- **Real-time Database Operations**: MySQL backend with optimized queries
- **Responsive Web Interface**: Streamlit-based user interface
- **Session Management**: Persistent chat history and user sessions
- **Error Handling**: Robust error management and user feedback

## Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: SQLAlchemy with MySQL database
- **AI/ML**: Groq API with Llama3 model (free, fast)
- **Database**: MySQL with relational schema design

### System Components
1. **Database Layer**: MySQL database with books, members, transactions, and sales
2. **AI Agent Layer**: Groq Llama3 integration with database context
3. **Application Layer**: Streamlit web application with modular structure
4. **Integration Layer**: Dynamic database connection and management

## Installation & Setup

### Prerequisites
```bash
pip install streamlit sqlalchemy pymysql groq
```

### AI Setup (Required for AI features)
To enable AI-powered responses, get a free Groq API key:
1. Visit: https://console.groq.com
2. Sign up (free) and create API key
3. Set as environment variable:
```bash
set GROQ_API_KEY=your_api_key_here
```
Or enter it in the sidebar when running the application.

### Database Setup
```bash
# Run the database setup script
mysql -u root -p < setup_databases.sql
```

### Running the Application
```bash
# Run the main application
streamlit run main_app.py

# Or using Python module
python -m streamlit run main_app.py
```

## Project Structure

```
library/
|-- README.md                    # Project documentation
|-- main_app.py                  # Main Streamlit application
|-- ai_assistant_groq.py         # AI Assistant with Groq integration
|-- book_management.py           # Book operations module
|-- member_management.py         # Member operations module
|-- sales_management.py          # Book sales module
|-- transaction_management.py    # Book issue/return module
|-- db_connection.py             # Database connection handler
|-- database_config.py           # Database configuration page
|-- setup_databases.sql          # SQL schema and sample data
|-- .gitignore                   # Git ignore rules
```

## Database Schema

### Books Table
- **id**: Primary key
- **isbn**: Unique ISBN identifier
- **title**: Book title
- **author**: Book author
- **publisher**: Publishing company
- **publication_year**: Year of publication
- **genre**: Book genre
- **category**: Book category
- **total_copies**: Total number of copies
- **available_copies**: Available copies for issue
- **for_sale**: Whether book is available for purchase
- **sale_price**: Price for purchasing the book
- **location**: Physical location in library
- **description**: Book description
- **added_date**: Date added to system
- **last_updated**: Last update timestamp

### Members Table
- **id**: Primary key
- **name**: Member name
- **email**: Email address
- **phone**: Phone number
- **membership_type**: Type of membership
- **join_date**: Date of joining
- **status**: Active/inactive status

### Transactions Table
- **id**: Primary key
- **book_id**: Foreign key to books table
- **member_id**: Foreign key to members table
- **issue_date**: Date of issue
- **due_date**: Due date for return
- **return_date**: Actual return date
- **status**: Transaction status

## AI Capabilities

### Natural Language Processing
The system can understand and process queries such as:
- "Find books by machine learning authors"
- "What books are available for issue?"
- "Show me all overdue books"
- "Who has the most books issued?"

### Intelligent Search
- Context-aware search based on query content
- Automatic detection of member names and book titles
- Smart filtering based on availability and categories

### Automated Assistance
- Automatic query generation for complex requests
- Error handling and user-friendly error messages
- Contextual suggestions and recommendations

## Usage Examples

### Basic Operations
1. **Book Search**: Use natural language to find books
2. **Issue Books**: Request book issuance with member details
3. **Return Books**: Process book returns and update availability
4. **Member Management**: Add/update member information

### Advanced Features
1. **Sales Integration**: Purchase books directly through the system
2. **Inventory Management**: Track book availability and locations
3. **Reporting**: Generate reports on library usage and trends

## Development Team

This project was developed by students of the Computer Applications Department at LJ University under the guidance of Prof. Alok Manke.

## Future Enhancements

- **Machine Learning Recommendations**: Personalized book recommendations
- **Mobile Application**: Native mobile app for library access
- **Advanced Analytics**: Detailed usage analytics and insights
- **Integration Systems**: Integration with university ERP systems
- **Multi-language Support**: Support for multiple languages

## License

This project is developed for educational purposes as part of the academic curriculum at LJ University.

---

**Note**: This project represents a successful integration of artificial intelligence with traditional library management systems, demonstrating the practical application of AI concepts in real-world scenarios.
