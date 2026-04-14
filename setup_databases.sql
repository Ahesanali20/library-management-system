-- ============================================
-- 1. HISTORY LIBRARY DATABASE
-- ============================================
CREATE DATABASE IF NOT EXISTS history_library_db;
USE history_library_db;

-- Books table for history library
CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    year_published INT,
    isbn VARCHAR(20),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    for_sale BOOLEAN DEFAULT 0,
    sale_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Library members table
CREATE TABLE IF NOT EXISTS library_members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    member_type ENUM('Student', 'Faculty', 'Staff') DEFAULT 'Student',
    department VARCHAR(100),
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book transactions table
CREATE TABLE IF NOT EXISTS book_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NULL,
    status ENUM('Active', 'Returned', 'Lost') DEFAULT 'Active',
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sales table
CREATE TABLE IF NOT EXISTS book_sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    quantity INT DEFAULT 1,
    price DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sample data for history_library_db
INSERT INTO books (title, author, category, year_published, isbn, total_copies, available_copies, for_sale, sale_price) VALUES
('The Fall of Rome', 'Bryan Ward-Perkins', 'Ancient History', 2005, '978-0-19-926186-3', 5, 3, 1, 25.99),
('Ancient Egypt: A Very Short Introduction', 'Ian Shaw', 'Ancient History', 2004, '978-0-19-280419-9', 4, 2, 1, 15.99),
('The Medieval Crusades', 'Jonathan Phillips', 'Medieval History', 2005, '978-0-375-41389-2', 6, 4, 1, 29.99),
('A History of Medieval Europe', 'Peter Brown', 'Medieval History', 2003, '978-0-631-18959-8', 5, 3, 1, 35.99),
('Modern History: From 1500 to Present', 'Richard Overy', 'Modern History', 2010, '978-0-06-174730-1', 7, 5, 1, 45.99),
('The 20th Century in Pictures', 'Philip Parker', 'Modern History', 2008, '978-1-4053-3350-6', 8, 6, 1, 39.99);

INSERT INTO library_members (name, email, phone, member_type, department, status) VALUES
('Raj Kumar', 'raj@college.com', '9876543210', 'Student', 'History', 'Active'),
('Dr. Anjali Singh', 'anjali@college.com', '9876543211', 'Faculty', 'History', 'Active'),
('Priya Sharma', 'priya@college.com', '9876543212', 'Student', 'History', 'Active'),
('Prof. Vikram Patel', 'vikram@college.com', '9876543213', 'Faculty', 'History', 'Active');

-- ============================================
-- 2. PROGRAMMING LIBRARY DATABASE
-- ============================================
CREATE DATABASE IF NOT EXISTS programming_library_db;
USE programming_library_db;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    year_published INT,
    isbn VARCHAR(20),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    for_sale BOOLEAN DEFAULT 0,
    sale_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Library members table
CREATE TABLE IF NOT EXISTS library_members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    member_type ENUM('Student', 'Faculty', 'Staff') DEFAULT 'Student',
    department VARCHAR(100),
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book transactions table
CREATE TABLE IF NOT EXISTS book_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NULL,
    status ENUM('Active', 'Returned', 'Lost') DEFAULT 'Active',
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sales table
CREATE TABLE IF NOT EXISTS book_sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    quantity INT DEFAULT 1,
    price DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sample data for programming_library_db
INSERT INTO books (title, author, category, year_published, isbn, total_copies, available_copies, for_sale, sale_price) VALUES
('PHP 8 in Action', 'Mike Vanier', 'PHP', 2021, '978-1617296444', 5, 3, 1, 49.99),
('Modern PHP', 'Josh Lockhart', 'PHP', 2015, '978-1491905173', 4, 2, 1, 39.99),
('Python Crash Course', 'Eric Matthes', 'Python', 2019, '978-1492051274', 8, 6, 1, 44.99),
('Fluent Python', 'Luciano Ramalho', 'Python', 2015, '978-1491946008', 6, 4, 1, 59.99),
('Head First Java', 'Bert Bates', 'Java', 2005, '978-0596009205', 7, 5, 1, 54.99),
('Effective Java', 'Joshua Bloch', 'Java', 2018, '978-0134685991', 5, 3, 1, 64.99),
('Web Development with Node.js', 'Alex Young', 'Web Dev', 2018, '978-1491902288', 4, 2, 1, 42.99),
('The Pragmatic Programmer', 'Dave Thomas', 'Web Dev', 2019, '978-0135957059', 6, 4, 1, 47.99);

