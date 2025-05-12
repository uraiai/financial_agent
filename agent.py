from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.thinking import ThinkingTools
from agno.tools.tavily import TavilyTools
from agno.playground import Playground, serve_playground_app

from tools.code_interpreter import ThiriTools

agent = Agent(
        name="Financial Analysis Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description='Help you with your financial analysis',
        instructions='''
        Given a company name, search for the competitors and their stock symbols. 
        Write python code to use yfinance and matplotlib to generate stock graph
        data for the past year as `output.png`. 

        Prepare a report based on the top 5 news articles about the company and 
        include the stock chart.

        IMPORTANT: Ensure that you think before you write code. 
        ''',
        tools=[
            ThinkingTools(add_instructions=True),
            TavilyTools(),
            # Use thiri for code execution.
            ThiriTools()
        ],
        markdown=True,
        show_tool_calls=True,
        debug_mode=True

)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("agent:app", reload=True)
