# Custom AI Tools Agent

## Summary

A LangChain agent with three custom tools:

1. Calculator
2. Weather lookup
3. Database query simulator

The agent decides which tool is required based on the user's question and can use more than one tool for a single request.

## Architecture

User Question
      |
      v
LangChain Agent
      |
      +--> Calculator Tool
      |
      +--> Weather Lookup Tool
      |
      +--> Database Query Simulator
      |
      v
Tool Result
      |
      v
Final Answer

## Concepts Demonstrated

- LangChain Tools
- Custom tools
- `@tool` decorator
- Tool descriptions
- Agent tool selection
- ReAct-style reasoning/tool-use loop
- Agent execution
- Callbacks
- Debugging tool calls and outputs
- Multiple-tool workflow

## Important note about current LangChain

Current LangChain documentation uses `create_agent` as the main agent harness. Older tutorials commonly use `AgentExecutor` and `create_react_agent`.

This project uses `create_agent` so it matches the current LangChain API while still demonstrating the same core agent/tool loop you learned on Day 13.

## Examples 
```

## Demo 1 - Calculator

```text
You: What is 125 * 48?
```

Expected behavior:

```text
Agent
 -> calculator
 -> 6000
 -> final answer
```

## Demo 2 - Weather

```text
You: What is the weather in Bangalore?
```

Expected behavior:

```text
Agent
 -> weather_lookup
 -> 28°C, Partly Cloudy
 -> final answer
```

## Demo 3 - Database

```text
You: Find employee 102.
```

Expected behavior:

```text
Agent
 -> database_query
 -> Rahul, Data Engineer
 -> final answer
```

## Demo 4 - Multiple tools

Use this in your manager demonstration:

```text
You: What is the weather in Bangalore and convert its temperature to Fahrenheit?
```

Expected behavior:

```text
Agent
 -> weather_lookup
 -> 28°C
 -> calculator
 -> 82.4°F
 -> final answer
```

This is the strongest demonstration because the agent must use more than one custom tool.

## Debugging

The custom callback prints:

```text
TOOL START
TOOL INPUT
TOOL OUTPUT
TOOL ERROR
```

This lets you show the execution flow while the agent is running.


## Example questions

```text
What is 250 / 5?
What is 125 * 48?
What is the weather in Bangalore?
What is the temperature in Delhi?
Find employee 102.
Tell me about Rahul.
Which employees are in Engineering?
What is the weather in Bangalore and convert 28 C to Fahrenheit?
Find employee 103 and calculate 10% of their salary.
```
