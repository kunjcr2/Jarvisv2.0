from langchain.agents import initialize_agent, Tool, AgentType
import src.Tools as Tools

from src.llm import get_llm
import os

tool = Tools.ToolManager()

# creating the agent
def get_agent():
    agent = initialize_agent(
        tools=tool.get_tools(),
        llm=get_llm(api_key=os.getenv('OPENAI_API_KEY')),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent_name="pie-assistant",
        verbose=True,
        handle_parsing_errors=True
    )
    return agent