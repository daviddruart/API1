from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos en memoria
books = [
    {"id": 1, "title": "Cien Años de Soledad", "author": "Gabriel García Márquez", "year": 1967},
    {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949}
]

# GET todos los libros
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200

# GET un libro por ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# POST crear libro
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Title and Author are required"}), 400

    new_id = max(b["id"] for b in books) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year")
    }
    books.append(new_book)
    return jsonify(new_book), 201

# PUT actualizar libro
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["year"] = data.get("year", book["year"])
    return jsonify(book), 200

# DELETE eliminar libro
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5454, debug=True)
