def clear_inputs(st, *keys):
    for key in keys:
        if key in st.session_state:
            st.session_state[key] = ""

def schedule_clear_inputs(st, *keys):
    """Safely clear inputs after the next rerun."""
    st.session_state.to_clear = keys
    # st.rerun()

def process_clear_queue(st):
    """Executed at top of app to process scheduled input resets."""
    if "to_clear" in st.session_state:
        for key in st.session_state.to_clear:
            st.session_state[key] = ""
        del st.session_state.to_clear

def refresh_books(library):
    """Fetch the latest book list from DB."""
    return library.view_books()
