import pytest
from unittest.mock import patch, MagicMock
from library_core_oops import Library, Book, Member

# ---------------------------
# FIXTURES
# ---------------------------
@pytest.fixture
def mock_db():
    """Mock execute_query and init_db for all tests."""
    with patch("library_core_oops.execute_query") as mock_exec, \
         patch("library_core_oops.init_db") as mock_init:
        yield mock_exec

@pytest.fixture
def library(mock_db):
    return Library()

# ---------------------------
# TEST: ADD BOOK
# ---------------------------
def test_add_book(library, mock_db):
    result = library.add_book("Test Book", "Author", "Fiction")

    mock_db.assert_called_with(
        "INSERT into books (title, author, genre, available) VALUES (?, ?, ?, 1)",
        ("Test Book", "Author", "Fiction")
    )

    assert "Test Book" in result

# ---------------------------
# TEST: REGISTER MEMBER
# ---------------------------
def test_register_member(library, mock_db):
    result = library.register_member("Arun", 25, "abc@mail.com")

    mock_db.assert_called_with(
        "INSERT into members (name, age, contact_info) VALUES (?, ?, ?)", ("Arun", 25, "abc@mail.com")
    )

    assert "Arun" in result

# ---------------------------
# TEST: BORROW BOOK – SUCCESS
# ---------------------------
def test_borrow_book_success(library, mock_db):
    mock_db(
        # book exists and available
        [{"id": 1, "available": 1}],
        # member exists
        [{"id": 10}],
        # UPDATE book (no return value)
        None,
        # INSERT into borrowed_books (no return value)
        None
    )

    result = library.borrow_book("The Alchemist", "Arun")
    assert "borrowed by" in result

# ---------------------------
# TEST: BORROW BOOK – BOOK NOT FOUND
# ---------------------------
def test_borrow_book_not_found(library, mock_db):
    mock_db.side_effect = [
        [],  # 1st call: book query → not found
        [{"id": 1}]  # 2nd call: member query (won’t be used but required)
    ]

    result = library.borrow_book("Unknown Book", "Arun")
    assert "not found" in result


# ---------------------------
# TEST: BORROW BOOK – MEMBER NOT FOUND
# ---------------------------
def test_borrow_book_member_not_found(library, mock_db):
    mock_db.side_effect = [
        [{"id": 1, "available": 1}],  # book exists
        [],  # member missing
    ]

    result = library.borrow_book("The Alchemist", "Unknown")
    assert "not found" in result


# ---------------------------
# TEST: BORROW BOOK – ALREADY BORROWED
# ---------------------------
def test_borrow_book_already_borrowed(library, mock_db):
    mock_db.side_effect = [
        [(1, 0)],  # book exists but already borrowed
        [(10,)],  # member exists
    ]

    result = library.borrow_book("The Alchemist", "Arun")
    assert "already borrowed" in result


# ---------------------------
# TEST: RETURN BOOK SUCCESS
# ---------------------------
def test_return_book_success(library, mock_db):
    mock_db.side_effect = [
        [{"id": 1}],        # book exists
        [{"id": 10}],       # member exists
        None,
        None
    ]

    result = library.return_book("The Alchemist", "Arun")
    assert "returned" in result


# ---------------------------
# TEST: RETURN BOOK - NOT FOUND
# ---------------------------
def test_return_book_not_found(library, mock_db):
    mock_db.side_effect = [
        [],   # book missing
        [],   # member missing
    ]

    result = library.return_book("Unknown", "Unknown")
    assert "not found" in result


# ---------------------------
# TEST: VIEW REPORTS
# ---------------------------
def test_view_reports(library, mock_db):
    mock_db.side_effect = [
        [{"count": 10}],  # total books
        [{"count": 3}],   # borrowed
        [{"count": 5}],   # total members
    ]

    result = library.view_reports()
    assert result["Total Books"] == 10
    assert result["Borrowed"] == 3
    assert result["Available"] == 7
    assert result["Total Members"] == 5


# ---------------------------
# TEST: VIEW BOOKS
# ---------------------------
def test_view_books(library, mock_db):
    mock_db.return_value = [
        {"id": 1, "title": "A", "author": "B", "genre": "Fiction", "available": 1, "borrower": None}
    ]

    books = library.view_books()
    assert books[0]["title"] == "A"
    assert books[0]["available"] is True


# ---------------------------
# TEST: VIEW MEMBERS
# ---------------------------
def test_view_members(library, mock_db):
    mock_db.return_value = [
        {"id": 1, "name": "Arun", "age": 25, "contact_info": "mail@mail.com"}
    ]

    members = library.view_members()
    assert members[0]["name"] == "Arun"


# ---------------------------
# TEST: DELETE BOOK - SUCCESS
# ---------------------------
def test_delete_book_success(library, mock_db):
    mock_db.side_effect = [
        [{"id": 1, "title": "Test Book", "available": 1}],  # book exists
        None,  # delete borrowed_books
        None   # delete book
    ]

    result = library.delete_book(1)
    assert "deleted successfully" in result


# ---------------------------
# TEST: DELETE BOOK - NOT FOUND
# ---------------------------
def test_delete_book_not_found(library, mock_db):
    mock_db.return_value = []  # no book

    result = library.delete_book(100)
    assert "not found" in result