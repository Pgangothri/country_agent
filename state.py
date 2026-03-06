from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from typing import List, Dict, Any, Optional


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    country: str
    fields: List[str]
    country_data: Dict[str, Any]
    response: str
    confidence: float
    error: Optional[str]
