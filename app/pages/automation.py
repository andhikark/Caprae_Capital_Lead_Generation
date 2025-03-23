import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Automation Settings", layout="centered")
st.title("⚙ Workflow Automation Settings")

DATA_PATH = "data/leads.csv"

if not os.path.exists(DATA_PATH):
    st.warning("No leads found. Please run the scraper first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

st.sidebar.title("Automation Toggles")

auto_crm = st.sidebar.checkbox("Auto-sync high-scoring leads to CRM", value=True)
auto_email = st.sidebar.checkbox("Send outreach email automatically", value=False)
auto_linkedin = st.sidebar.checkbox("Send LinkedIn message automatically", value=False)

score_threshold = st.sidebar.slider("Minimum Score for Automation", 60, 100, 85)

filtered = df[df["score"] >= score_threshold]

st.write(f"### {len(filtered)} leads meet the automation threshold (≥ {score_threshold})")
st.dataframe(filtered)

if st.button("Sync Leads to CRM (Google Sheet / Placeholder)"):
    filtered.to_csv("data/synced_leads.csv", index=False)
    st.success("Leads synced to 'data/synced_leads.csv' (simulate CRM push)")

if st.button("✉ Send Outreach Emails (Simulated)"):
    st.success("Email outreach triggered for high-score leads! (simulated)")

if st.button("🔗 Send LinkedIn Message (Simulated)"):
    st.success("LinkedIn messages sent to qualified leads! (simulated)")

st.write("---")
