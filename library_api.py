# library_api.py
from flask import Flask, jsonify, request
from flasgger import Swagger
from library_core_oops import Library

app = Flask(__name__)
swagger = Swagger(app)
library = Library()

@app.route('/books', methods=['GET'])
def get_books():
    """
    Get All Books
    ---
    responses:
      200:
        description: Returns all books in the library
    """
    books = library.view_books()
    return jsonify(books), 200


@app.route('/members', methods=['GET'])
def get_members():
    """
    Get All Members
    ---
    responses:
      200:
        description: Returns all registered members
    """
    members = library.view_members()
    return jsonify(members), 200


@app.route('/book', methods=['POST'])
def add_book():
    """
    Add a New Book
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: author
        in: formData
        type: string
        required: true
      - name: genre
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Book added successfully
    """
    title = request.form.get("title")
    author = request.form.get("author")
    genre = request.form.get("genre", "")
    msg = library.add_book(title, author, genre)
    return jsonify({"message": msg}), 200


@app.route('/member', methods=['POST'])
def register_member():
    """
    Register a New Member
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: age
        in: formData
        type: integer
        required: true
      - name: contact_info
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Member registered successfully
    """
    name = request.form.get("name")
    age = request.form.get("age")
    contact = request.form.get("contact_info", "")
    msg = library.register_member(name, age, contact)
    return jsonify({"message": msg}), 200


@app.route('/borrow', methods=['POST'])
def borrow_book():
    """
    Borrow a Book
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: member
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Borrow a book by title and member name
    """
    title = request.form.get("title")
    member = request.form.get("member")
    msg = library.borrow_book(title, member)
    return jsonify({"message": msg}), 200


@app.route('/return', methods=['POST'])
def return_book():
    """
    Return a Book
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: member
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Return a borrowed book
    """
    title = request.form.get("title")
    member = request.form.get("member")
    msg = library.return_book(title, member)
    return jsonify({"message": msg}), 200


if __name__ == "__main__":
    app.run(debug=True)
