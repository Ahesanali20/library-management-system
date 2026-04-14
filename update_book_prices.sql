-- Update book prices in existing databases
-- Run this script to add prices to existing books

-- History Library Database
USE history_library_db;
UPDATE books SET for_sale = 1, sale_price = 25.99 WHERE title = 'The Fall of Rome';
UPDATE books SET for_sale = 1, sale_price = 15.99 WHERE title = 'Ancient Egypt: A Very Short Introduction';
UPDATE books SET for_sale = 1, sale_price = 29.99 WHERE title = 'The Medieval Crusades';
UPDATE books SET for_sale = 1, sale_price = 35.99 WHERE title = 'A History of Medieval Europe';
UPDATE books SET for_sale = 1, sale_price = 45.99 WHERE title = 'Modern History: From 1500 to Present';
UPDATE books SET for_sale = 1, sale_price = 39.99 WHERE title = 'The 20th Century in Pictures';

-- Programming Library Database
USE programming_library_db;
UPDATE books SET for_sale = 1, sale_price = 49.99 WHERE title = 'PHP 8 in Action';
UPDATE books SET for_sale = 1, sale_price = 39.99 WHERE title = 'Modern PHP';
UPDATE books SET for_sale = 1, sale_price = 44.99 WHERE title = 'Python Crash Course';
UPDATE books SET for_sale = 1, sale_price = 59.99 WHERE title = 'Fluent Python';
UPDATE books SET for_sale = 1, sale_price = 54.99 WHERE title = 'Head First Java';
UPDATE books SET for_sale = 1, sale_price = 64.99 WHERE title = 'Effective Java';
UPDATE books SET for_sale = 1, sale_price = 42.99 WHERE title = 'Web Development with Node.js';
UPDATE books SET for_sale = 1, sale_price = 47.99 WHERE title = 'The Pragmatic Programmer';

-- Novel Library Database
USE novel_library_db;
UPDATE books SET for_sale = 1, sale_price = 12.99 WHERE title = 'Pride and Prejudice';
UPDATE books SET for_sale = 1, sale_price = 14.99 WHERE title = 'The Notebook';
UPDATE books SET for_sale = 1, sale_price = 18.99 WHERE title = 'Outlander';
UPDATE books SET for_sale = 1, sale_price = 13.99 WHERE title = 'A Walk to Remember';
UPDATE books SET for_sale = 1, sale_price = 16.99 WHERE title = 'The Girl with the Dragon Tattoo';
UPDATE books SET for_sale = 1, sale_price = 15.99 WHERE title = 'Gone Girl';
UPDATE books SET for_sale = 1, sale_price = 14.99 WHERE title = 'The Silence of the Lambs';
UPDATE books SET for_sale = 1, sale_price = 11.99 WHERE title = 'The Great Gatsby';
UPDATE books SET for_sale = 1, sale_price = 13.99 WHERE title = 'To Kill a Mockingbird';
UPDATE books SET for_sale = 1, sale_price = 12.99 WHERE title = '1984';
