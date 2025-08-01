# Simple house maintenance tracker app created by Beaven Angels
import streamlit as st
import pandas as pd
from datetime import date
import os

# Constants
CSV_FILE = "maintenance_log.csv"
USERNAME = "Beaven"
PASSWORD = "22091"

# Page setup
st.set_page_config(page_title="🏠 House Maintenance Tracker", layout="centered")
st.title("🏠 House Maintenance Tracker")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Load data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Problem", "Solution", "Status"])

# Save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Delete a record
def delete_record(index_to_delete):
    df = load_data()
    df = df.drop(index=index_to_delete).reset_index(drop=True)
    save_data(df)
    st.success("Record deleted.")
    st.rerun()

# Login
if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔐 Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

# Load existing data
df = load_data()

# Admin-only input form
if st.session_state.authenticated:
    st.subheader("➕ Add a New Maintenance Entry")
    with st.form("maintenance_form", clear_on_submit=True):
        entry_date = st.date_input("Date", value=date.today())
        problem = st.text_input("Problem", placeholder="e.g., Broken faucet")
        solution = st.text_input("Solution", placeholder="e.g., Replaced faucet")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            if problem and solution:
                new_entry = {
                    "Date": entry_date,
                    "Problem": problem,
                    "Solution": solution,
                    "Status": status,
                }
                new_df = pd.DataFrame([new_entry])
                df = pd.concat([df, new_df], ignore_index=True)
                save_data(df)
                st.success("Entry added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

# Display records
st.subheader("📝 Maintenance Log")

if df.empty:
    st.info("No maintenance records yet.")
else:
    st.dataframe(df, use_container_width=True)

    if st.session_state.authenticated:
        st.subheader("🗂️ Manage Entries")
        for i, row in df.iterrows():
            with st.expander(f"{row['Date']} - {row['Problem']}"):
                st.write(f"**Solution:** {row['Solution']}")
                st.write(f"**Status:** {row['Status']}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        delete_record(i)
                with col2:
                    st.write("✔️ Record ID:", i)
