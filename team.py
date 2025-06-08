from textwrap import dedent
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude 
from agno.models.google import Gemini
from agno.tools.thinking import ThinkingTools
from agno.tools.tavily import TavilyTools
from agno.playground import Playground, serve_playground_app
from agno.team import Team

from tools.code_interpreter import ThiriTools
current_date = datetime.now().strftime("%Y-%m-%d")

# Research Agent - Focuses on finding company and competitor information
research_agent = Agent(
    name="Financial Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    description='Research companies and their competitors',
    instructions=dedent(f'''
    You are an expert financial researcher.

    today's date is {current_date}.
    
    When a user asks about a company:
    
    1) Search for the company and its competitors
    2) Find their stock symbols
    3) Provide a brief overview of the company and its market position
    
    Be thorough in your research but concise in your reporting.
    '''),
    tools=[
        ThinkingTools(add_instructions=True),
        TavilyTools(),
    ],
    markdown=True,
    show_tool_calls=True,
)

# Code Writing Agent - Focuses on writing and executing Python code
code_agent = Agent(
    name="Code Agent",
    # model=Claude(id="claude-3-7-sonnet"),
    model=OpenAIChat(id="gpt-4o"),
    description='Write and execute Python code for financial analysis',
    instructions=dedent('''
    You are an expert python programmer.
    
    today's date is {current_date}.


    When asked to analyze stocks:
    
    1) Write error-free python code for financial analysis
    
    Write python code to use yfinance and matplotlib to generate stock graph
    data for the past year as `output.png` in the current directory. Remember
    that yfinance has changed its API to return only `Close` instead of `Adj Close`. 
    So DO NOT use it.
    
    Ensure that you print the statistics out to the console as a table. Use
    pandas to output statistics as a CSV string to STDOUT. DO NOT write the CSV
    file to the disk.
    
    Only ONE IMAGE should be generated containing all the stock symbols
    The output file MUST be called `output.png`
    
    IMPORTANT:
    If running code or downloading image fails, regenerate the code and attempt to download the file again.
    You should ALWAYS write code.
    You should THINK before you WRITE CODE.
    '''),
    tools=[
        ThinkingTools(add_instructions=True),
        ThiriTools()
    ],
    markdown=True,
    show_tool_calls=True,
)

# Summary Agent - Focuses on summarizing findings
summary_agent = Agent(
    name="Financial Summary Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    description='Summarize financial analysis findings',
    instructions=dedent('''
    You are an expert financial analyst.
    
    today's date is {current_date}.

    Your job is to:
    
    1) Take research information and code analysis results
    2) Create a clear, concise summary for the user
    3) Highlight key insights and trends
    4) Explain the implications in plain language
    
    Make complex financial information accessible to users of all knowledge levels.
    '''),
    tools=[
        ThinkingTools(add_instructions=True),
    ],
    markdown=True,
    show_tool_calls=True,
)

# Create a team with the route mode
financial_team = Team(
    name="Financial Analysis Team",
    mode="coordinate",
    model=OpenAIChat(id="gpt-4o-mini"),
    members=[
        research_agent,
        code_agent,
        summary_agent,
    ],
    instructions=dedent('''
        You are the leader of a financial analysis team. 
        Your job is to create a comprehensive financial analysis of the company and its competitors
        including stock price history. Use the coder on your team to get the stock price data and relevant metrics.
        including a stock chart analysis. 

        You have a very efficient coder on your team who can use python, matplotlib and libraries for financial data
        to get accurate results. Do not just rely on search results for this data.

        today's date is {current_date}.

        Coordinate with the team members below:
        - Research Agent: For questions about companies, competitors, or market information
        - Code Agent: For requests requiring code execution, data analysis, or visualization
        - Financial Summary Agent: For requests to summarize or explain financial information in simple terms

        ALWAYS leverage the code writing agent to do detailed analysis.
        '''),
    enable_team_history=True,
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)

app = Playground(teams=[financial_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("team:app", reload=True)
