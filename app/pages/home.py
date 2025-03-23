import streamlit as st

st.set_page_config(page_title="LeadGen Toolkit", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align: center;'> LeadGen Toolkit</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Your lightweight engine for smarter lead discovery, scoring & outreach.</h3>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### What This Tool Does")
st.markdown("""
- Scrape business data from Google Maps, Crunchbase, job boards, and more  
- Discover company websites, emails, LinkedIn profiles, and contacts  
- Use GPT & ML to enrich and score leads intelligently  
- Filter, export, and push qualified leads to your CRM  
""")

st.markdown("### Who It's Built For")
st.markdown("""
- **Sales teams** seeking accurate, high-intent prospects  
- **Recruiters** looking to discover hidden gems  
- **Marketers** identifying fresh B2B opportunities  
""")

st.markdown("### Ready to explore?")

col1, col2 = st.columns(2)
with col1:
    if st.button("➡ Go to Dashboard"):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("➡ Go to Scraper"):
        st.switch_page("pages/scraper.py")



