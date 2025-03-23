import streamlit as st
import os

st.set_page_config(page_title="AI-Powered Lead Intelligence", layout="wide")

if "use_case" not in st.session_state:
    st.session_state["use_case"] = None 

st.sidebar.title("🔍 Navigation")
st.sidebar.markdown("Use the menu below to explore different features:")

if st.sidebar.button("🏠 Home"):
    st.switch_page("pages/home.py")
if st.sidebar.button("📊 Dashboard"):
    st.switch_page("pages/dashboard.py")
if st.sidebar.button("🕵️ Scraper"):
    st.switch_page("pages/scraper.py")
if st.sidebar.button("⚙ Automation Settings"):
    st.switch_page("pages/automation.py")
if st.sidebar.button("📢 Live Lead Tracking"):
    st.switch_page("pages/tracking.py")

st.switch_page("pages/home.py")
