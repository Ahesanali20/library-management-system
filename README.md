# Library AI Agent

An intelligent, data science-driven library management system that leverages artificial intelligence and machine learning to enhance library operations and user experience at LJ University.

## Overview

The Library AI Agent is a sophisticated system that combines traditional library management with modern AI capabilities, providing intelligent search, natural language processing, and automated assistance for library operations.

## Key Features

### AI-Powered Capabilities
- **Natural Language Interface**: Users can interact with the system using conversational language
- **Intelligent Search**: Google-like search functionality with contextual understanding
- **AI Agent Integration**: Powered by Google Gemini for intelligent query processing
- **SQL Agent**: Automated database query generation and execution

### Library Management
- **Book Management**: Complete CRUD operations for book inventory
- **Member Management**: User registration and management system
- **Transaction Tracking**: Issue/return operations with automated tracking
- **Sales Integration**: Book purchasing functionality with pricing management

### Technical Features
- **Real-time Database Operations**: SQLite backend with optimized queries
- **Responsive Web Interface**: Streamlit-based user interface
- **Session Management**: Persistent chat history and user sessions
- **Error Handling**: Robust error management and user feedback

## Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: SQLAlchemy with SQLite database
- **AI/ML**: Google Gemini API with intelligent context-aware responses
- **Database**: SQLite with relational schema design

### System Components
1. **Database Layer**: Structured SQLite database with books, members, and transactions
2. **AI Agent Layer**: Google Gemini integration with database context processing
3. **Application Layer**: Streamlit web application with user interface
4. **Integration Layer**: Seamless connection between AI capabilities and database operations

## Installation & Setup

### Prerequisites
```bash
pip install streamlit sqlalchemy pymysql google-generativeai
```

### AI Setup (Optional)
To enable AI-powered responses, get a free Gemini API key:
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key and set as environment variable:
```bash
set GEMINI_API_KEY=your_api_key_here
```
Note: If no API key is provided, the system works in rule-based mode.

### Database Setup
```bash
# Run the database setup script
python setup_library_db.py
# For enhanced features
python enhanced_library_setup.py
```

### Running the Application
```bash
# Run the modular version
streamlit run main_app.py

# Or using Python module
python -m streamlit run main_app.py
```

## Project Structure

```
library/
|-- README.md                    # Project documentation
|-- requirements.txt             # Python dependencies
|-- main_app.py                  # Main Streamlit application
|-- ai_assistant.py              # AI Assistant with Gemini integration
|-- book_management.py           # Book operations module
|-- member_management.py         # Member operations module
|-- sales_management.py          # Book sales module
|-- transaction_management.py    # Book issue/return module
|-- db_connection.py             # Database connection handler
|-- mysql_library_setup.sql      # SQL schema definition
|-- .gitignore                   # Git ignore rules
|-- .streamlit/                  # Streamlit configuration
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
