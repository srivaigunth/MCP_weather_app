from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

NWS_API_URL = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0) 
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature:dict) -> str:
    props = feature["properties"]
    return f"""
            Event :{ props.get("event",'unknown')}
            Area : {props.get("areaDesc",'unknown')}
            Severity : {props.get("severity","unknown")}
            Descrption : {props.get('description','no desc')}
            Instruction:{props.get('instruction','no specific instruction')}
            """

@mcp.tool()
async def get_alerts(state : str) -> str:
    """Get weather alerts for a US State.

    Args:
        state : Two-letter US state code (e.g. CA , NY)
    """

    url = f"{NWS_API_URL}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found"
    if not data["features"]:
        return "No active alerts for this state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n - - - \n".join(alerts)

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"
