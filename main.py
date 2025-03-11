# adding get all books (GET /books)
# get a single book by ID (GET /books/{book_id})
# create a new book (POST /books)
# update a book by ID (PUT /books/{book_id})
# delete a book by ID (DELETE /books/{book_id})

from fastapi import FastAPI, HTTPException
from models import Book 
import sqlite3

app = FastAPI() 

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row # Why do we need this? 
    return conn

conn = get_db_connection()
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT NOT NULL      
            ) """)
conn.commit()
conn.close()

@app.get("/books")
def index():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    con.close()
    return books
    

@app.get("/books/{book_id}")
def search(book_id: int):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cur.fetchone()
    con.close()
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
def add_book(book: Book):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO books (title, author, description) VALUES (?, ?, ?)", (book.title, book.author, book.description))
    con.commit()
    con.close()
    return {"message": "Book added successfully"}

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('UPDATE books SET title = ?, author = ?, description = ? WHERE id = ?', (updated_book.title, updated_book.author, updated_book.description, book_id))
    con.commit() 
    # this is lowkey gonna be some funky logic, but i need to add some error handling 
    cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cur.fetchone()
    con.close()
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")
    

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('DELETE FROM books WHERE id = ?', (book_id,))
    con.commit()
    con.close()
    if cur.rowcount:
        return {"message": "Book deleted successfully"}
    return HTTPException(404, "Book not found")