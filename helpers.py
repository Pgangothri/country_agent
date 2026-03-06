from state import AgentState
import re
import logging
from langchain_core.messages import HumanMessage
import httpx

logging.basicConfig(level=logging.INFO)

COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "america": "United States",
    "uk": "United Kingdom",
    "britain": "United Kingdom",
    "uae": "United Arab Emirates",
}


def intent_router(state: AgentState) -> AgentState:
    query_original = state["messages"][-1].content
    query = query_original.lower()

    # Country patterns
    country_patterns = {
        r"germany|deutschland": "Germany",
        r"japan|nippon": "Japan",
        r"brazil|brasil": "Brazil",
        r"india": "India",
        r"china": "China",
        r"canada": "Canada",
        r"australia": "Australia",
        r"france": "France",
    }

    # Field patterns
    field_patterns = {
        r"population|people|citizens": "population",
        r"capital|main city": "capital",
        r"currency|money|dollar|yen|rupee": "currencies",
        r"language|languages|spoken": "languages",
        r"area|size|square": "area",
        r"continent|region": "region",
        r"name": "name",
    }

    # Detect country
    country = None

    for pattern, name in country_patterns.items():
        if re.search(pattern, query):
            country = name
            break

    # alias detection
    if not country:
        for alias, name in COUNTRY_ALIASES.items():
            if alias in query:
                country = name
                break

    # fallback detection
    if not country:
        words = re.findall(r"\b[A-Z][a-z]{1,14}\b", query_original)
        country = words[0] if words else "unknown"

    # detect fields
    fields = []
    for pattern, field in field_patterns.items():
        if re.search(pattern, query):
            fields.append(field)

    if not fields:
        fields = ["capital", "population"]

    logging.info(f"Detected country: {country}")
    logging.info(f"Detected fields: {fields}")

    return {
        **state,
        "country": country,
        "fields": fields,
        "messages": state["messages"]
        + [HumanMessage(content=f"Detected country={country}, fields={fields}")],
    }


# ----------------------------
# 2. API CALLER
# ----------------------------
async def api_caller(state: AgentState) -> AgentState:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://restcountries.com/v3.1/name/{state['country']}"
            response = await client.get(url)

        if response.status_code != 200:
            return {**state, "error": f"No data found for {state['country']}"}

        results = response.json()

        if not results:
            return {**state, "error": f"No country data found for {state['country']}"}

        # choose best match
        country_data = None
        for item in results:
            if item["name"]["common"].lower() == state["country"].lower():
                country_data = item
                break

        country_data = country_data or results[0]

        logging.info(f"Fetched API data for {state['country']}")

        return {
            **state,
            "country_data": country_data,
            "messages": state["messages"]
            + [HumanMessage(content=f"API data fetched for {state['country']}")],
        }

    except httpx.TimeoutException:
        return {**state, "error": "API request timed out"}

    except Exception as e:
        return {**state, "error": f"API error: {str(e)}"}


# ----------------------------
# 3. ANSWER SYNTHESIS
# ----------------------------
def synthesize_answer(state: AgentState) -> AgentState:
    if not state.get("country_data"):
        return {
            **state,
            "response": "Sorry, no country data available.",
            "confidence": 0.2,
        }

    data = state["country_data"]
    fields = state["fields"]

    country_name = data.get("name", {}).get("common", state["country"])

    answers = []

    for field in fields:
        if field == "name":
            answers.append(f"The country is {country_name}.")

        elif field == "population":
            pop = data.get("population")
            if pop:
                answers.append(f"{country_name}'s population is {pop:,}.")

        elif field == "capital":
            capital = data.get("capital", ["N/A"])[0]
            answers.append(f"The capital of {country_name} is {capital}.")

        elif field == "currencies":
            currencies = data.get("currencies", {})
            if currencies:
                code = list(currencies.keys())[0]
                name = currencies[code]["name"]
                answers.append(f"{country_name} uses {name} ({code}).")

        elif field == "languages":
            langs = list(data.get("languages", {}).values())
            lang_str = ", ".join(langs[:3])
            answers.append(f"Main languages in {country_name}: {lang_str}.")

        elif field == "area":
            area = data.get("area")
            if area:
                answers.append(f"{country_name}'s area is {area:,.0f} sq km.")

        elif field == "region":
            region = data.get("region")
            if region:
                answers.append(f"{country_name} is in the {region} region.")

    if not answers:
        answers.append("Requested information not available.")

    response = " ".join(answers)

    return {
        **state,
        "response": response,
        "confidence": 0.95,
    }


# ----------------------------
# 4. ERROR HANDLER
# ----------------------------
def handle_error(state: AgentState) -> AgentState:
    error_msg = state.get("error", "Unknown error occurred")

    logging.error(error_msg)

    return {
        **state,
        "response": f"I apologize, but {error_msg}. Please try another country.",
        "confidence": 0.1,
    }
