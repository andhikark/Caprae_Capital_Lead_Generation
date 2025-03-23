import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from backend.model_trainer import predict_lead_scores  

st.set_page_config(page_title="Lead Dashboard", layout="wide")

st.title("📊 Lead Intelligence Dashboard")

DATA_PATH = "data/leads.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    st.warning("No leads found. Please run the scraper first.")
    st.stop()

try:
    df = predict_lead_scores(df)
    df.to_csv(DATA_PATH, index=False)
    st.success("✅ AI-predicted lead scores applied.")
except Exception as e:
    st.warning("⚠️ Could not apply model. Showing original scores.")
    st.text(str(e))

use_predicted = "predicted_score" in df.columns
score_column = "predicted_score" if use_predicted else "score"

st.subheader("🔥 Hot Leads (Top 10% of all leads)")
threshold = df[score_column].quantile(0.90)
hot_df = df[df[score_column] >= threshold]

if not hot_df.empty:
    st.markdown(f"Leads with score ≥ **{int(threshold)}** are considered hot.")
    for idx, row in hot_df.iterrows():
        with st.expander(f"{row['name']} — {row[score_column]} pts"):
            st.markdown(f"**Industry:** {row.get('industry', '-')}")
            st.markdown(f"**Summary:** {row.get('summary', '-')}")
            st.markdown(f"**Employees:** {row.get('employees', '-')}")
            st.markdown(f"**Tags:** {row.get('tags', '-')}")
            st.markdown(f"**Email:** {row.get('email', '-')}")
            st.markdown(f"**Website:** [{row.get('website')}]({row.get('website')})")
            st.markdown(f"**LinkedIn:** {row.get('linkedin', '-')}")
            st.markdown(f"**Tech Stack:** {row.get('tech_stack', '-')}")
            st.markdown(f"**Contact Page:** {row.get('contact_page', '-')}")
else:
    st.info("No hot leads found based on the current model output.")

st.sidebar.header("🔍 Filter Leads")
min_score = st.sidebar.slider("Minimum AI Lead Score", 0, 100, 70)
industry = st.sidebar.selectbox("Industry", ["All"] + sorted(df["industry"].dropna().unique().tolist()))
location = st.sidebar.text_input("Location Contains", "")

filtered_df = df[df[score_column] >= min_score]
if industry != "All":
    filtered_df = filtered_df[filtered_df["industry"] == industry]
if location:
    filtered_df = filtered_df[filtered_df["location"].str.contains(location, case=False, na=False)]

st.subheader("📈 Lead Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df))
col2.metric("Filtered Leads", len(filtered_df))
col3.metric("Avg. Score", round(filtered_df[score_column].mean(), 2) if not filtered_df.empty else "N/A")

st.subheader("📊 Score Distribution")
fig, ax = plt.subplots()
ax.hist(filtered_df[score_column], bins=10, color='skyblue', edgecolor='black')
ax.set_xlabel("Lead Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

st.write(f"### Showing {len(filtered_df)} leads with score ≥ {min_score}")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("🔎 Lead Details")
for idx, row in filtered_df.iterrows():
    with st.expander(f"{row['name']} — {row[score_column]} pts"):
        st.markdown(f"**Industry:** {row.get('industry', '-')}")
        st.markdown(f"**Summary:** {row.get('summary', '-')}")
        st.markdown(f"**Employees:** {row.get('employees', '-')}")
        st.markdown(f"**Tags:** {row.get('tags', '-')}")
        st.markdown(f"**Email:** {row.get('email', '-')}")
        st.markdown(f"**Website:** [{row.get('website')}]({row.get('website')})")
        st.markdown(f"**LinkedIn:** {row.get('linkedin', '-')}")
        st.markdown(f"**Tech Stack:** {row.get('tech_stack', '-')}")
        st.markdown(f"**Contact Page:** {row.get('contact_page', '-')}")

st.download_button(
    label="⬇ Download Filtered Leads as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_leads.csv",
    mime="text/csv"
)

st.markdown("### 🔁 Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Re-run Scraper"):
        st.switch_page("pages/scraper.py")
with col2:
    if st.button("⚙ Go to Automation Settings"):
        st.switch_page("pages/automation.py")
with col3:
    if st.button("📤 Push High-Scoring Leads to CRM"):
        st.success("Leads synced to CRM! (placeholder)")

st.write("---")
st.caption("Built with ❤️ for smarter outreach.")
