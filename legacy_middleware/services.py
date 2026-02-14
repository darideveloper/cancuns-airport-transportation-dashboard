import requests
from django.conf import settings


def _post_to_legacy(
    endpoint: str,
    payload: dict,
    token: str = None,
    headers: dict = None,
    timeout: int = 10,
) -> requests.Response:
    """
    Internal helper to send a POST request to the legacy API.
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    final_headers = {
        "Content-Type": "application/json",
    }

    if token:
        final_headers["Authorization"] = f"Bearer {token}"

    if headers:
        final_headers.update(headers)

    return requests.post(url, json=payload, headers=final_headers, timeout=timeout)


def fetch_legacy_autocomplete(keyword: str) -> requests.Response:
    """
    Fetch autocomplete results from the legacy API.

    Args:
        keyword (str): The search term.

    Returns:
        requests.Response: The response from the legacy API.
    """
    headers = {"app-key": settings.LEGACY_API_KEY}
    payload = {"keyword": keyword}

    return _post_to_legacy("api/v1/autocomplete-affiliates", payload, headers=headers)


def fetch_legacy_token():
    """
    Fetch a new OAuth token from the legacy API.

    Returns:
        tuple: (token, expires_at)
    """
    payload = {
        "user": settings.LEGACY_API_USER,
        "secret": settings.LEGACY_API_SECRET,
    }

    response = _post_to_legacy("api/v1/oauth", payload)
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
    # Inject default rate_group if missing
    if "rate_group" not in payload and settings.LEGACY_API_RATE_GROUP:
        payload["rate_group"] = settings.LEGACY_API_RATE_GROUP

    return _post_to_legacy("api/v1/quote", payload, token=token)


def fetch_reservation_create(token, payload):
    """
    Create a new reservation in the legacy API.

    Args:
        token (str): The OAuth token.
        payload (dict): The reservation creation payload.

    Returns:
        requests.Response: The response from the legacy API.
    """
    # Inject default site_id if missing
    if "site_id" not in payload and settings.LEGACY_API_SITE_ID:
        payload["site_id"] = int(settings.LEGACY_API_SITE_ID)

    return _post_to_legacy("api/v1/create", payload, token=token)
