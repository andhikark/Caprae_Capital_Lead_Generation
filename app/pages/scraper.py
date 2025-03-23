import streamlit as st
import pandas as pd
import os

from backend.scraper import (
    scrape_google_maps_places,
    scrape_crunchbase_mock,
    scrape_linkedin_companies,
    scrape_job_board,
    scrape_angellist_startups,
    combine_sources
)

st.set_page_config(page_title="Lead Scraper", layout="centered")
st.title("🕵️ Lead Generator")

st.write("Enter the keyword and location, and select the sources to scrape verified leads.")

query = st.text_input("🔍 Keyword (e.g. Fintech, Marketing Agency)")
location = st.text_input("📍 Location (e.g. New York, London)")
sources = st.multiselect(
    "🌐 Data Sources",
    ["Google Maps", "Crunchbase", "LinkedIn", "Job Boards", "AngelList"],
    default=["Google Maps"]
)
max_results = st.slider("Max results per source", 5, 50, 15)

if st.button("🚀 Start Scraping"):
    if not query or not location:
        st.error("Please enter both a keyword and location.")
    else:
        st.info("Scraping in progress...")

        all_dataframes = []

        if "Google Maps" in sources:
            with st.spinner("Scraping Google Maps..."):
                df_google = scrape_google_maps_places(query, location, max_results)
                all_dataframes.append(df_google)

        if "Crunchbase" in sources:
            with st.spinner("Scraping Crunchbase..."):
                df_cb = scrape_crunchbase_mock(query, location, max_results)
                all_dataframes.append(df_cb)

        if "LinkedIn" in sources:
            with st.spinner("Scraping LinkedIn (mock)..."):
                df_li = scrape_linkedin_companies([f"{query} {i}" for i in range(1, max_results + 1)])
                all_dataframes.append(df_li)

        if "Job Boards" in sources:
            with st.spinner("Scraping Job Boards..."):
                df_job = scrape_job_board(query, location, max_results)
                all_dataframes.append(df_job)

        if "AngelList" in sources:
            with st.spinner("Scraping AngelList..."):
                df_angel = scrape_angellist_startups(query, location, max_results)
                all_dataframes.append(df_angel)

        if all_dataframes:
            df_all = combine_sources(*all_dataframes)
            os.makedirs("data", exist_ok=True)
            df_all.to_csv("data/leads.csv", index=False)
            st.success(f"✅ Scraping complete! {len(df_all)} leads collected.")
            st.dataframe(df_all)

            if st.button("➡ Go to Dashboard"):
                st.switch_page("pages/dashboard.py")
