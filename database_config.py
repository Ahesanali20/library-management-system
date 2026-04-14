"""
Database Configuration Manager
Supports multiple MySQL databases with dynamic connection switching
"""

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class DatabaseConfig:
    """Manages multiple database connections"""
    
    @staticmethod
    def get_connection_string(db_host, db_user, db_password, db_name, db_port="3306"):
        """Create MySQL connection string"""
        if db_password:
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            return f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
    
    @staticmethod
    def test_connection(db_host, db_user, db_password, db_name, db_port="3306"):
        """Test database connection with user-friendly error messages"""
        try:
            connection_string = DatabaseConfig.get_connection_string(
                db_host, db_user, db_password, db_name, db_port
            )
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True, "✅ Connection successful!"
        except Exception as e:
            error_str = str(e)
            # User-friendly error messages
            if "Unknown database" in error_str:
                return False, f"❌ Database '{db_name}' not found. Please check the database name."
            elif "Access denied" in error_str:
                return False, "❌ Access denied. Please check your username and password."
            elif "Can't connect" in error_str or "Connection refused" in error_str:
                return False, f"❌ Cannot connect to MySQL server at {db_host}:{db_port}. Please check if MySQL is running."
            elif "Unknown server host" in error_str:
                return False, f"❌ Unknown host '{db_host}'. Please check the server address."
            else:
                return False, f"❌ Connection failed. Please check your credentials and try again."
    
    @staticmethod
    def get_all_databases(db_host, db_user, db_password, db_port="3306"):
        """Fetch all databases from MySQL server"""
        try:
            # Connect without specifying a database
            if db_password:
                connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}"
            else:
                connection_string = f"mysql+pymysql://{db_user}@{db_host}:{db_port}"
            
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                # Query to get all databases (exclude system databases)
                result = conn.execute(text("SHOW DATABASES"))
                databases = [row[0] for row in result.fetchall()]
                # Filter out system databases
                system_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys']
                databases = [db for db in databases if db not in system_dbs]
                return databases
        except Exception as e:
            st.error(f"Error fetching databases: {e}")
            return []
    
    @staticmethod
    def get_engine(db_host, db_user, db_password, db_name, db_port="3306"):
        """Get SQLAlchemy engine for database"""
        try:
            connection_string = DatabaseConfig.get_connection_string(
                db_host, db_user, db_password, db_name, db_port
            )
            @st.cache_resource
            def _get_engine():
                return create_engine(connection_string, pool_pre_ping=True)
            return _get_engine()
        except SQLAlchemyError as e:
            st.error(f"Database Engine Error: {e}")
            return None
    
    @staticmethod
    def save_database_config(config_name, db_config):
        """Save database configuration to session state"""
        if 'saved_databases' not in st.session_state:
            st.session_state.saved_databases = {}
        st.session_state.saved_databases[config_name] = db_config
    
    @staticmethod
    def get_saved_configs():
        """Get all saved database configurations"""
        return st.session_state.get('saved_databases', {})
    
    @staticmethod
    def delete_saved_config(config_name):
        """Delete saved database configuration"""
        if 'saved_databases' in st.session_state:
            if config_name in st.session_state.saved_databases:
                del st.session_state.saved_databases[config_name]

