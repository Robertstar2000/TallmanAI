# main.py

import os
import streamlit as st
from dotenv import load_dotenv
import datetime
import chromadb
import pandas as pd
from user_management import add_user, verify_pin, load_users, reset_password, save_users
from qa_module import (
    query_chroma,
    generate_ai_response,
    ensure_database,
    handle_answer,
    close_chroma_client,
    reload_database,
)

# ============================
# Load Environment Variables
# ============================
load_dotenv()

# ============================
# Path Definitions
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))
qa_data_path = os.path.join(script_dir, "QA_data", "qa_data.txt")

# ============================
# Apply Custom CSS for Styling
# ============================
def load_custom_css():
    st.markdown(
        """
        <style>
        /* Custom styling here */
        </style>
        """,
        unsafe_allow_html=True,
    )

load_custom_css()

# ============================
# User Authentication
# ============================
def authenticate_user(username, pin):
    users = load_users()
    if username in users:
        user = users[username]
        if verify_pin(pin, user["pin"]):
            if user["role"] == "new":
                return {
                    "authenticated": False,
                    "message": "Your account is pending admin approval.",
                }
            elif user["role"] == "hold":
                return {
                    "authenticated": False,
                    "message": "Your account is on hold. Please contact support.",
                }
            else:
                return {
                    "authenticated": True,
                    "message": "Login successful",
                    "role": user["role"],
                }
        else:
            return {"authenticated": False, "message": "Invalid PIN"}
    else:
        return {"authenticated": False, "message": "No matching user found"}

def handle_login(username, pin):
    if not username or not pin:
        st.error("Please enter both username and PIN.")
    else:
        auth_result = authenticate_user(username, pin)
        if auth_result["authenticated"]:
            st.session_state.user = username
            st.session_state.user_role = auth_result["role"]
            st.session_state.screen = "qa"
            st.success("Login successful!")
        else:
            st.error(auth_result["message"])

def handle_login_callback():
    username = st.session_state.login_username
    pin = st.session_state.login_pin
    handle_login(username, pin)

def display_login_screen():
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("🔐 Login")
    st.write("---")

    if "login_username" not in st.session_state:
        st.session_state.login_username = ""
    if "login_pin" not in st.session_state:
        st.session_state.login_pin = ""

    st.text_input("Username", key="login_username")
    st.text_input("PIN", type="password", key="login_pin")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("LOG IN", key="login_button", on_click=handle_login_callback)
    with col2:
        st.button("New Account", key="new_account_button", on_click=set_screen, args=("new_account",))
    with col3:
        st.button("Reset Password", key="reset_password_button", on_click=set_screen, args=("reset_password",))

def handle_new_account(username, pin, email):
    if not username or not pin or not email:
        st.error("Please fill out all fields.")
    else:
        users = load_users()
        if username in users:
            st.error("Username already exists.")
        else:
            user_data = {
                'id': str(len(users) + 1),  # generate a new id
                'username': username,
                'pin': pin,
                'email': email,
                'role': 'new'
            }
            add_user(user_data)
            st.success("Account created successfully! Awaiting admin approval.")

def handle_new_account_callback():
    username = st.session_state.new_account_username
    pin = st.session_state.new_account_pin
    email = st.session_state.new_account_email
    handle_new_account(username, pin, email)

def display_new_account_screen():
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("🆕 Create New Account")
    st.write("---")

    if "new_account_username" not in st.session_state:
        st.session_state.new_account_username = ""
    if "new_account_pin" not in st.session_state:
        st.session_state.new_account_pin = ""
    if "new_account_email" not in st.session_state:
        st.session_state.new_account_email = ""

    st.text_input("Username", key="new_account_username")
    st.text_input("PIN", type="password", key="new_account_pin")
    st.text_input("Email", key="new_account_email")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Submit", key="submit_new_account_button", on_click=handle_new_account_callback)
    with col2:
        st.button("Back to Login", key="back_to_login_button", on_click=set_screen, args=("login",))

def handle_reset_password(username, email, new_pin):
    if not username or not email or not new_pin:
        st.error("Please fill out all fields.")
    else:
        users = load_users()
        if username in users and users[username]["email"] == email:
            reset_password(username, new_pin)
            st.success("Password reset successfully!")
        else:
            st.error("Invalid username or email.")

def handle_reset_password_callback():
    username = st.session_state.reset_password_username
    email = st.session_state.reset_password_email
    new_pin = st.session_state.reset_password_new_pin
    handle_reset_password(username, email, new_pin)

