import requests
from django.conf import settings


def fetch_legacy_autocomplete(keyword: str) -> requests.Response:
    """
    Fetch autocomplete results from the legacy API.

    Args:
        keyword (str): The search term.

    Returns:
        requests.Response: The response from the legacy API.
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/api/v1/autocomplete-affiliates"
    headers = {
        "Content-Type": "application/json",
        "app-key": settings.LEGACY_API_KEY,
    }
    payload = {"keyword": keyword}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response
    except requests.RequestException as e:
        # re-raise to be handled by the view
        raise e
