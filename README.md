# 🧠 iLLMs – ReAct Agents with Ease

**iLLMs** is a minimal Python framework for building **ReAct-style** LLM agents with tool support.
It combines a structured reasoning loop (Thought → Action → Observation → Answer) with simple abstractions for tools and agents.

---

## ✨ Features

* 🧠 ReAct loop: Thought → Action → Observation → Answer
* 🧩 Define tools via a simple decorator
* 🛠 Easily plug tools into your agent
* 🧪 Clean example in Jupyter Notebook

---

## 🏗️ Structure

```
iLLMs/
├── Agent.py         # Core agent logic (ReAct loop)
├── Tool.py          # Tool definition and decorator
├── Examples/
│   └── agent.ipynb  # Notebook showing usage
└── README.md
```

---

## 🚀 Quickstart

### 1. Install dependencies

```bash
pip install groq
```

### 2. Define tools

```python
from Tool import tool

@tool
def greet(name: str) -> str:
    """Returns a greeting for the given name."""
    return f"Hello, {name}!"
```

### 3. Create a ReAct agent

```python
from Agent import Agent
from groq import Groq

client = Groq(api_key="your_api_key")

agent = Agent(
    client=client,
    name="ReActBot",
    role="A helpful assistant that reasons and acts using tools.",
    tools=[greet],
    system_message_file="SYSTEM_PROMPT.txt"
)
```

### 4. Run the agent

```python
response = agent("Say hello to Sam.")
print(response)
```

---

## 🔁 ReAct Loop Overview

The agent internally loops through:

* **Thought**: Think about what to do next
* **Action**: Pick and invoke a tool
* **Observation**: Receive and reflect on the result
* **Answer**: Conclude when ready

Structured JSON responses control the loop:

```json
{
  "state": "Action",
  "payload": "greet",
  "args": ["Sam"]
}
```

---

## 📓 Example Notebook

Check `Examples/agent.ipynb` for a full demonstration of defining tools and running your agent.

---

## 📄 License

MIT License © 2025

## Future Work 

* Add multi_agentic workflows
* Support for different LLM providers


