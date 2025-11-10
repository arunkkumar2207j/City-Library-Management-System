import streamlit as st
from library_db import init_db
from library_core_oops import Library
import inspect

# Run init_db() once per session
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True
    st.info("✅ Library database initialized.")

# Now safely use your Library class
library = Library()

menu_options = ["Dashboard Home", "Add Book", "Register Member", "Borrow Book", "Return Book", "View Books", "View Members", "Reports & Queries", "🧩 DB Debug Panel"]

st.sidebar.selectbox(
    "📚 Choose Menu",
    menu_options,
    key="menu"
)
menu = st.session_state.menu

# st.write("📄 Library class source file:", inspect.getsourcefile(Library))
# st.write("📚 Library class methods:", dir(Library))
# print(library.view_books()[0])
# print(library.view_reports())
print(library.delete_book(2))  # change to an existing book ID
print(library.view_books())

if menu == "Add Book":
    st.subheader("➕ Add a New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")

    if st.button("Save Book"):
        if not title.strip() or not author.strip():
            st.warning("⚠️ Title and Author are required.")
        else:
            msg = library.add_book(title, author, genre)
            st.success(msg)

elif menu == "Register Member":
    st.subheader("👤 Register New Member")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    contact = st.text_input("Contact Info (email or phone)")

    if st.button("Register Member"):
        if not name.strip():
            st.warning("⚠️ Name cannot be empty.")
        else:
            msg = library.register_member(name, age, contact)
            st.success(msg)

elif menu == "Borrow Book":
    st.subheader("📖 Borrow a Book")

    books = [b for b in library.view_books() if b["available"]]
    members = [m["name"] for m in library.view_members()]

    if not books:
        st.warning("No books available for borrowing.")
    else:
        book_titles = [b["title"] for b in books]
        book_title = st.selectbox("Select Book", book_titles)
        member_name = st.selectbox("Select Member", members)

        if st.button("Borrow Book"):
            msg = library.borrow_book(book_title, member_name)
            st.success(msg)

elif menu == "Return Book":
    st.subheader("🔁 Return a Book")

    borrowed_books = [b for b in library.view_books() if not b["available"]]
    members = [m["name"] for m in library.view_members()]

    if not borrowed_books:
        st.info("No borrowed books at the moment.")
    else:
        book_titles = [b["title"] for b in borrowed_books]
        book_title = st.selectbox("Select Book to Return", book_titles)
        member_name = st.selectbox("Select Member", members)

        if st.button("Return Book"):
            msg = library.return_book(book_title, member_name)
            st.success(msg)

elif menu == "View Books":
    st.subheader("📚 All Books")

    # --- Always pull fresh data from the DB ---
    books = library.view_books()

    if not books:
        st.info("No books found in the library database.")
    else:
        import pandas as pd
        df = pd.DataFrame(books)
        st.dataframe(df)

        st.markdown("### 🗑️ Delete a Book")
        book_titles = [f"{b['id']} — {b['title']} ({b['author']})" for b in books]
        book_choice = st.selectbox("Select a book to delete", book_titles)

        selected_id = int(book_choice.split(" — ")[0])

        if st.button("🗑️ Delete Selected Book"):
            st.session_state.confirm_delete = selected_id

        if "confirm_delete" in st.session_state:
            book_id = st.session_state.confirm_delete
            st.warning(f"Are you sure you want to delete book ID {book_id}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, delete it"):
                    msg = library.delete_book(book_id)
                    st.success(msg)

                    # ✅ Force a fresh DB fetch after delete
                    if "confirm_delete" in st.session_state:
                        del st.session_state.confirm_delete

                    # Clear Streamlit cache and rerun
                    st.cache_data.clear()
                    st.rerun()

            with col2:
                if st.button("❌ Cancel"):
                    st.info("Deletion canceled.")
                    del st.session_state.confirm_delete


elif menu == "View Members":
    st.subheader("View Members")
    all_members = library.view_members()
    if all_members:
        st.table(all_members)
    else:
        st.info("No members found in the library database.")

