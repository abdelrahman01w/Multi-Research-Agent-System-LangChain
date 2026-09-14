from langchain.agents import create_agent # rather than create_react_agent and  agent_executor
from langchain_groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import strOutputParser
from src.tools.tools import web_serach, scrape_url
from dotenv import load_dotenv

load_dotenv()

# model initialization
llm = Groq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
)

# 1st agent ==> Search Agent
def build_search_agent():
    return create_agent(
        llm=llm,
        tools=[web_serach],
    )

# 2nd agent ==> Reader Agent "scrapper"

def build_reader_agent():
    return create_agent(
        llm=llm,
        tools=[scrape_url],
    )

# writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system",  "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain= writer_prompt | llm | strOutputParser()

# critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system",  "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain= critic_prompt | llm | strOutputParser()