INSERT INTO library_members (name, email, phone, member_type, department, status) VALUES
('Amit Verma', 'amit@college.com', '9876543220', 'Student', 'CSE', 'Active'),
('Dr. Neha Gupta', 'neha@college.com', '9876543221', 'Faculty', 'CSE', 'Active'),
('Rohit Singh', 'rohit@college.com', '9876543222', 'Student', 'CSE', 'Active'),
('Prof. Arun Kumar', 'arun@college.com', '9876543223', 'Faculty', 'IT', 'Active'),
('Sneha Patel', 'sneha@college.com', '9876543224', 'Student', 'IT', 'Active');

-- ============================================
-- 3. NOVEL LIBRARY DATABASE
-- ============================================
CREATE DATABASE IF NOT EXISTS novel_library_db;
USE novel_library_db;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    year_published INT,
    isbn VARCHAR(20),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    for_sale BOOLEAN DEFAULT 0,
    sale_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Library members table
CREATE TABLE IF NOT EXISTS library_members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    member_type ENUM('Student', 'Faculty', 'Staff') DEFAULT 'Student',
    department VARCHAR(100),
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book transactions table
CREATE TABLE IF NOT EXISTS book_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NULL,
    status ENUM('Active', 'Returned', 'Lost') DEFAULT 'Active',
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sales table
CREATE TABLE IF NOT EXISTS book_sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    quantity INT DEFAULT 1,
    price DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES library_members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Sample data for novel_library_db
INSERT INTO books (title, author, category, year_published, isbn, total_copies, available_copies, for_sale, sale_price) VALUES
('Pride and Prejudice', 'Jane Austen', 'Romantic', 1813, '978-0143039990', 4, 2, 1, 12.99),
('The Notebook', 'Nicholas Sparks', 'Romantic', 1996, '978-0446676952', 5, 3, 1, 14.99),
('Outlander', 'Diana Gabaldon', 'Romantic', 1991, '978-0385333696', 3, 2, 1, 18.99),
('A Walk to Remember', 'Nicholas Sparks', 'Romantic', 1999, '978-0446577199', 4, 2, 1, 13.99),
('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Thriller', 2005, '978-0307269935', 6, 4, 1, 16.99),
('Gone Girl', 'Gillian Flynn', 'Thriller', 2012, '978-0553842662', 5, 3, 1, 15.99),
('The Silence of the Lambs', 'Thomas Harris', 'Thriller', 1991, '978-0312924578', 4, 2, 1, 14.99),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925, '978-0743273565', 7, 5, 1, 11.99),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, '978-0061120084', 6, 4, 1, 13.99),
('1984', 'George Orwell', 'Fiction', 1949, '978-0451524935', 5, 3, 1, 12.99);

INSERT INTO library_members (name, email, phone, member_type, department, status) VALUES
('Deepak Verma', 'deepak@college.com', '9876543230', 'Student', 'Arts', 'Active'),
('Dr. Priya Nair', 'priya.nair@college.com', '9876543231', 'Faculty', 'English', 'Active'),
('Ananya Singh', 'ananya@college.com', '9876543232', 'Student', 'Arts', 'Active'),
('Prof. Rajesh Kumar', 'rajesh@college.com', '9876543233', 'Faculty', 'Literature', 'Active'),
('Shreya Desai', 'shreya@college.com', '9876543234', 'Student', 'Commerce', 'Active'),
('Vivek Sharma', 'vivek@college.com', '9876543235', 'Student', 'Arts', 'Active');
