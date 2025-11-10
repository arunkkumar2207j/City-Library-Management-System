from library_db import init_db, seed_data
# Book Data Structures & Preparation (Sample)
# books = [
#     {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "fantasy", "available": True, "borrower": None},
#     {"id": 2, "title": "Atomic Habits", "author": "James Clear", "genre": "science fiction", "available": False, "borrower": "Arun"},
# ]

books = []
book_id = 1
# Member Data Structures & Preparation (Sample)
# members = [
#     {"id": 1, "name": "Arun", age=22, contact_info="", "borrowed_books": []},
#     {"id": 2, "name": "Priya", age=30, contact_info="", "borrowed_books": []},
# ]
members = []
member_id = 1

def view_books():
    return books

def add_book(title, author, genre):
    global book_id
    new_book = {"id": book_id, "title":title, "author":author, "genre": genre, "available": True, "borrower": ""}
    books.append(new_book)
    book_id += 1
    return f"Book title: '{title}' successfully added"

def borrow_book(book_title, member_name):
    for book in books:
        if book["title"].lower() == book_title.lower():
            if not book["available"]:
                return f"'{book_title}' is already borrowed."
            book["available"] = False
            book["borrower"] = member_name
            for member in members:
                if member["name"].lower() == member_name.lower():
                    member["borrowed_books"].append(book_title)
            return f"'{book_title}' borrowed by {member_name}."
    return "Book not found."

def return_book(book_title, member_name):
    for book in books:
        if book["title"].lower() == book_title.lower():
            book["available"] = True
            book["borrower"] = None
            for member in members:
                if member["name"].lower() == member_name.lower():
                    member["borrowed_books"].remove(book_title)
            return f"'{book_title}' returned by {member_name}."
    return "Book not found."

def register_member(member_name, age, contact_info):
    global member_id
    new_member = {"id": member_id, "name": member_name, "age":int(age), "contact_info":int(contact_info), "borrowed_books":[]}
    members.append(new_member)
    member_id += 1
    return f"Member name: '{member_name}' successfully registered"

def view_members():
    return members

def view_reports():
    total_books = len(books)
    borrowed = sum(not b['available'] for b in books)
    available = total_books - borrowed
    return {"Total Books":total_books, "borrowed":borrowed, "available": available}

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")
    seed_data()
    print("🎉 Library setup complete with sample data!")

    # add_book("Python for Beginners", "Arun")
    # add_book("Python for Intermediate", "Kumar")
    # add_book("Python for Professional", "Sai")
    # register_member("Joseph")
    # register_member("Jemima")
    # register_member("Stefani")
    # all_books = view_books()
    # print(f"Books: {all_books}")
    # all_members = view_members()
    # print(f"Members: {all_members}")
    # report = view_reports()
    # print(f"Report: {report}")
    # borrow_book("Python for Beginners", "Jemima")
    # borrow_book("Python for Intermediate", "Stefani")
    # all_books = view_books()
    # print(f"Books: {all_books}")
    # all_members = view_members()
    # print(f"Members: {all_members}")
    # report = view_reports()
    # print(f"Report: {report}")
    # return_book("Python for Beginners", "Jemima")
    # all_books = view_books()
    # print(f"Books: {all_books}")
    # report = view_reports()
    # print(f"Report: {report}")