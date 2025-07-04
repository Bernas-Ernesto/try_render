from flask import Flask, jsonify, request
from database import init_db, view_book, add_book, update_book, delete_book

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():
    init_db()
    books = view_book()
    if not books:
        return jsonify({"message": "No books found in the database."}), 404
    dictionary_books = [
        {"id": book[0], "title": book[1], "author": book[2]} for book in books
    ]
    return jsonify(dictionary_books), 200

@app.route('/books/<title>/<author>', methods=['POST'])
def post_book_with_params(title, author):
    new_book = add_book(title, author)
    return jsonify({
        "message": "Book added successfully!",
        "data": new_book,
        "location": f"/books/{new_book['id']}"
    }), 201

@app.route('/books', methods=['POST'])
def post_book():
    contents = request.json
    new_book = add_book(contents["title"], contents["author"])
    return jsonify({
        "message": "Book added successfully!",
        "data": new_book,
        "location": f"/books/{new_book['id']}"
    }), 201

@app.route('/books/<int:book_id>/<new_title>/<new_author>', methods=['PUT'])
def put_book_with_params(book_id, new_title, new_author):
    update_book(book_id, new_title, new_author)
    updated_book = {'id': book_id, 'title': new_title, 'author': new_author}
    return jsonify({"message": "Book updated successfully!", "data": updated_book}), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
def put_book_from_json(book_id):
    contents = request.json
    update_book(book_id, contents["title"], contents["author"])
    updated_book = {'id': book_id, 'title': contents["title"], 'author': contents["author"]}
    return jsonify({"message": "Book updated successfully!", "data": updated_book}), 200

@app.route('/books/<int:book_id>', methods=['GET', 'DELETE'])
def manage_book(book_id):
    books = view_book()
    indexed_book = search_book(book_id, books)
    if indexed_book is None:
        return jsonify({"error": "Book not found"}), 404
    if request.method == 'DELETE':
        delete_book(book_id)
        return jsonify({"message": "Book Successfully Deleted"}), 200
    return jsonify(indexed_book), 200

def search_book(book_id, books):
    for book in books:
        if book[0] == book_id:
            return {"id": book[0], "title": book[1], "author": book[2]}
    return None

if __name__ == "__main__":
    app.run(debug=True)
