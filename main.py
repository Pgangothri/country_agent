from fastapi import FastAPI, HTTPException
import logging
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from models import QueryRequest, AgentResponse
from state import AgentState
from helpers import intent_router, api_caller, synthesize_answer, handle_error

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Country Information AI Agent", version="1.0.0")


# ----------------------------
# Router
# ----------------------------
def should_continue(state: AgentState):
    if state.get("country_data"):
        return "synthesize"

    return "error"


# ----------------------------
# Build LangGraph Workflow
# ----------------------------
workflow = StateGraph(AgentState)

workflow.add_node("intent", intent_router)
workflow.add_node("api", api_caller)
workflow.add_node("synthesize", synthesize_answer)
workflow.add_node("error", handle_error)

workflow.set_entry_point("intent")

workflow.add_edge("intent", "api")

workflow.add_conditional_edges(
    "api",
    should_continue,
    {
        "synthesize": "synthesize",
        "error": "error",
    },
)

workflow.add_edge("synthesize", END)
workflow.add_edge("error", END)

app_graph = workflow.compile()


# ----------------------------
# FastAPI Endpoint
# ----------------------------
@app.post("/ask", response_model=AgentResponse)
async def ask_country(request: QueryRequest):
    try:
        initial_state = {
            "messages": [HumanMessage(content=request.query)],
            "country": "",
            "fields": [],
            "country_data": {},
            "response": "",
            "confidence": 0.0,
            "error": None,
        }

        result = await app_graph.ainvoke(initial_state)

        return AgentResponse(
            answer=result["response"],
            country=result.get("country"),
            fields=result.get("fields", []),
            confidence=result.get("confidence", 0.5),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "country-agent"}


@app.get("/")
async def root():
    return {
        "message": "Country Information AI Agent",
        "examples": [
            "What is the population of Germany?",
            "What currency does Japan use?",
            "Capital and population of Brazil?",
            "Languages spoken in India",
        ],
        "endpoint": "/ask",
    }


# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
