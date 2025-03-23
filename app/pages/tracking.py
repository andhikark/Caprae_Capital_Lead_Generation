import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Lead Activity Tracking", layout="centered")
st.title("Real-Time Lead Tracking & Alerts")

DATA_PATH = "data/leads.csv"
if not os.path.exists(DATA_PATH):
    st.warning("No leads to track. Please run the scraper first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

def simulate_activity_updates(df):
    updates = []
    for i, row in df.iterrows():
        activity = random.choice(["New funding raised 💰", "Hiring spike 🚀", "New product launch 🧪", "Website traffic surge 📈", None])
        if activity:
            updates.append({
                "name": row["name"],
                "industry": row["industry"],
                "location": row["location"],
                "activity": activity
            })
    return pd.DataFrame(updates)

if st.button("🔄 Check for New Lead Activity"):
    activity_df = simulate_activity_updates(df)
    if not activity_df.empty:
        st.success(f"{len(activity_df)} leads showed new activity!")
        st.dataframe(activity_df)
        if st.button("📤 Send Me This Update (Simulated)"):
            st.info("Email or Slack alert sent! (simulated)")
    else:
        st.info("No activity changes at the moment. Try again later.")
else:
    st.caption("Click the button above to simulate checking for live updates.")