def database_login_page():
    """Multi-database login and selection page"""
    st.set_page_config(page_title="Library Management - Database Login", layout="wide")
    
    st.title("📚 Library Management System")
    st.markdown("### Database Connection Setup")
    
    # Initialize session state
    if 'current_database' not in st.session_state:
        st.session_state.current_database = None
    if 'db_config' not in st.session_state:
        st.session_state.db_config = None
    
    # Tabs for different options
    tab1, tab2, tab3 = st.tabs(["🔌 Connect to Database", "💾 Saved Databases", "📋 About"])
    
    # Tab 1: Connect to new database
    with tab1:
        st.subheader("Connect to MySQL Database")
        
        # Quick database selection
        st.markdown("### 📚 Quick Database Selection")
        
        databases = {
            "🏛️ History Library": {
                "db_name": "history_library_db",
                "description": "Ancient, Medieval & Modern History Books",
                "emoji": "🏛️"
            },
            "💻 Programming Library": {
                "db_name": "programming_library_db",
                "description": "PHP, Python, Java, Web Dev Books",
                "emoji": "💻"
            },
            "📖 Novel Library": {
                "db_name": "novel_library_db",
                "description": "Romantic, Thriller & Fiction Novels",
                "emoji": "📖"
            }
        }
        
        cols = st.columns(3)
        selected_db = None
        
        for idx, (label, db_info) in enumerate(databases.items()):
            with cols[idx]:
                if st.button(
                    f"{db_info['emoji']}\n{label}\n\n{db_info['description']}",
                    use_container_width=True,
                    key=f"quick_db_{db_info['db_name']}"
                ):
                    selected_db = db_info['db_name']
                    st.session_state.selected_quick_db = db_info['db_name']
        
        st.divider()
        st.markdown("### 🔧 Manual Connection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            db_host = st.text_input(
                "Database Host",
                value="localhost",
                help="MySQL server address (e.g., localhost, 127.0.0.1, or IP)"
            )
            db_user = st.text_input(
                "Username",
                value="root",
                help="MySQL username"
            )
        
        with col2:
            db_port = st.text_input(
                "Port",
                value="3306",
                help="MySQL port (default: 3306)"
            )
            db_password = st.text_input(
                "Password",
                type="password",
                help="MySQL password (leave empty if no password)"
            )
        
        db_name = st.text_input(
            "Database Name",
            value=st.session_state.get('selected_quick_db', ''),
            help="MySQL database name (e.g., history_library_db, programming_library_db, novel_library_db)"
        )
        
        # Test connection button
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Test Connection", use_container_width=True):
                if not db_name:
                    st.error("❌ Please enter database name")
                else:
                    with st.spinner("Testing connection..."):
                        success, message = DatabaseConfig.test_connection(
                            db_host, db_user, db_password, db_name, db_port
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        
        with col2:
            if st.button("✅ Connect", use_container_width=True):
                if not db_name:
                    st.error("❌ Please enter database name")
                else:
                    with st.spinner("Connecting..."):
                        success, message = DatabaseConfig.test_connection(
                            db_host, db_user, db_password, db_name, db_port
                        )
                        if success:
                            st.session_state.current_database = {
                                'host': db_host,
                                'user': db_user,
                                'password': db_password,
                                'name': db_name,
                                'port': db_port
                            }
                            st.session_state.db_config = st.session_state.current_database
                            st.success(f"✅ Connected to '{db_name}'!")
                            st.balloons()
                        else:
                            st.error(message)
        
        with col3:
            if st.button("🏠 Home", use_container_width=True):
                if st.session_state.db_config:
                    st.switch_page("pages/home.py")
    
    # Tab 2: Saved databases
    with tab2:
        st.subheader("📋 Your Saved Databases")
        
        # Quick reference to available databases
        st.info("""
        📚 **Available System Databases:**
        - 🏛️ **history_library_db** - Ancient, Medieval & Modern History
        - 💻 **programming_library_db** - PHP, Python, Java, Web Dev
        - 📖 **novel_library_db** - Romantic, Thriller & Fiction Novels
        
        Use the '🔌 Connect to Database' tab to connect to any of these!
        """)
        
        st.divider()
        
        saved_configs = DatabaseConfig.get_saved_configs()
        
        if saved_configs:
            for config_name, config in saved_configs.items():
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{config_name}**")
                        st.caption(f"Host: {config['host']} | DB: {config['name']}")
                    
                    with col2:
                        if st.button("🔌 Connect", key=f"connect_{config_name}", use_container_width=True):
                            st.session_state.current_database = config
                            st.session_state.db_config = config
                            st.success(f"Connected to {config_name}!")
                            st.switch_page("pages/home.py")
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{config_name}", use_container_width=True):
                            DatabaseConfig.delete_saved_config(config_name)
                            st.rerun()
        else:
            st.info("📌 No saved databases yet. Create one using the 'Connect to Database' tab!")
    
    # Tab 3: About
    with tab3:
        st.subheader("ℹ️ About Multi-Database Support")
        
        st.markdown("""
        ### Features:
        
        ✅ **Connect to Any MySQL Database**
        - Enter host, username, password, database name
        - Test connection before connecting
        
        ✅ **Save Multiple Connections**
        - Save frequently used databases
        - Quick access without re-entering credentials
        
        ✅ **Switch Databases Anytime**
        - Navigate to Home and select different database
        - Your data stays separated
        
        ✅ **Secure**
        - Passwords not stored on disk
        - Session-based connections
        
        ### Available Databases:
        
        🏛️ **history_library_db**
        - Stores Ancient, Medieval & Modern History Books
        - Perfect for history enthusiasts
        
        💻 **programming_library_db**
        - Stores PHP, Python, Java, Web Dev Books
        - For developers and programmers
        
        📖 **novel_library_db**
        - Stores Romantic, Thriller & Fiction Novels
        - For novel readers and fiction lovers
        
        ### Common Issues:
        
        **Connection Refused?**
        - Ensure MySQL is running
        - Check host and port are correct
        - Verify username and password
        
        **Database Not Found?**
        - Ensure database name is correct
        - Check that the database exists in MySQL
        - Available databases: history_library_db, programming_library_db, novel_library_db
        
        **Permission Denied?**
        - Verify user has access to the database
        - Check MySQL user permissions
        """)

def get_database_connection():
    """Get current database configuration"""
    return st.session_state.get('db_config')

def is_database_connected():
    """Check if database is connected"""
    return st.session_state.get('db_config') is not None
