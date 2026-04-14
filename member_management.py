"""
Member Management Module for Library System
Handles all member-related operations: add, search, display
"""

import streamlit as st
from db_connection import db_connection

class MemberManager:
    """Member management operations"""
    
    @staticmethod
    def search_members(search_term=""):
        """Search members with filters"""
        query = """
            SELECT * FROM library_members 
            WHERE status = 'Active'
        """
        params = {}
        
        if search_term:
            query += " AND (name LIKE :search OR member_id LIKE :search OR email LIKE :search)"
            params["search"] = f"%{search_term}%"
        
        query += " ORDER BY name"
        
        return db_connection.execute_query(query, params)
    
    @staticmethod
    def get_member_by_id(member_id):
        """Get member details by ID"""
        query = "SELECT * FROM library_members WHERE member_id = :member_id"
        result = db_connection.execute_query(query, {"member_id": member_id})
        return result.fetchone() if result else None
    
    @staticmethod
    def add_member(member_id, name, email="", phone="", member_type="Student", 
                  department=""):
        """Add new member to database"""
        # Validation
        if not member_id or not name:
            st.error("Member ID and Full Name are required fields!")
            return False
        
        query = """
            INSERT INTO library_members 
            (member_id, name, email, phone, member_type, department, status)
            VALUES (:member_id, :name, :email, :phone, :type, :dept, 'Active')
        """
        
        params = {
            "member_id": member_id, "name": name, "email": email, "phone": phone,
            "type": member_type, "dept": department
        }
        
        return db_connection.commit_changes(query, params)
    
    @staticmethod
    def get_active_members():
        """Get active members list for dropdowns"""
        query = """
            SELECT member_id, name, email FROM library_members 
            WHERE status = 'Active' 
            ORDER BY name
        """
        return db_connection.execute_query(query)
    
    @staticmethod
    def get_member_history(member_id):
        """Get member's transaction history"""
        query = """
            SELECT bt.transaction_id, b.title, b.author, bt.issue_date, 
                   bt.return_date, bt.status
            FROM book_transactions bt
            JOIN books b ON bt.book_id = b.book_id
            WHERE bt.member_id = :member_id
            ORDER BY bt.issue_date DESC
        """
        return db_connection.execute_query(query, {"member_id": member_id})

def display_members():
    """Display active members"""
    members = MemberManager.search_members()
    
    if members:
        for member in members:
            with st.expander(f"{member.name} - {member.member_type}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Member ID**: {member.member_id}")
                    st.write(f"**Email**: {member.email}")
                    st.write(f"**Phone**: {member.phone}")
                with col2:
                    st.write(f"**Type**: {member.member_type}")
                    st.write(f"**Department**: {member.department}")
                    st.write(f"**Status**: {member.status}")
                st.write(f"**Join Date**: {member.join_date}")
    else:
        st.info("No active members found.")

def add_member_form():
    """Form to add new member"""
    st.subheader("Add New Member - Naya Member Jodein")
    
    with st.form("add_member_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            member_id = st.text_input("Member ID*:")
            name = st.text_input("Full Name*:")
            email = st.text_input("Email:")
            phone = st.text_input("Phone:")
        
        with col2:
            member_type = st.selectbox("Member Type*:", ["Student", "Faculty", "Staff"])
            department = st.text_input("Department:")
        
        if st.form_submit_button("Add Member"):
            success = MemberManager.add_member(
                member_id, name, email, phone, member_type,
                department
            )
            
            if success:
                st.success(f"Member '{name}' added successfully!")
                st.rerun()

def member_history_page():
    """Display member transaction history"""
    members_result = MemberManager.get_active_members()
    members = members_result.fetchall() if members_result else []
    
    if members:
        member_options = [f"{member.member_id} - {member.name}" for member in members]
        selected_member = st.selectbox("Select Member:", member_options)
        
        if selected_member:
            member_id = int(selected_member.split(" - ")[0])
            
            # Get member details
            member = MemberManager.get_member_by_id(member_id)
            
            st.subheader(f"History for {member.name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Member ID**: {member.member_id}")
                st.write(f"**Email**: {member.email}")
                st.write(f"**Phone**: {member.phone}")
                st.write(f"**Type**: {member.member_type}")
            
            with col2:
                st.write(f"**Department**: {member.department}")
                st.write(f"**Status**: {member.status}")
                st.write(f"**Join Date**: {member.join_date}")
            
            # Get transaction history
            trans_result = MemberManager.get_member_history(member_id)
            transactions = trans_result.fetchall() if trans_result else []
            
            if transactions:
                st.subheader("📚 Transaction History")
                for trans in transactions:
                    with st.expander(f"{trans.status}: {trans.title} ({trans.issue_date})"):
                        st.write(f"**Book**: {trans.title} by {trans.author}")
                        st.write(f"**Issue Date**: {trans.issue_date}")
                        st.write(f"**Return Date**: {trans.return_date if trans.return_date else 'Not Returned'}")
                        st.write(f"**Status**: {trans.status}")
            else:
                st.info("No transactions found for this member.")
    else:
        st.info("No active members found.")

def member_management_page():
    """Main member management page"""
    st.header("Member Management - Member Management")
    
    # Display members
    display_members()
    
    # Add new member form
    add_member_form()