elif menu == "Reports & Queries":
    st.subheader("📊 Reports & Queries")

    all_books = library.view_books()
    all_members = library.view_members()
    reports = library.view_reports()

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📘 Total Books", reports["Total Books"])
    col2.metric("📗 Available", reports["Available"])
    col3.metric("📕 Borrowed", reports["Borrowed"])
    col4.metric("👥 Members", reports["Total Members"])

    st.divider()

    # Search feature
    search = st.text_input("🔍 Search by Title or Author")
    if search.strip():
        filtered = [b for b in all_books if search.lower() in b["title"].lower() or search.lower() in b["author"].lower()]
        if filtered:
            st.success(f"Found {len(filtered)} matching book(s):")
            st.table(filtered)
        else:
            st.warning("No matching results found.")

elif menu == "Dashboard Home":
    st.title("🏠 Library Dashboard")
    st.markdown("### Welcome to City Library Management System")

    # --- Load live data from the database ---
    reports = library.view_reports()
    all_books = library.view_books()
    all_members = library.view_members()

    # --- Summary Metrics ---
    st.markdown("#### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Books", reports["Total Books"])
    col2.metric("📗 Available", reports["Available"])
    col3.metric("📕 Borrowed", reports["Borrowed"])
    col4.metric("👥 Members", reports["Total Members"])

    st.divider()

    # --- Chart 1: Pie Chart for Book Availability ---
    import matplotlib.pyplot as plt

    st.markdown("#### 📊 Books Status Overview")
    fig, ax = plt.subplots()
    labels = ["Available", "Borrowed"]
    sizes = [reports["Available"], reports["Borrowed"]]
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        shadow=True
    )
    ax.axis("equal")
    st.pyplot(fig)

    st.divider()

    # --- Chart 2: Genre-wise Book Distribution ---
    import pandas as pd

    st.markdown("#### 📚 Books by Genre")
    df = pd.DataFrame(all_books)

    if not df.empty:
        genre_count = df["genre"].value_counts()
        st.bar_chart(genre_count)
    else:
        st.info("No books available to display genre distribution.")

    st.divider()

    # --- Member Overview ---
    st.markdown("#### 👤 Active Borrowers")
    borrowed_members = [m for m in all_members if m.get("borrowed_books", [])]

    if borrowed_members:
        st.table(borrowed_members)
    else:
        st.info("No active borrowed members at the moment.")

elif menu == "Reports & Queries":
    st.title("📊 Reports & Queries")

    all_books = library.view_books()
    all_members = library.view_members()
    reports = library.view_reports()

    # --- Summary metrics ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📘 Total Books", reports["Total Books"])
    col2.metric("📗 Available", reports["Available"])
    col3.metric("📕 Borrowed", reports["Borrowed"])
    col4.metric("👥 Members", reports["Total Members"])

    st.divider()

    # --- Borrowed Books Summary Table ---
    st.markdown("### 🔄 Borrowed Books Summary")

    from library_db import execute_query
    import pandas as pd

    borrowed_records = execute_query("""
        SELECT 
            bb.id AS record_id,
            b.title AS book_title,
            m.name AS member_name,
            bb.borrow_date,
            bb.return_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        JOIN members m ON bb.member_id = m.id
        ORDER BY bb.id DESC
    """, fetch=True)

    if borrowed_records:
        # Replace NULL return dates with a friendly message
        for record in borrowed_records:
            record["return_date"] = record["return_date"] or "⏳ Not Returned Yet"

        df = pd.DataFrame(borrowed_records)
        st.dataframe(df, use_container_width=True)
        st.caption(f"Total Transactions: {len(df)}")
    else:
        st.info("No borrowed book records found.")

    st.divider()

    # --- Search functionality ---
    st.markdown("### 🔍 Search Books by Title or Author")
    search_term = st.text_input("Enter search keyword:")
    if search_term.strip():
        filtered = [
            b for b in all_books
            if search_term.lower() in b["title"].lower()
            or search_term.lower() in b["author"].lower()
        ]
        if filtered:
            st.success(f"Found {len(filtered)} matching book(s):")
            st.table(filtered)
        else:
            st.warning("No matches found.")


