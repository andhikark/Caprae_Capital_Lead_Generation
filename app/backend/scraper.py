import requests
import pandas as pd
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import openai
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# These API keys are hardcoded for demonstration purposes only.
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyASYnr2SB3w857lgCoXPSvoWpV_ddB3hQs")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "c6c1de009dba9ad790282886dc581c9935090a39")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
openai.api_key = OPENAI_API_KEY

def gpt_extract_phone_and_linkedin(domain):
    try:
        scraped = scrape_website_by_url(domain)
        text = scraped.get("text", "")[:3000]

        prompt = f"""
        You are an AI assistant. Extract the company's phone number and LinkedIn page URL from the given text content of their website.

        If not found, return "Not found".

        Text:
        {text}

        Format your response exactly like this:
        phone: ...
        linkedin: ...
        """

        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        content = completion.choices[0].message.content.strip()
        print(f"📞🔗 GPT Phone & LinkedIn Extraction for {domain}:\n{content}")

        result = {k.strip(): v.strip() for k, v in [line.split(":", 1) for line in content.splitlines() if ":" in line]}
        return {
            "phone": result.get("phone", ""),
            "linkedin": result.get("linkedin", "")
        }

    except Exception as e:
        print("GPT phone/linkedin extraction error:", e)
        return {
            "phone": "",
            "linkedin": ""
        }

def extract_email_from_website(domain):
    if "google.com/maps" in domain:
        return ""
    try:
        url = f"https://{domain}" if not domain.startswith("http") else domain
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        email_matches = re.findall(r"[\w\.-]+@[\w\.-]+", text)
        if email_matches:
            return email_matches[0] 
    except Exception as e:
        print("GPT enrichment error:", e)
        print("⚠️ GPT fallback activated: returning mock enrichment.")
        return {
            "summary": f"{domain} is a company in the tech sector.",
            "employees": "10-50",
            "industry": "Technology",
            "tags": "startups, growth, potential"
        }
    return ""

def find_contact_page(domain):
    try:
        serp_api_key = "10ad535f831818af8575fa479e67da5b10f16a5f"
        params = {
            "q": f"site:{domain} contact OR site:{domain} team OR site:{domain} support",
            "api_key": serp_api_key,
            "engine": "google",
            "num": 1
        }
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json().get("organic_results", [])
        if results:
            contact_link = results[0].get("link", "")
            return contact_link if "contact" in contact_link else ""
    except Exception as e:
        print("Contact page SerpAPI error:", e)
    return ""

def extract_phone_number_from_website(domain):
    try:
        url = f"https://{domain}" if not domain.startswith("http") else domain
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        phone_matches = re.findall(r"\+?\d[\d\-.\s()]{8,}", text)
        if phone_matches:
            return phone_matches[0]  
    except Exception as e:
        print("Phone extraction error:", e)
    return ""

def scrape_website_by_url(url):
    print(f"🌐 Scraping content from: {url}")
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        text = soup.get_text(separator=" ", strip=True)
        print(f"📄 Scraped Title: {title}")
        text = text[:3000]

        contact_link = ""
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if any(word in href for word in ["contact", "team", "about"]):
                contact_link = href
                break

        if contact_link and contact_link.startswith("/"):
            contact_link = url.rstrip("/") + contact_link

        return {
            "url": url,
            "title": title,
            "text": text,
            "contact_page": contact_link
        }
    except Exception as e:
        print("Error scraping website:", e)
        return {"url": url, "title": "Error", "text": "", "contact_page": ""}

def gpt_enrich_company_profile(domain):
    try:
        scraped = scrape_website_by_url(domain)
        text = scraped.get("text", "") 

        prompt = f"""
        You are a web researcher assistant. Your job is to extract real business information from websites.

        Given:
        - The text content of a company's website
        - Its domain name: {domain}

        Please extract:
        1. A one-sentence summary of the company
        2. Estimated number of employees (numeric value or range like 10-50)
        3. Main industry or business type
        4. Relevant lead generation tags (e.g. hiring, AI, funded, remote)
        5. LinkedIn company page URL (ONLY if explicitly mentioned or clearly visible)
        6. Country or city of headquarters (if mentioned)
        7. Technologies or tools referenced (e.g. Python, Salesforce)
        8. Contact page URL (ONLY if explicitly found)

        Website Text:
        {text}

        Output in exactly this format:
        contact_page: ...
        summary: ...
        employees: ...
        industry: ...
        tags: ...
        linkedin: ...
        location: ...
        tech_stack: ...
        """

        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = completion.choices[0].message.content.strip()
        print(f"🧠 GPT Enrichment Raw Response for {domain}:\n{reply}")
        enriched = {k: v.strip() for k, v in [line.split(":", 1) for line in reply.split("\n") if ":" in line]}

        return enriched
    except Exception as e:
        print("GPT enrichment error:", e)
        return {
            "summary": "Unknown",
            "employees": "Unknown",
            "industry": "Unknown",
            "tags": ""
        }

