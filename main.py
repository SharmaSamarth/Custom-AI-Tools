import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama

from langchain.agents import (
    create_react_agent,
    AgentExecutor
)

from langchain_core.prompts import PromptTemplate

from tools import tools
from database import create_database


# LOAD ENVIRONMENT VARIABLES

load_dotenv()


# CREATE SQLITE DATABASE

create_database()


# OLLAMA MODEL

MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3:8b"
)

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)


# REACT PROMPT

prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

You have access to the following tools:

{tools}

Use the following format:

Question: the user's question

Thought: think about what tool is needed

Action: the tool to use, exactly one of [{tool_names}]

Action Input: the input to the tool

Observation: the result of the tool

...

Thought: I now know the final answer

Final Answer: the final response to the user

Important rules:

1. Always use the calculator tool for calculations.
2. Always use the weather_lookup tool for weather questions.
3. Always use the database_query tool for employee/database questions.
4. Only use SELECT queries for the database.
5. You may use multiple tools when necessary.
6. Do not invent information.

Question: {input}

{agent_scratchpad}
""")


# CREATE REACT AGENT

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# CREATE AGENT EXECUTOR

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,

    # This is useful for your Day 13 debugging demonstration.
    verbose=True,

    # Prevent the agent from running forever.
    max_iterations=10,

    # Return a useful response if iteration limit is reached.
    handle_parsing_errors=True
)


# RUN APPLICATION

def main():

    print("\n======================================")
    print("   DAY 13 LANGCHAIN TOOLS + AGENT")
    print("======================================")

    print(f"Using Ollama model: {MODEL_NAME}")

    print("\nAvailable tools:")
    print("1. Calculator")
    print("2. Weather Lookup")
    print("3. Database Query")

    print("\nType 'exit' to stop.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:

            response = agent_executor.invoke({
                "input": user_input
            })

            print("\nAgent:", response["output"])
            print("\n" + "-" * 60)

        except Exception as e:

            print("\nApplication Error:")
            print(e)

            print("-" * 60)


if __name__ == "__main__":
    main()