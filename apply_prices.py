"""
Apply book prices to current database
Run this script to update existing books with prices
"""

from db_connection import db_connection

# Define price updates for each database
price_updates = {
    'history_library_db': [
        ('The Fall of Rome', 25.99),
        ('Ancient Egypt: A Very Short Introduction', 15.99),
        ('The Medieval Crusades', 29.99),
        ('A History of Medieval Europe', 35.99),
        ('Modern History: From 1500 to Present', 45.99),
        ('The 20th Century in Pictures', 39.99),
    ],
    'programming_library_db': [
        ('PHP 8 in Action', 49.99),
        ('Modern PHP', 39.99),
        ('Python Crash Course', 44.99),
        ('Fluent Python', 59.99),
        ('Head First Java', 54.99),
        ('Effective Java', 64.99),
        ('Web Development with Node.js', 42.99),
        ('The Pragmatic Programmer', 47.99),
    ],
    'novel_library_db': [
        ('Pride and Prejudice', 12.99),
        ('The Notebook', 14.99),
        ('Outlander', 18.99),
        ('A Walk to Remember', 13.99),
        ('The Girl with the Dragon Tattoo', 16.99),
        ('Gone Girl', 15.99),
        ('The Silence of the Lambs', 14.99),
        ('The Great Gatsby', 11.99),
        ('To Kill a Mockingbird', 13.99),
        ('1984', 12.99),
    ]
}

def apply_prices():
    """Apply prices to books in current database"""
    try:
        # Get current database name from connection
        # We'll try to update based on book titles
        
        updated_count = 0
        
        for title, price in price_updates['history_library_db'] + price_updates['programming_library_db'] + price_updates['novel_library_db']:
            query = """
                UPDATE books 
                SET for_sale = 1, sale_price = :price 
                WHERE title = :title
            """
            params = {"price": price, "title": title}
            
            result = db_connection.commit_changes(query, params)
            if result:
                updated_count += 1
                print(f"[OK] Updated: {title} - ${price}")
        
        print(f"\n[SUCCESS] Total books updated: {updated_count}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error updating prices: {e}")
        return False

if __name__ == "__main__":
    print("Applying book prices to database...")
    apply_prices()
