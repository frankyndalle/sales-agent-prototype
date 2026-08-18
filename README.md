# CAP 931: Capstone - Multi-Agent Sales Assistant Prototype

## Overview
The Multi-Agent Sales Assistant Prototype is a web application designed to help enterprise sales representatives rapidly gather account insights, analyze competitor overlaps, evaluate target company strategy, and synthesize tailor-made pitch strategies. Powered by Streamlit, LangChain, and high-performance Groq LLM models, this system chains specialized autonomous agents to deliver a structured executive one-pager in seconds.

## Architecture & Workflow
The application implements a multi-agent prompt chaining architecture:
1. Sales Intake Agent: Analyzes the target company, product category, customer persona, and core request to define user goals, use cases, and missing criteria.
2. Research & Intelligence Agent: Evaluates market landscape, competitor overlaps (e.g., Snowflake, Databricks), and strategic positioning.
3. Synthesis Strategist Agent: Merges the intake and research outputs into a polished executive account insight summary with clean headers.

## Technical Stack & Model Selection
* Frontend: Streamlit (Interactive, user-friendly sidebar for dynamic inputs).
* Orchestration: LangChain (ChatPromptTemplate, StrOutputParser).
* LLM Engine: Groq API running openai/gpt-oss-120b.
* Justification: Selected for its lightning-fast token generation speed, high-tier reasoning capabilities comparable to proprietary frontier models, and cost efficiency for real-time multi-agent workflows.

## Installation & Local Execution
1. Clone the repository:
   git clone https://github.com/frankyndalle/sales-agent-prototype.git
   cd sales-agent-prototype

2. Install dependencies:
   pip install streamlit langchain langchain-groq python-dotenv

3. Run the application:
   streamlit run main.py

## Project Structure
* main.py — Core application logic, Streamlit UI components, and multi-agent chain definitions.
* .gitignore — Excludes virtual environments and sensitive environment files.
* README.md — Comprehensive project documentation and user guide.

## Optional Enhancements & Production Deployment

### 1. Automated Alert System (Proposed)
To scale this prototype into an active prospecting tool, an automated email alert system can be integrated using Python's smtplib or SendGrid API. This system would periodically scrape target company press releases or job postings for keyword triggers and automatically email sales reps when a strategic shift occurs.

### 2. Production Deployment Plan
* Hosting: Deployable on Streamlit Community Cloud or containerized via Docker and hosted on AWS ECS / Google Cloud Run.
* Security: Use environment secret managers (AWS Secrets Manager or Streamlit Secrets) to securely handle API keys rather than local configuration.
* Scalability: Implement asynchronous chain execution using asyncio to handle multiple concurrent sales representative requests without latency bottlenecks.