def display_reset_password_screen():
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("🔒 Reset Password")
    st.write("---")

    if "reset_password_username" not in st.session_state:
        st.session_state.reset_password_username = ""
    if "reset_password_email" not in st.session_state:
        st.session_state.reset_password_email = ""
    if "reset_password_new_pin" not in st.session_state:
        st.session_state.reset_password_new_pin = ""

    st.text_input("Username", key="reset_password_username")
    st.text_input("Email", key="reset_password_email")
    st.text_input("New PIN", type="password", key="reset_password_new_pin")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Reset Password", key="reset_password_button", on_click=handle_reset_password_callback)
    with col2:
        st.button("Back to Login", key="reset_back_to_login_button", on_click=set_screen, args=("login",))

# ============================
# QA Screen
# ============================
def handle_answer_callback(collection):
    user_question = st.session_state.qa_user_question_input
    query_type = st.session_state.qa_query_type
    handle_answer(user_question, query_type, collection)
    st.session_state.user_question = user_question

def display_qa_screen(collection, handle_answer):
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("🤖 QA Assistant")
    st.write("---")

    # Radio button to select query type
    query_type = st.radio(
        "Select the subject for the prompt:",
        ["Tallman", "Sales", "Product", "Tutorial"],
        horizontal=True,
        key="qa_query_type",
    )

    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    st.text_area(
        "Your Question", value=st.session_state.user_question, key="qa_user_question_input"
    )

    st.button("Answer", key="qa_answer_button", on_click=handle_answer_callback, args=(collection,))

    if "last_response" in st.session_state:
        last_response = st.session_state.last_response
        if last_response.startswith("Error generating AI response:"):
            st.error(last_response)
        else:
            st.text_area(
                "Your Answer",
                value=last_response,
                height=200,
                key="qa_last_response",
            )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Correct Answer", key="qa_correct_answer_button", on_click=set_screen, args=("correct",))
    with col2:
        st.button("LOG OUT", key="qa_logout_button", on_click=logout)
    with col3:
        if st.session_state.get("user_role") == "admin":
            st.button("User Management", key="qa_user_management_button", on_click=set_screen, args=("user_management",))

def logout():
    st.session_state.user = None
    st.session_state.screen = "login"

# ============================
# Correct Answer Screen
# ============================
def handle_correction_callback(collection):
    correction = st.session_state.correct_correction_input
    handle_correction(correction, collection)

def handle_correction(correction, collection):
    if not correction:
        st.error("Please provide a correction before submitting.")
    else:
        user_question = st.session_state.get("user_question", "Unknown Question")
        last_response = st.session_state.get("last_response", "")
        
        # 1. Collect the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 2. Generate a reformulated answer by combining the previous answer with the correction
        new_answer = generate_ai_response(
            user_question=user_question,
            snippets=[last_response, correction],
            subject=6  # Subject index for corrections
        )
        
        # 3. Append the new QA entry to the qa_data.txt file
        try:
            append_qa_entry(current_date, user_question, new_answer, qa_data_path)
            st.success("Your correction has been applied and added to the QA data.")
        except Exception as e:
            st.error(f"Failed to append QA entry: {e}")
            return
        
        # 4. Upsert the new QA entry into the ChromaDB collection
        new_qa_entry = f"{current_date}\nQUESTION: {user_question}\nANSWER: {new_answer}\n\n"
        try:
            collection.upsert(
                documents=[new_qa_entry],
                ids=[f"{user_question}_correction_{current_date}"],
                metadatas=[{"source": f"QA_data_correction_{current_date}"}],
            )
            st.success("Correction saved to the database.")
        except Exception as e:
            st.error(f"Failed to save correction to the database: {e}")

        st.session_state.screen = "qa"

def display_correct_screen(collection):
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("✏️ Correct Answer")
    st.write("---")

    last_response = st.session_state.get("last_response", "No previous response found.")
    st.text_area(
        "AI's Answer",
        value=last_response,
        height=200,
        key="correct_answer_last",
    )

    st.text_area("Your Correction", key="correct_correction_input")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Submit Correction", key="submit_correction_button", on_click=handle_correction_callback, args=(collection,))
    with col2:
        st.button("Done", key="done_button", on_click=set_screen, args=("qa",))

# ============================
# User Management Screen
# ============================
def save_user_changes(edited_df, users):
    for idx, row in edited_df.iterrows():
        username = row["username"]
        if username in users:
            users[username]["role"] = row["role"]
    try:
        save_users(list(users.values()))
        st.success("User roles updated successfully.")
    except Exception as e:
        st.error(f"Failed to save changes: {e}")

