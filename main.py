import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Hardcoded API key for seamless execution of your CAP 931 project
api_key = "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"

# Streamlit Page Configuration
st.set_page_config(
    page_title="Sales Agent Prototype - CAP 931",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Sales Assistant Prototype")
st.markdown("CAP 931 Capstone — Powered by LangChain, Groq, & Streamlit")

# Sidebar Inputs for Sales Representative
st.sidebar.header("Prospect & Product Details")

product_name = st.sidebar.text_input("Product Name", "Enterprise Cloud Data Platform")
value_proposition = st.sidebar.text_input("Value Proposition", "Reduces data warehousing costs by 40% with automated scaling.")
company_url = st.sidebar.text_input("Target Company URL", "https://example-enterprise.com")
product_category = st.sidebar.text_input("Product Category", "Data Warehousing")
competitors = st.sidebar.text_input("Competitor URLs / Names", "Snowflake, Databricks")
target_customer = st.sidebar.text_input("Target Customer / Persona", "Chief Data Officer")

run_button = st.sidebar.button("Generate Account Insights One-Pager")

# Define Agent Prompt Templates
sales_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert enterprise sales intake assistant. Analyze the prospect's request, core goals, budget, and requirements. Do not make product recommendations yet."
    ),
    (
        "human",
        "Customer Request:\n{customer_request}\n\nTarget Company URL: {company_url}\nProduct Category: {product_category}\n\nIdentify and summarize:\n1. Customer Goal & Use Case\n2. Budget Constraints\n3. Important Requirements\n4. Missing Information"
    )
])

research_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior market research and competitor intelligence agent. Analyze company strategy, industry footprint, and competitor overlaps."
    ),
    (
        "human",
        "Company URL: {company_url}\nCompetitors: {competitors}\nProduct: {product_name} - {value_proposition}\n\nProvide insights on:\n1. Company Strategy\n2. Key Leadership / Focus Areas\n3. Competitor Overlaps\n4. Recommended Sales Positioning"
    )
])

synthesis_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the lead sales strategist generating a concise one-page account insight summary."
    ),
    (
        "human",
        "Based on the intake analysis and research, compile a polished summary:\n\nINTAKE:\n{sales_analysis}\n\nRESEARCH:\n{research_analysis}\n\nFormat cleanly with headers: Executive Summary, Competitor Analysis, Key Leadership, and Tailored Pitch Strategy."
    )
])

# Main Execution Logic
if run_button:
    with st.spinner("Running multi-agent workflow... Please wait."):
        try:
            # Initialize Groq LLM with active production model
            model = ChatGroq(
                model="openai/gpt-oss-120b",
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

            # Execute Agent 2: Research & Competitor Intelligence
            research_analysis = research_chain.invoke({
                "company_url": company_url,
                "competitors": competitors,
                "product_name": product_name,
                "value_proposition": value_proposition
            })

            # Execute Agent 3: Final Synthesis (One-Pager)
            final_one_pager = synthesis_chain.invoke({
                "sales_analysis": sales_analysis,
                "research_analysis": research_analysis
            })

            # Display Results
            st.success("✨ Account Insights One-Pager Generated Successfully!")
            st.markdown("---")
            st.markdown(final_one_pager)

            with st.expander("🔍 View Raw Agent Breakdown"):
                st.subheader("Sales Agent Intake Output")
                st.write(sales_analysis)
                st.subheader("Research Agent Output")
                st.write(research_analysis)

        except Exception as e:
            st.error(f"An error occurred during agent execution: {e}")
else:
    st.info("👈 Enter your product and target account details in the sidebar and click **Generate Account Insights One-Pager** to start.")