from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import requests
from langchain.docstore.document import Document
from redis.commands.search.query import Query
import redis
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


mcp = FastMCP("documentSearch")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def vector_search(query: str):
    q = Query(
        f"*=>[KNN 3 @embedding $vec AS vector_distance]"
    ).return_field("content").dialect(2)

    query_params = {
        "vec": np.frombuffer(model.encode(query).astype(np.float32).tobytes(), dtype=np.float32)
    }
    
    res = r.ft("vector_idx").search(q, query_params=query_params)

    return res

@mcp.tool()
async def document_search(query: str) -> list[Document]:
    """Search for documents in Redis using a query.

    Args:
        query (str): The query string to search for.

    Returns:
        list[Document]: A list of documents containing the search results.
    """
    res = vector_search(query)
    if not res.docs:
        return []
    
    return [Document(page_content=doc.content, metadata={"score": doc.vector_distance}) for doc in res.docs]

if __name__ == "__main__":
    mcp.run(transport="streamable-http")