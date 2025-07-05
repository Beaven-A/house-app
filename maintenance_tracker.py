#Simple house maintenance tracker app created by Beaven Angels
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="House Maintenance Tracker", layout="centered")
st.title("🏠 House Maintenance Tracker")

# Hardcoded credentials
USERNAME = "Beaven"
PASSWORD = "22091"

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Initialize maintenance log
if "maintenance_log" not in st.session_state:
    st.session_state.maintenance_log = []

# Login form
if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔐 Login to Add Entries")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

# Show form only if authenticated
if st.session_state.authenticated:
    st.subheader("➕ Add a New Maintenance Entry")
    with st.form("maintenance_form", clear_on_submit=True):
        entry_date = st.date_input("Date", value=date.today())
        problem = st.text_input("Problem", placeholder="e.g., Leaking pipe in kitchen")
        solution = st.text_input("Solution", placeholder="e.g., Replaced washer")
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
                st.session_state.maintenance_log.append(new_entry)
                st.success("Entry added successfully!")
            else:
                st.error("Please fill in all fields.")
else:
    st.info("Login to add or edit maintenance records.")

# Always show maintenance log
st.subheader("📝 Maintenance Log")
if st.session_state.maintenance_log:
    df = pd.DataFrame(st.session_state.maintenance_log)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No maintenance records yet.")
