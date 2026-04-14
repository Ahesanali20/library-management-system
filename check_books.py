"""
Check current books in database
"""

from db_connection import db_connection

def check_books():
    """Check books in current database"""
    try:
        query = "SELECT book_id, title, author, for_sale, sale_price FROM books LIMIT 10"
        result = db_connection.execute_query(query)
        
        if result:
            books = result.fetchall()
            print(f"Total books found: {len(books)}\n")
            
            for book in books:
                print(f"ID: {book.book_id}")
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"For Sale: {book.for_sale}")
                print(f"Price: ${book.sale_price}")
                print("-" * 40)
        else:
            print("No books found or database connection issue")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_books()
