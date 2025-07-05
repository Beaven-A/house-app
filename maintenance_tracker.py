import streamlit as st
import pandas as pd
from datetime import date
import os

# App config
st.set_page_config(page_title="🏠 House Maintenance Tracker", layout="centered")
st.title("🏠 House Maintenance Tracker")

# Credentials
USERNAME = "Beaven"
PASSWORD = "22091"
CSV_FILE = "maintenance_log.csv"

# Auth state
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

# Login form
if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔐 Admin Login to Edit")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid username or password")

# Load current data
df = load_data()

# Show maintenance log
st.subheader("📝 Maintenance Log")

if df.empty:
    st.info("No maintenance records yet.")
else:
    st.write("All maintenance records:")

    # Editable table (only for admin)
    if st.session_state.authenticated:
        edited_df = st.experimental_data_editor(df, use_container_width=True, num_rows="dynamic")
        if st.button("💾 Save Changes"):
            save_data(edited_df)
            st.success("Changes saved.")
            st.rerun()
    else:
        st.dataframe(df, use_container_width=True)

# Admin-only Add/Delete section
if st.session_state.authenticated:
    st.subheader("➕ Add New Maintenance Entry")
    with st.form("add_form", clear_on_submit=True):
        entry_date = st.date_input("Date", value=date.today())
        problem = st.text_input("Problem")
        solution = st.text_input("Solution")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        add_entry = st.form_submit_button("Add Entry")

        if add_entry:
            if problem and solution:
                new_row = {"Date": entry_date, "Problem": problem, "Solution": solution, "Status": status}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success("Entry added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

    st.subheader("🗑️ Delete Individual Record")
    for i in df.index:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 4, 4, 4, 3, 1])
        with col1:
            st.markdown(f"**{i+1}.**")
        with col2:
            st.markdown(f"{df.at[i, 'Date']}")
        with col3:
            st.markdown(f"{df.at[i, 'Problem']}")
        with col4:
            st.markdown(f"{df.at[i, 'Solution']}")
        with col5:
            st.markdown(f"{df.at[i, 'Status']}")
        with col6:
            if st.button("❌", key=f"delete_{i}"):
                df = df.drop(i).reset_index(drop=True)
                save_data(df)
                st.success("Deleted successfully.")
                st.rerun()
