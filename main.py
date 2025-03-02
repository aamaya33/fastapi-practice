# adding get all books (GET /books)
# get a single book by ID (GET /books/{book_id})
# create a new book (POST /books)
# update a book by ID (PUT /books/{book_id})
# delete a book by ID (DELETE /books/{book_id})

from fastapi import FastAPI, HTTPException
from models import Book 

app = FastAPI() 

books_db = []

@app.get("/books")
def index():
    return books_db

@app.get("/books/{book_id}")
def search(book_id: int):
    for index, book in enumerate(books_db):
        if book_id == index: 
            return book
    raise HTTPException(404, "Book not found")

@app.post("/books")
def add_book(book: Book):
    book.id = len(books_db) + 1 
    books_db.append(book)
    return {"message": "Book added successfully"}

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            updated_book.id = book_id
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if index == book_id:
            books_db.pop(index)
    return HTTPException(404, "Book not found")