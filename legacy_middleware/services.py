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


def fetch_legacy_token():
    """
    Fetch a new OAuth token from the legacy API.

    Returns:
        tuple: (token, expires_at)
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/api/v1/oauth"
    payload = {
        "user": settings.LEGACY_API_USER,
        "secret": settings.LEGACY_API_SECRET,
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()

    token = data.get("token")
    expires_in = data.get("expires_in", 2592000)

    # Calculate expiry with buffer (e.g. 1 day as per docs)
    from django.utils import timezone
    from datetime import timedelta

    expires_at = timezone.now() + timedelta(seconds=expires_in - 86400)

    return token, expires_at


def fetch_quote(token, payload):
    """
    Fetch a quote from the legacy API using the provided token.

    Args:
        token (str): The OAuth token.
        payload (dict): The quote request payload.

    Returns:
        requests.Response: The response from the legacy API.
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/api/v1/quote"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Inject default rate_group if missing
    if "rate_group" not in payload and settings.LEGACY_API_RATE_GROUP:
        payload["rate_group"] = settings.LEGACY_API_RATE_GROUP

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    return response


def fetch_reservation_create(token, payload):
    """
    Create a new reservation in the legacy API.

    Args:
        token (str): The OAuth token.
        payload (dict): The reservation creation payload.

    Returns:
        requests.Response: The response from the legacy API.
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/api/v1/create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Inject default site_id if missing
    if "site_id" not in payload and settings.LEGACY_API_SITE_ID:
        payload["site_id"] = int(settings.LEGACY_API_SITE_ID)

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    return response
