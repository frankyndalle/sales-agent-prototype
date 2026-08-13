import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="Interactive Multi-Agent Chat Test", layout="wide"
)

st.title("🤖 Interactive Multi-Agent Sales Chat (Test Sandbox)")
st.markdown(
    "This is an isolated test file to experiment with collaborative multi-agent"
    " conversation."
)

# Initialize Groq Model
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
parser = StrOutputParser()

# Sidebar configuration for context
st.sidebar.header("Test Configuration")
product_name = st.sidebar.text_input(
    "Product Name", "Enterprise Cloud Data Platform"
)
competitors = st.sidebar.text_input("Competitors", "Snowflake, Databricks")
target_persona = st.sidebar.text_input(
    "Target Customer", "Chief Data Officer"
)

# Chat History State
if "test_messages" not in st.session_state:
  st.session_state.test_messages = []

# Display prior chat messages
for message in st.session_state.test_messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Chat Input
if user_prompt := st.chat_input(
    "Ask the multi-agent team a question (e.g., How do we pitch against"
    " Snowflake?)"
):
  st.session_state.test_messages.append(
      {"role": "user", "content": user_prompt}
  )
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    with st.spinner("Multi-agent team is collaborating..."):
      chat_prompt = ChatPromptTemplate.from_messages([
          (
              "system",
              (
                  "You are a collaborative Multi-Agent Sales Operations Team"
                  f" helping a representative pitch {product_name} to a"
                  f" {target_persona}, competing against {competitors}.\n\nYour"
                  " team consists of:\n1. Sales Intake Specialist (analyzes"
                  " customer goals)\n2. Market Research Specialist (analyzes"
                  " competitor overlaps and positioning)\n3. Strategy Synthesis"
                  " Specialist (outlines pitch tactics and recommendations)\n\nCoordinate"
                  " across these specialized perspectives to provide a"
                  " comprehensive, structured multi-agent response."
              ),
          ),
          ("human", "{user_input}"),
      ])
      chat_chain = chat_prompt | model | parser
      response = chat_chain.invoke({"user_input": user_prompt})
      st.markdown(response)
      st.session_state.test_messages.append(
          {"role": "assistant", "content": response}
      )