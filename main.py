import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load environment variables securely from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Sales Agent Prototype - CAP 931",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Sales Assistant Prototype")
st.markdown("CAP 931 Capstone — Powered by LangChain, Groq (`llama-3.3-70b-versatile`), BeautifulSoup Web Scraping, & Streamlit")

# Sidebar Inputs for Sales Representative
st.sidebar.header("Prospect & Product Details")

product_name = st.sidebar.text_input("Product Name", "Enterprise Cloud Data Platform")
value_proposition = st.sidebar.text_input("Value Proposition", "Reduces data warehousing costs by 40% with automated scaling.")
company_url = st.sidebar.text_input("Target Company URL", "https://example-enterprise.com")
product_category = st.sidebar.text_input("Product Category", "Data Warehousing")
competitors = st.sidebar.text_input("Competitor Names / URLs", "Snowflake, Databricks")
target_customer = st.sidebar.text_input("Target Customer / Persona", "Chief Data Officer")

run_button = st.sidebar.button("Generate Account Insights One-Pager")

# Helper function to fetch and parse public web data for source grounding
def fetch_web_content(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=" ", strip=True)
            return text[:3500] # Return extracted textual evidence
    except Exception as e:
        return f"[Could not retrieve live text from {url}: {str(e)}]"
    return "[No content retrieved]"

# Define Agent Prompt Templates
sales_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert enterprise sales intake assistant. Analyze the prospect's request, core goals, budget, and requirements based on intake inputs."
    ),
    (
        "human",
        "Customer Request:\n{customer_request}\n\nTarget Company URL: {company_url}\nProduct Category: {product_category}\n\nIdentify and summarize:\n1. Customer Goal & Use Case\n2. Budget Constraints\n3. Important Requirements\n4. Missing Information"
    )
])

research_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a rigorous market research and competitor intelligence agent. You MUST base your analysis strictly on the provided scraped website evidence. Explicitly state when information cannot be verified from the sources."
    ),
    (
        "human",
        "Target Company URL: {company_url}\nScraped Company Evidence:\n{company_text}\n\nCompetitors: {competitors}\nCompetitor Evidence:\n{comp_evidence}\n\nProduct: {product_name} - {value_proposition}\n\nProvide insights on:\n1. Company Strategy (from sources)\n2. Key Leadership / Focus Areas\n3. Competitor Overlaps\n4. Recommended Sales Positioning"
    )
])

synthesis_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the lead sales strategist generating a concise one-page account insight summary. Include verified source URLs for reference."
    ),
    (
        "human",
        "Based on the intake analysis and source-grounded research, compile a polished summary:\n\nINTAKE:\n{sales_analysis}\n\nRESEARCH:\n{research_analysis}\n\nTarget Company URL: {company_url}\n\nFormat cleanly with headers: Executive Summary, Competitor Analysis, Key Leadership, Source Verification, and Tailored Pitch Strategy."
    )
])

# Main Execution Logic
if run_button:
    if not api_key:
        st.error("Error: GROQ_API_KEY not found. Please ensure your .env file is configured correctly.")
    else:
        with st.spinner("Scraping public web data and running multi-agent workflow... Please wait."):
            try:
                # 1. Scrape live data from target company URL
                scraped_company_text = fetch_web_content(company_url)

                # 2. Scrape competitor URLs or simulate domain lookups for competitor names
                comp_list = [c.strip() for c in competitors.split(",")]
                comp_evidence_dict = {}
                for comp in comp_list:
                    # Construct basic URL or scrape if URL provided
                    c_url = comp if comp.startswith("http") else f"https://www.{comp.lower().replace(' ', '')}.com"
                    comp_evidence_dict[comp] = fetch_web_content(c_url)

                comp_evidence_str = "\n".join([f"- {comp}: {text}" for comp, text in comp_evidence_dict.items()])

                # Initialize Groq LLM with standardized model: llama-3.3-70b-versatile
                model = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=0.1,
                    api_key=api_key
                )
                parser = StrOutputParser()

                # Build Chains
                sales_chain = sales_prompt | model | parser
                research_chain = research_prompt | model | parser
                synthesis_chain = synthesis_prompt | model | parser

                # Execute Agent 1: Sales Intake
                sales_analysis = sales_chain.invoke({
                    "customer_request": f"Pitch {product_name} to {target_customer} at {company_url}.",
                    "company_url": company_url,
                    "product_category": product_category
                })

                # Execute Agent 2: Research & Competitor Intelligence (Source-Grounded)
                research_analysis = research_chain.invoke({
                    "company_url": company_url,
                    "company_text": scraped_company_text,
                    "competitors": competitors,
                    "comp_evidence": comp_evidence_str,
                    "product_name": product_name,
                    "value_proposition": value_proposition
                })

                # Execute Agent 3: Final Synthesis (One-Pager)
                final_one_pager = synthesis_chain.invoke({
                    "sales_analysis": sales_analysis,
                    "research_analysis": research_analysis,
                    "company_url": company_url
                })

                # Display Results
                st.success("✨ Source-Grounded Account Insights One-Pager Generated Successfully!")
                st.markdown("---")
                st.markdown(final_one_pager)

                with st.expander("🔍 View Raw Agent Breakdown & Scraped Evidence"):
                    st.subheader("Scraped Company Web Evidence")
                    st.write(scraped_company_text[:1000] + "..." if len(scraped_company_text) > 1000 else scraped_company_text)
                    st.subheader("Sales Agent Intake Output")
                    st.write(sales_analysis)
                    st.subheader("Research Agent Output")
                    st.write(research_analysis)

            except Exception as e:
                st.error(f"An error occurred during agent execution: {e}")
else:
    st.info("👈 Enter your product and target account details in the sidebar and click **Generate Account Insights One-Pager** to start.")