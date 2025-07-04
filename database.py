import sqlite3

def init_db():
    with sqlite3.connect("library.db") as connection:
        cur = connection.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        
        connection.commit()
        print("Database created and table initialized.")

def add_book(title, author):

    with sqlite3.connect("library.db") as connection:
        cur = connection.cursor()

        cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", 
                    (title, author))

        new_book_id = cur.lastrowid
        cur.execute("SELECT * FROM books WHERE id = ?", (new_book_id,))
        new_book = cur.fetchone()
        connection.commit()
        print("Book added successfully!")
        return {"id": new_book[0],  "title": new_book[1],  
                "author": new_book[2]}

def view_book():
    with sqlite3.connect('library.db') as connection:
        cur = connection.cursor()
        
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()

        if not books:
            return "No Books found in the database."
        return books

def update_book(book_id, new_title, new_author):
    with sqlite3.connect("library.db") as connection:
        cur = connection.cursor()
        cur.execute("UPDATE books SET title = ?, author = ? WHERE id = ?",
        (new_title, new_author, book_id))
        connection.commit()
        print("Book updated successfully!")
        
def delete_book(book_id):
    with sqlite3.connect("library.db") as connection:
        cur = connection.cursor()
        cur.execute("DELETE FROM books WHERE = ?", (book_id,))
        connection.commit()
        print("Book deleted successfully!")
        
init_db()