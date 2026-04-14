"""
Database Connection Module for Library Management System
Supports dynamic MySQL connections with session-based configuration
"""

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class DatabaseConnection:
    """Database connection manager for library system"""
    
    @staticmethod
    def get_engine():
        """Get database engine from current session configuration"""
        try:
            db_config = st.session_state.get('db_config')
            
            if not db_config:
                st.error("No database connected. Please login first.")
                return None
            
            # Build connection string from session state
            db_user = db_config.get('user', 'root')
            db_password = db_config.get('password', '')
            db_host = db_config.get('host', 'localhost')
            db_port = db_config.get('port', '3306')
            db_name = db_config.get('name', 'library_management')
            
            if db_password:
                connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            else:
                connection_string = f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
            
            return create_engine(connection_string, pool_pre_ping=True)
            
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Execute database query with user-friendly error handling"""
        try:
            with self.get_engine().connect() as conn:
                if params:
                    return conn.execute(text(query), params)
                else:
                    return conn.execute(text(query))
        except SQLAlchemyError as e:
            error_str = str(e)
            # User-friendly error messages
            if "Unknown database" in error_str:
                st.error("❌ Database not found. Please check your database connection.")
            elif "Access denied" in error_str:
                st.error("❌ Access denied. Please check your database credentials.")
            elif "Unknown column" in error_str:
                st.error("❌ Database schema mismatch. Please check your database structure.")
            elif "Table" in error_str and "doesn't exist" in error_str:
                st.error("❌ Required table not found. Please initialize the database.")
            elif "Can't connect" in error_str or "Connection refused" in error_str:
                st.error("❌ Cannot connect to database. Please check if MySQL is running.")
            else:
                st.error("❌ Database error. Please try again.")
            return None
    
    def commit_changes(self, query, params=None):
        """Execute query and commit changes with user-friendly error handling"""
        try:
            engine = self.get_engine()
            if not engine:
                return False
            
            with engine.connect() as conn:
                if params:
                    conn.execute(text(query), params)
                else:
                    conn.execute(text(query))
                conn.commit()
                return True
        except SQLAlchemyError as e:
            error_str = str(e)
            # User-friendly error messages
            if "Unknown database" in error_str:
                st.error("❌ Database not found. Please check your database connection.")
            elif "Access denied" in error_str:
                st.error("❌ Access denied. Please check your database credentials.")
            elif "Unknown column" in error_str:
                st.error("❌ Database schema mismatch. Please check your database structure.")
            elif "Table" in error_str and "doesn't exist" in error_str:
                st.error("❌ Required table not found. Please initialize the database.")
            elif "Duplicate entry" in error_str:
                st.error("❌ Duplicate entry. This record already exists.")
            elif "Can't connect" in error_str or "Connection refused" in error_str:
                st.error("❌ Cannot connect to database. Please check if MySQL is running.")
            else:
                st.error("❌ Database error. Please try again.")
            return False

# Global database connection instance
db_connection = DatabaseConnection()
