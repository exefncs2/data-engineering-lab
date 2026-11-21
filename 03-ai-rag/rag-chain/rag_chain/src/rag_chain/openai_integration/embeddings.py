"""OpenAI Embeddings 封裝模組（相容 OpenAI Python SDK v1+）。"""

from typing import Sequence

from openai import OpenAI


def get_embeddings(texts: Sequence[str], model: str = "text-embedding-3-small"):
    """呼叫 OpenAI Embeddings API 並回傳向量資料清單。"""
    client = OpenAI()
    response = client.embeddings.create(model=model, input=list(texts))
    return response.data
