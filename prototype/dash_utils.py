import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# API HELPER FUNCTIONS (Dates and API handeling)
def normalize_date_for_api(value):
    """Ensure the API receives plain YYYY-MM-DD dates without a time component."""
    if value is None:
        return datetime.now().date().isoformat()
    if hasattr(value, "isoformat"):
        if isinstance(value, datetime):
            return value.date().isoformat()
        return str(value)
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return datetime.now().date().isoformat()
        if "T" in raw or " " in raw:
            raw = raw.split("T")[0].split(" ")[0]
        return raw
    return str(value)


def format_date_series(series: pd.Series, include_time: bool = False) -> pd.Series:
    """Safely normalizes mixed date strings to a consistent display format."""
    if series.empty:
        return series

    parsed = pd.to_datetime(series, errors="coerce", format="mixed")
    if include_time:
        return parsed.dt.strftime("%Y-%m-%d %H:%M").fillna("")
    return parsed.dt.strftime("%Y-%m-%d").fillna("")


def make_request(method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict = None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        response.raise_for_status()
        return response.json() if response.text else None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Make sure the FastAPI server is running on http://127.0.0.1:8000")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API Error: {e.response.json().get('detail', str(e))}")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None