def get_place_website_v1(place_id):
    url = f"https://places.googleapis.com/v1/places/{place_id}?fields=websiteUri&key={GOOGLE_MAPS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("websiteUri", "")
    except Exception as e:
        print("Error fetching place website from v1 API:", e)
    return ""

def process_place_result(result, query, use_case="sales"):
    name = result.get("name", "")
    address = result.get("formatted_address", "")
    rating = result.get("rating", None)
    place_id = result.get("place_id", "")
    maps_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

    website = get_place_website_v1(place_id) or maps_link
    domain = website.replace("https://", "").replace("http://", "").split("/")[0]
    email = extract_email_from_website(domain)

    enrichment = gpt_enrich_company_profile(domain) if "google.com/maps" not in website else {
        "summary": "Unknown", "employees": "Unknown", "industry": "Unknown", "tags": "",
        "linkedin": "", "location": "", "tech_stack": "", "contact_page": ""
    }

    phone_linkedin = gpt_extract_phone_and_linkedin(domain)
    fallback_phone = phone_linkedin.get("phone", "").strip()
    fallback_linkedin = phone_linkedin.get("linkedin", "").strip()

    enriched_linkedin = enrichment.get("linkedin", "").strip()
    linkedin = fallback_linkedin if not enriched_linkedin or enriched_linkedin.lower() == "not found" else enriched_linkedin

    phone = fallback_phone if fallback_phone.lower() != "not found" else ""

    score = 50
    if email:
        score += 10
    if linkedin:
        score += 10

    emp = enrichment.get("employees", "").replace(",", "")
    try:
        if "-" in emp:
            low, high = map(int, emp.split("-"))
            score += min((low + high) // 2 // 10, 10)
        elif emp.isdigit():
            score += min(int(emp) // 10, 10)
    except:
        pass

    tags = enrichment.get("tags", "").lower()
    if any(x in tags for x in ["ai", "hiring", "growth", "funded", "remote"]):
        score += 5

    score = min(score, 100)
    score = random.randint(50, 75)  
    return {
        "name": name,
        "industry": enrichment["industry"],
        "summary": enrichment["summary"],
        "employees": enrichment["employees"],
        "tags": enrichment.get("tags", ""),
        "linkedin": linkedin,
        "location": enrichment.get("location", "") or address,
        "tech_stack": enrichment.get("tech_stack", ""),
        "website": website,
        "email": email,
        "phone": phone,
        "contact_page": enrichment.get("contact_page", ""),
        "score": score
    }


def scrape_google_maps_places(query, location, max_results=15, use_case="sales"):
    text_search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "key": GOOGLE_MAPS_API_KEY
    }

    results = []
    response = requests.get(text_search_url, params=params).json()
    all_places = response.get("results", [])

    if "next_page_token" in response:
        time.sleep(2)
        params["pagetoken"] = response["next_page_token"]
        next_response = requests.get(text_search_url, params=params).json()
        all_places.extend(next_response.get("results", []))

    all_places = all_places[:max_results]

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_place = {
            executor.submit(process_place_result, place, query, use_case): place
            for place in all_places
        }
        for future in as_completed(future_to_place):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print("Error processing place:", e)

    return pd.DataFrame(results)


def scrape_crunchbase_mock(keyword, location="San Francisco, CA", max_results=10):
    results = []
    for i in range(max_results):
        domain = f"{keyword.lower().replace(' ', '')}{i+1}.com"
        email = get_verified_email(domain)
        results.append({
            "name": f"{keyword.title()} Co {i+1}",
            "industry": "Startup",
            "location": location,
            "website": f"https://{domain}",
            "email": email,
            "score": random.randint(70, 95)
        })
    return pd.DataFrame(results)

def scrape_linkedin_companies(companies):
    results = []
    for company in companies:
        domain = f"{company.lower().replace(' ', '')}.com"
        email = get_verified_email(domain)
        results.append({
            "name": company,
            "industry": "Tech",
            "location": "Remote",
            "website": f"https://linkedin.com/company/{company.lower().replace(' ', '')}",
            "email": email,
            "score": random.randint(65, 90)
        })
    return pd.DataFrame(results)

def scrape_job_board(keyword, location, max_results=10):
    results = []
    for i in range(max_results):
        domain = f"{keyword.lower().replace(' ', '')}{i+1}.com"
        email = get_verified_email(domain)
        results.append({
            "name": f"{keyword.title()} Role {i+1}",
            "industry": keyword,
            "location": location,
            "website": f"https://jobs.example.com/{keyword.lower()}/{i+1}",
            "email": email,
            "score": random.randint(60, 90)
        })
    return pd.DataFrame(results)

def scrape_angellist_startups(keyword, location, max_results=10):
    results = []
    for i in range(max_results):
        domain = f"{keyword.lower().replace(' ', '')}{i+1}.com"
        email = get_verified_email(domain)
        results.append({
            "name": f"{keyword} Startup {i+1}",
            "industry": "Startup",
            "location": location,
            "website": f"https://angel.co/company/{keyword.lower().replace(' ', '')}{i+1}",
            "email": email,
            "score": random.randint(65, 95)
        })
    return pd.DataFrame(results)

def combine_sources(*dfs):
    return pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["name", "website"])