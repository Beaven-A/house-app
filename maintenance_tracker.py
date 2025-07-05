#Simple house maintenance tracker app created by Beaven Angels
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="House Maintenance Tracker", layout="centered")

st.title("🏠 House Maintenance Tracker")

# Initialize the session state if not already
if "maintenance_log" not in st.session_state:
    st.session_state.maintenance_log = []

st.subheader("Add a New Maintenance Entry")

with st.form("maintenance_form", clear_on_submit=True):
    entry_date = st.date_input("Date", value=date.today())
    problem = st.text_input("Problem", placeholder="e.g., Leaking pipe in kitchen")
    solution = st.text_input("Solution", placeholder="e.g., Replaced washer in pipe")
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

st.subheader("📝 Maintenance Log")

if st.session_state.maintenance_log:
    df = pd.DataFrame(st.session_state.maintenance_log)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No maintenance records yet.")
