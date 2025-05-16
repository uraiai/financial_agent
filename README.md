# Financial Analysis Agent

This repository demonstrates a financial analysis agent built with [Agno](https://github.com/your-agno-link), showcasing Urai’s powerful code execution capabilities.

## What This Demonstrates

This agent highlights how Urai’s code execution engine enables even lightweight language models like **GPT-4o-mini** to perform advanced financial analysis through code generation and execution.

For example, given a prompt such as `Can you analyze SAP?`, the agent dynamically generates Python code to retrieve financial data (e.g., from Yahoo Finance), then presents structured outputs like tables and charts. This is all achieved without relying on expensive models.

Urai simplifies complex AI agent workflows by allowing language models to generate and run code in a secure, sandboxed environment. This decouples agent logic from model sophistication, enabling powerful outcomes at lower cost and higher speed.

> 💡 Want early access? Sign up at [https://uraiai.com](https://uraiai.com) to get notified when we launch.

## Running the Agent

### Prerequisites

- [uv](https://github.com/astral-sh/uv)
- Python 3.9+

### Instructions

```bash
git clone https://github.com/uraiai/financial_agent.git
cd financial_agent
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python agent.py
```

This should display the Agno playground URL. 

> Note: You will need the **API Key** for code execution. Sign up at [https://uraiai.com](https://uraiai.com) to get the API key.

## About Agno

Agno is a modular agent building library. Rather than imposing itself as the framework, Agno
provides a set of tools that you can compose to build agents. This repo shows how 
Urai integrates seamlessly with Agno, enabling dynamic, code-driven agents that can take real actions.
