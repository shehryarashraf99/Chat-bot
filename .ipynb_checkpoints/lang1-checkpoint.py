from rag_agent import lookup_policy
from tavily_agent import web_search_tool
from sql_agent import nl2sql_tool
from typing import Annotated
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
os.environ['OPENAI_API_KEY'] = "your_open_ai_key"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [web_search_tool, lookup_policy, nl2sql_tool]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
     messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[web_search_tool, lookup_policy, nl2sql_tool])
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()


config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
