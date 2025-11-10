from library_db import init_db, seed_data, execute_query
from datetime import datetime

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    def save(self):
        query = "INSERT into books (title, author, genre, available) VALUES (?, ?, ?, 1)"
        execute_query(query, (self.title, self.author, self.genre))

class Member:
    def __init__(self, name, age, contact_info):
        self.name = name
        self.age = age
        self.contact_info = contact_info

    def register(self):
        query = "INSERT into members (name, age, contact_info) VALUES (?, ?, ?)"
        execute_query(query, (self.name, self.age, self.contact_info))

class Library:
    def __init__(self):
        init_db()

    # Add a new book
    def add_book(self, title, author, genre):
        Book(title, author, genre).save()
        return f"✅ Book '{title}' by {author} added successfully."

    # Register new member
    def register_member(self, name, age, contact_info):
        Member(name, age, contact_info).register()
        return f"✅ Member '{name}' registered successfully."

    # Borrow a book
    def borrow_book(self, book_title, member_name):
        book = execute_query("SELECT id, available FROM books WHERE LOWER(title)=LOWER(?)", (book_title,), fetch=True)
        member = execute_query("SELECT id FROM members WHERE LOWER(name)=LOWER(?)", (member_name,), fetch=True)

        if not book:
            return f"❌ Book '{book_title}' not found."
        if not member:
            return f"❌ Member '{member_name}' not found."
        if book[0][1] == 0:
            return f"⚠️ Book '{book_title}' is already borrowed."

        execute_query("UPDATE books SET available=0, borrower=? WHERE id=?", (member_name, book[0][0]))
        execute_query("INSERT INTO borrowed_books (book_id, member_id, borrow_date) VALUES (?, ?, ?)",
                      (book[0][0], member[0][0], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        return f"✅ '{book_title}' borrowed by {member_name}."

    # Return a book
    def return_book(self, book_title, member_name):
        """Mark a book as returned by a member."""
        # Fetch book and member
        book = execute_query("SELECT id FROM books WHERE LOWER(title)=LOWER(?)", (book_title,), fetch=True)
        member = execute_query("SELECT id FROM members WHERE LOWER(name)=LOWER(?)", (member_name,), fetch=True)

        if not book or not member:
            return "❌ Book or Member not found."

        book_id = book[0]["id"]
        member_id = member[0]["id"]

        # Mark the book as available again
        execute_query("UPDATE books SET available=1, borrower=NULL WHERE id=?", (book_id,))

        # Update borrowed_books record
        from datetime import datetime
        execute_query(
            """
            UPDATE borrowed_books
            SET return_date=?
            WHERE book_id=? AND member_id=? AND return_date IS NULL
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), book_id, member_id)
        )

        return f"✅ '{book_title}' returned by {member_name}."

    # Reports
    def view_reports(self):
        """Return library summary statistics."""
        total_books = execute_query("SELECT COUNT(*) AS count FROM books", fetch=True)[0]["count"]
        borrowed = execute_query("SELECT COUNT(*) AS count FROM books WHERE available=0", fetch=True)[0]["count"]
        available = total_books - borrowed
        total_members = execute_query("SELECT COUNT(*) AS count FROM members", fetch=True)[0]["count"]

        return {
            "Total Books": total_books,
            "Borrowed": borrowed,
            "Available": available,
            "Total Members": total_members
        }

    # View all books
    def view_books(self):
        """Return all books as list of dictionaries."""
        data = execute_query("SELECT id, title, author, genre, available, borrower FROM books", fetch=True)
        # ✅ data is already list[dict], no need to unpack tuples
        books = []
        for row in data:
            books.append({
                "id": row["id"],
                "title": row["title"],
                "author": row["author"],
                "genre": row["genre"],
                "available": bool(row["available"]),
                "borrower": row["borrower"]
            })
        return books

    # View all members
    def view_members(self):
        """Return all members as list of dictionaries."""
        data = execute_query("SELECT id, name, age, contact_info FROM members", fetch=True)
        members = []
        for row in data:
            members.append({
                "id": row["id"],
                "name": row["name"],
                "age": row["age"],
                "contact_info": row["contact_info"]
            })
        return members

    def delete_book(self, book_id: int):
        """Delete a book and any related borrowed_books entries."""
        book = execute_query("SELECT id, title, available FROM books WHERE id=?", (book_id,), fetch=True)
        if not book:
            return f"❌ Book with ID {book_id} not found."

        book_id_db, title, available = book[0]["id"], book[0]["title"], book[0]["available"]

        # delete any borrowed_books entries referencing this book
        execute_query("DELETE FROM borrowed_books WHERE book_id=?", (book_id_db,))

        # delete the book record itself
        execute_query("DELETE FROM books WHERE id=?", (book_id_db,))

        return f"🗑️ Book '{title}' (ID {book_id_db}) deleted successfully."


if __name__ == "__main__":
    library = Library()

    print(library.add_book("The Alchemist", "Paulo Coelho", "Fiction"))
    print(library.add_book("Atomic Habits", "James Clear", "Self-help"))

    print(library.register_member("Arun", 25, "arun@email.com"))
    print(library.register_member("Priya", 30, "priya@email.com"))

    print(library.borrow_book("The Alchemist", "Arun"))
    print(library.return_book("The Alchemist", "Arun"))

    print(library.view_reports())