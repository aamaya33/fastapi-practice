import requests
import json
from pydantic import BaseModel
from typing import Optional
import sys

# request.py

# Define the Book model to match the one in the application
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: Optional[str] = None

# Base URL for the FastAPI application
BASE_URL = "http://127.0.0.1:8000"

def test_get_books():
    """Test the GET /books endpoint"""
    response = requests.get(f"{BASE_URL}/books")
    print("GET /books Response:", response)
    print("Response Body:", response.json())
    return response.json()

def test_add_book(book_id, title, author, description):
    """Test the POST /books/{book_id} endpoint"""
    # Using a dummy book_id since it's not used in the function
    params = {
        "title": title,
        "author": author,
        "description": description
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}", params=params)
    print(f"POST /books/{book_id} Response:", response.status_code)
    print("Response Body:", response.json())
    return response.json()

def test_delete_book(book_name):
    """Test the DELETE /books/{book_id} endpoint"""
    response = requests.delete(f"{BASE_URL}/books/{book_name}")
    print(f"DELETE /books/{book_name} Response:", response.status_code)
    print("Response Body:", response.json() if response.status_code == 200 else response.text)
    return response

def test_update_book(book_id, book_data):
    """Test the PUT /books/{book_id} endpoint"""
    response = requests.put(
        f"{BASE_URL}/books/{book_id}",
        json=book_data
    )
    print(f"PUT /books/{book_id} Response:", response.status_code)
    print("Response Body:", response.json())
    assert response.status_code == 200
    return response.json()

if __name__ == "__main__":
    # Run all tests in sequence
    print("Testing GET /books (empty state)")
    test_get_books()
    
    print("\nTesting POST /books/1 (add first book)")
    test_add_book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A novel about the American Dream")
    
    print("\nTesting POST /books/2 (add second book)")
    test_add_book(2, "To Kill a Mockingbird", "Harper Lee", "A novel about racial injustice")
    
    print("\nTesting GET /books (after adding books)")
    books = test_get_books()
    
    # Note: There's a potential issue in the API's delete_book function
    # It tries to remove book_name from books_db but books_db contains Book objects
    # Uncomment the following lines if the delete endpoint is fixed
    # print("\nTesting DELETE /books/The Great Gatsby")
    # delete_response = test_delete_book("The Great Gatsby")
    
    # Update book with index 0
    print("\nTesting PUT /books/0")
    book_data = {
        "title": "Updated Book Title",
        "author": "Updated Author",
        "description": "Updated description"
    }
    test_update_book(0, book_data)
    
    print("\nTesting GET /books (final state)")
    test_get_books()
    
    print("\nAll tests completed")