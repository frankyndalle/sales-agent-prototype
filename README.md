# 🤖 Multi-Agent Sales Assistant Prototype (CAP 931 Capstone)

An enterprise-grade, multi-agent sales assistant prototype designed to streamline account research, competitor intelligence, and pitch strategy generation for sales professionals. Powered by **LangChain**, **Groq (`openai/gpt-oss-120b`)**, **BeautifulSoup Web Scraping**, and **Streamlit**.

---

## 🚀 Key Features

1. **Three-Agent Prompt Chaining Architecture:**
   - **Sales Intake Agent:** Analyzes prospect requests, core goals, budget constraints, and requirements.
   - **Research & Competitor Intelligence Agent:** Performs live web scraping and strictly grounds its analysis in real retrieved web evidence.
   - **Strategy Synthesis Agent:** Combines intake and research data to synthesize a polished account insights one-pager.
2. **Live Source-Grounded Web Scraping:** Uses `BeautifulSoup` and `requests` to pull text content directly from target company and competitor URLs to prevent LLM hallucinations.
3. **Secure Configuration:** Fully integrated with `.env` and `python-dotenv` for secure environment variable management (`GROQ_API_KEY`).
4. **Modern Dependency Management:** Built and managed using `uv`.

---

## 🛠️ Project Structure

- `main.py` — The core Streamlit application containing the multi-agent workflow and BeautifulSoup scraper.
- `test_chat.py` — Interactive multi-agent test sandbox.
- `pyproject.toml` — Project configuration and dependencies.
- `.env` — Secure local environment file for your Groq API key (excluded from version control via `.gitignore`).

---

## ⚙️ Installation & Execution Workflow

Ensure you have **Python 3.10+** and **`uv`** installed on your system.

### 1. Configure Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here