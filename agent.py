from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.tools.thinking import ThinkingTools
from agno.tools.tavily import TavilyTools
from agno.playground import Playground, serve_playground_app

from tools.code_interpreter import ThiriTools

agent = Agent(
        name="Financial Analysis Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        # model=Gemini(id="gemini-2.5-pro-preview-"),
        description='Help you with your financial analysis',
        instructions=dedent('''
        You are an expert python programmer.

        A user would ask a question about the company. In addition to answering 
        the question, do the following.

        1) Given a company name, search for the competitors and their stock symbols.
        2) Write error free python code for analysis

        <CODE_EXECUTION>
        Write python code to use yfinance and matplotlib to generate stock graph
        data for the past year as `output.png` in the current directory.  Remember
        that yfinance has changed its API to return only `Close` instead of `Adj Close`. 
        So DO NOT use it.

        Ensure that you print the statistics out to the console as a table. Use
        pandas to output statistics as a CSV string to STDOUT. DO NOT write the CSV
        file to the disk.

        Only ONE IMAGE should be generated containing all the stock symbols
        The output file SHOULD be called `output.png`
        </CODE_EXECUTION>

        3) Summarize the report to the user.


        IMPORTANT:
        If running code or downloading image fails, regenerate the code and attempt to download the file again.
        You should ALWAYS write code.
        You should THINK before you WRITE CODE.
        '''),
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