def display_user_management_screen():
    st.image("images/tallmanlogo.png", use_column_width=True)
    st.title("👥 User Management")
    st.write("---")

    if st.session_state.get("user_role") != "admin":
        st.error("You do not have permission to access this page.")
        st.stop()

    st.write(
        "Edit user roles below. Change the role of a user by selecting from 'admin', 'user', 'hold', or 'new'."
    )

    users = load_users()

    users_df = pd.DataFrame.from_dict(users, orient="index")
    users_df = users_df.drop(columns=["pin"])
    users_df = users_df.reset_index(drop=True)
    users_df = users_df[["id", "username", "email", "role"]]

    users_df["role"] = users_df["role"].astype("category")
    users_df["role"] = users_df["role"].cat.set_categories(["admin", "user", "hold", "new"])

    edited_df = st.data_editor(
        users_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        column_config={
            "role": st.column_config.SelectboxColumn(
                "Role",
                options=["admin", "user", "hold", "new"],
            ),
        },
        height=400,
        key="user_management_editor",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Save Changes", key="save_user_changes_button", on_click=save_user_changes, args=(edited_df, users))
    with col2:
        st.button("Back to QA", key="back_to_qa_button", on_click=set_screen, args=("qa",))

    st.write("---")
    st.button("ReLoad DB", key="reload_db_button", on_click=reload_db)

def reload_db():
    with st.spinner("Reloading the database, please wait..."):
        try:
            if "chroma_client" in st.session_state:
                close_chroma_client(st.session_state.chroma_client)
                del st.session_state.chroma_client
            st.cache_resource.clear()
            collection, client = reload_database("tallman_knowledge", qa_data_path)
            st.session_state.chroma_client = client
            st.success("Database reloaded successfully!")
        except Exception as e:
            st.error(f"Failed to reload database: {e}")

# ============================
# Caching the Database Collection
# ============================
@st.cache_resource(show_spinner=False)
def load_collection():
    collection, client = ensure_database("tallman_knowledge", qa_data_path)
    st.session_state.chroma_client = client
    return collection

# ============================
# Helper Functions for Database
# ============================
def append_qa_entry(date: str, user_question: str, answer: str, qa_data_path: str):
    """
    Appends a new QA entry to the beginning of the qa_data.txt file in the specified format.
    """
    entry = f"{date}\nUSER QUESTION: {user_question}\nANSWER: {answer}\n\n"
    
    try:
        os.makedirs(os.path.dirname(qa_data_path), exist_ok=True)

        if os.path.exists(qa_data_path):
            with open(qa_data_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = ""

        new_content = entry + existing_content

        with open(qa_data_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("New QA entry prepended successfully.")
    except Exception as e:
        print(f"Failed to prepend QA entry: {e}")
        raise e

def reload_database(collection_name, qa_data_path, persist_directory="chroma_db", max_lines_per_chunk=100):
    print(f"Reloading database for collection: {collection_name}")
    chroma_client = get_chroma_client(persist_directory=persist_directory)
    
    try:
        chroma_client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Failed to delete collection '{collection_name}': {e}")
        raise e
    
    collection, chroma_client = ensure_database(collection_name, qa_data_path, persist_directory, max_lines_per_chunk)
    print(f"Collection '{collection_name}' reloaded successfully.")
    return collection, chroma_client

def get_chroma_client(persist_directory="chroma_db"):
    print("Initializing ChromaDB client...")
    try:
        chroma_client = chromadb.PersistentClient(path=persist_directory)
        print("ChromaDB client initialized successfully.")
        return chroma_client
    except Exception as e:
        print(f"Failed to initialize ChromaDB client: {e}")
        raise e

def close_chroma_client(chroma_client):
    """
    Closes the ChromaDB client to release file locks.
    """
    try:
        chroma_client.close()
        print("ChromaDB client closed successfully.")
    except AttributeError:
        print("ChromaDB client does not have a close method.")
    except Exception as e:
        print(f"Failed to close ChromaDB client: {e}")
        raise e

def set_screen(screen_name):
    st.session_state.screen = screen_name

# ============================
# Main Function to Control Navigation
# ============================
def main():
    # Initialize session state
    if "user" not in st.session_state:
        st.session_state.user = None
    if "screen" not in st.session_state:
        st.session_state.screen = "login"

    # Navigation logic
    if st.session_state.screen == "login":
        display_login_screen()
    elif st.session_state.screen == "new_account":
        display_new_account_screen()
    elif st.session_state.screen == "reset_password":
        display_reset_password_screen()
    elif st.session_state.screen == "qa":
        with st.spinner("Initializing the database, please wait..."):
            try:
                collection = load_collection()
                if not collection:
                    st.error("Database failed to load.")
                    return
            except Exception as e:
                st.error(f"Error loading database: {e}")
                return
        display_qa_screen(collection, handle_answer)
    elif st.session_state.screen == "correct":
        with st.spinner("Initializing the database, please wait..."):
            try:
                collection = load_collection()
                if not collection:
                    st.error("Database failed to load.")
                    return
            except Exception as e:
                st.error(f"Error loading database: {e}")
                return
        display_correct_screen(collection)
    elif st.session_state.screen == "user_management":
        with st.spinner("Initializing the database, please wait..."):
            try:
                collection = load_collection()
                if not collection:
                    st.error("Database failed to load.")
                    return
            except Exception as e:
                st.error(f"Error loading database: {e}")
                return
        display_user_management_screen()

if __name__ == "__main__":
    main()
