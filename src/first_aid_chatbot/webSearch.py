from typing import Any
from mcp.server.fastmcp import FastMCP
import requests
from langchain.docstore.document import Document
import redis
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"]= os.getenv("GROQ_API_KEY")

mcp = FastMCP("websearch")

def search_serper(query):
    headers = {"X-API-KEY": os.getenv("SERPER_API_KEY")}
    payload = {"q": query}
    res = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
    results = res.json().get("organic", [])
    
    return [Document(page_content=item["snippet"], metadata={"source": item["link"]}) for item in results[:5]]

@mcp.tool()
async def serper_search(q: str) -> list[Document]:
    """Search using Serper API."""
    return search_serper(q)

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run(transport="stdio"))
