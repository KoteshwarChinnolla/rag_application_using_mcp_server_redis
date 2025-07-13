from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def mcp_server(message: str):
    client=MultiServerMCPClient(
        {
            "websearch":{
                "command":"python",
                "args":["src/first_aid_chatbot/webSearch.py"],
                "transport":"stdio",
            },
            "document_search": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]}
    )

    return math_response['messages'][-1].content

# asyncio.run(main())