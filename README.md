# Financial Ananlysis Agent

Here is an example of a financial analysis agent built with Agno that uses Urai's code
execution capabilities.

## How does this work?

This agent is written to demonstrate the power of even small inexpensive models like gpt-4o-mini.
GPT 4o-mini only takes $0.15 per million tokens in input and $0.6 for million tokens in output.
Even such a weak model can do extremely well in code synthesis tasks in lanugages like Python and
Typescript.

Here we ask for an input like `Can you analyze SAP?` and it will think with 4o and generate code 
and produce results like downloading data from yahoo finance and producing tables and charts without
having to pay for really expensive models like o3 which cost $10 / M tokens input and $40 / M tokens
output. That is 66 times more expensive.

Sign up at [https://uraiai.com](https://uraiai.com) to get notified when we release.

## How to run this?

Install [uv](https://github.com/astral-sh/uv) and python and clone this repository.

Create a venv. Install dependencies and run the agent.

```
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
$ python agent.py
```

This should open up the URL for you open the agent up in Agno playground. 

## Aside about Agno

Agno is a very nice agent building library. Rather than imposing itself as the framework, Agno
provides a set of tools that you can compose to build agents. I like it very much.
