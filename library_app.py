import streamlit as st
from library_core import *
from utils.index import schedule_clear_inputs, process_clear_queue

# always call this early
process_clear_queue(st)

st.set_page_config(page_title="City Library Management", layout="wide")
st.title("City Library Management")

menu_options = ["Add Book", "View Books", "Borrow Book", "Return Book",  "Register Member", "View Members", "Reports & Queries"]

# --------------------------
# Handle queued navigation (SAFE)
# --------------------------
if "next_page" in st.session_state:
    st.session_state.menu = st.session_state.next_page
    del st.session_state.next_page


# Initialize session state
if "menu" not in st.session_state:
    st.session_state.menu = menu_options[0]

# --------------------------
# Sidebar menu (existing code)
# --------------------------
st.sidebar.title("📚 Navigation")
st.sidebar.selectbox(
    "Choose Menu",
    menu_options,
    key="menu"
)
# Keep session state synced
menu = st.session_state.menu

if menu == "Add Book":
    st.subheader("Add Book")
    title = st.text_input("Title", key="add_title")
    author = st.text_input("Author", key="add_author")
    genre = st.text_input("Genre", key="add_genre")
    if st.button("Save Book"):
        if title.strip() == "" or author.strip() == "" or genre.strip() == "":
            st.warning("Title, Author and Genre cannot be empty")
        else:
            add_book(title, author, genre)
            st.success("Title, Author and Genre Saved")
            # --- Clear the inputs *before* the next rerun cycle ---
            schedule_clear_inputs(st, "add_title", "add_author", "add_genre")
            st.rerun()

elif menu == "View Books":
    st.subheader("View Books")
    all_books = view_books()
    if len(all_books) > 0:
        st.table(all_books)
    else:
        st.write("Books List is empty")
    if st.button("Add Book"):
        st.session_state.next_page = "Add Book"
        st.rerun()

elif menu == "Borrow Book":
    st.subheader("Borrow Book")
    member = st.selectbox("Select Member", [m["name"] for m in members])
    book = st.selectbox("Select Book", [b["title"] for b in books])
    if st.button("Borrow Book"):
        st.success(borrow_book(book, member))

elif menu == "Return Book":
    st.subheader("Return Book")
    member = st.selectbox("Select Member", [m["name"] for m in members])
    borrowed_books = next((m["borrowed_books"] for m in members if m["name"] == member), [])
    book = st.selectbox("Select Book", borrowed_books)
    if st.button("Return Book"):
        st.success(return_book(book, member))

elif menu == "Register Member":
    st.subheader("Register Member")
    member = st.text_input("Name", key="add_name")
    age = st.text_input("Age", key="add_age")
    contact_info = st.text_input("Contact Number", key="add_contact")
    if st.button("Add Member"):
        if member.strip() == "" or age.strip() == "" or contact_info.strip() == "":
            st.warning("Name, Age and Contact Info cannot be empty")
        else:
            register_member(member, age, contact_info)
            st.success("Name, Age and Contact Info Saved")
            # --- Clear the inputs *before* the next rerun cycle ---
            schedule_clear_inputs(st, "add_name", "add_age", "add_contact")
            st.rerun()

elif menu == "View Members":
    st.subheader("View Members")
    all_members = view_members()
    if len(all_members) > 0:
        st.table(all_members)
    else:
        st.write("No Members Registered yet.")
    if st.button("Add Member"):
        st.session_state.next_page = "Register Member"
        st.rerun()

elif menu == "Reports & Queries":
    st.subheader("Reports & Queries")
    # st.json(view_reports())
    all_members = view_members()
    all_books = view_books()

    # -------------------------------
    # 🔍 Book Search Section
    # -------------------------------
    st.text("🔍 Search Books by Title or Author")

    search_query = st.text_input("Enter book title or author name or genra", key="search_books")
    if search_query.strip():
        # Case-insensitive partial match for title or author
        results = [
            b for b in all_books
            if search_query.lower() in b["title"].lower()
               or search_query.lower() in b["author"].lower()
               or search_query.lower() in b["genre"].lower()
        ]

        if results:
            st.success(f"✅ Found {len(results)} matching book(s):")
            st.table(results)
        else:
            st.warning("⚠️ No books found matching your search.")
    else:
        st.info("Type in a book title or author to search.")

    st.divider()
    if all_books:
        available_books = [b for b in all_books if not b["borrower"]]
        st.text("Available Books")
        if available_books:
            st.table(available_books)
        else:
            st.info("All books are currently borrowed.")
    else:
        st.warning("📚 No books in the system yet.")

    st.divider()
    if all_members:
        borrowed_books_members = [m for m in all_members if m["borrowed_books"]]
        st.text("Members Who Borrowed Books")
        if borrowed_books_members:
            st.table(borrowed_books_members)
        else:
            st.info("No members have borrowed books yet.")
    else:
        st.warning("👤 No members registered yet.")
