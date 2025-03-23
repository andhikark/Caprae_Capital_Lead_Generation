# AI-Powered Lead Generation & Scoring Tool

This project is a powerful, modular, and intelligent web app designed to help businesses discover, score, and automate engagement with potential leads. It combines web scraping, AI enrichment (using GPT), and a machine learning model to intelligently rank leads based on multiple factors like email availability, LinkedIn presence, industry, employee size, and more.

---

## Features

- **Multi-source Scraping**: Google Maps, Crunchbase, LinkedIn (simulated), AngelList, Job Boards
- **AI Enrichment**: GPT-powered company profiling, contact page detection, employee size, tech stack, tags
- **Lead Scoring Model**: Random Forest model trained on enriched lead data
- **Streamlit Dashboard**: View leads, filter by industry/score/location, and explore details
- **Automation**: Simulate syncing to CRM, email, LinkedIn outreach
- **Export Options**: Download filtered leads as CSV

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/Caprae_Capital_Lead_Generation.git
cd Caprae_Capital_Lead_Generation
```


> ⚠️ For demo purposes, hardcoded keys are used in the code. Replace with secure environment access for production.

2. **Run the App**

```bash
streamlit run app/main.py
```

3. **Train the Lead Scoring Model (Optional)**

```bash
python app/backend/model_trainer.py
```

---

## 🔧 Folder Structure

```
├── app/
│   ├── main.py
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── scraper.py
│   │   ├── automation.py
│   ├── backend/
│   │   ├── scraper.py
│   │   ├── model_trainer.py
├── data/
│   ├── leads.csv
├── models/
│   ├── lead_model.pkl
│   ├── industry_encoder.pkl
```

---

## Further Improvements we could do in this project

- Real CRM integration (HubSpot, Salesforce, Google Sheets)
- Real email delivery (Gmail API, SendGrid integration)
- Background task runner (e.g., with APScheduler or Celery)
- Multi-language support
- Add CAPTCHA / bot detection handling for scraping
- Scraper scheduling & history tracking
- Unit + E2E testing pipeline
- Smart filtering & auto-tagging for sales personas

---

## 📣 Contribution
Feel free to fork, improve, and submit pull requests. Ideas, bug reports, and enhancements are welcome!

---

## Powered By
- OpenAI GPT-3.5
- Google Maps Places API
- Hunter.io API
- Streamlit
- Scikit-learn
- BeautifulSoup
- SerpAPI

---

Built with 💡 by Andhika Restu 
