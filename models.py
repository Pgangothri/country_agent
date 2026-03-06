from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str


class AgentResponse(BaseModel):
    answer: str
    country: Optional[str]
    fields: List[str]
    confidence: float
    source: str = "REST Countries API"
