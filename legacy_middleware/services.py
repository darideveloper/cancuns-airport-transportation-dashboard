import requests
from django.conf import settings


def _legacy_request(
    endpoint: str,
    method: str = "POST",
    payload: dict = None,
    params: dict = None,
    token: str = None,
    headers: dict = None,
    timeout: int = 10,
) -> requests.Response:
    """
    Internal helper to send a request to the legacy API.
    """
    url = f"{settings.LEGACY_API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    final_headers = {
        "Content-Type": "application/json",
    }

    if token:
        final_headers["Authorization"] = f"Bearer {token}"

    if headers:
        final_headers.update(headers)

    if method.upper() == "POST":
        return requests.post(
            url, json=payload, headers=final_headers, timeout=timeout, params=params
        )
    elif method.upper() == "GET":
        return requests.get(url, headers=final_headers, timeout=timeout, params=params)
    else:
        return requests.request(
            method,
            url,
            json=payload,
            headers=final_headers,
            timeout=timeout,
            params=params,
        )


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

    return _legacy_request(
        "api/v1/autocomplete-affiliates",
        method="POST",
        payload=payload,
        headers=headers,
    )


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

    response = _legacy_request("api/v1/oauth", method="POST", payload=payload)
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

    return _legacy_request("api/v1/quote", method="POST", payload=payload, token=token)


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

    return _legacy_request("api/v1/create", method="POST", payload=payload, token=token)


def fetch_payment_link(
    token, reservation_id, payment_provider, language, success_url, cancel_url
):
    """
    Fetch the payment link for a reservation.
    GET /api/v1/reservation/payment/handler

    Args:
        token (str): The OAuth token.
        reservation_id (str/int): The reservation ID.
        payment_provider (str): 'STRIPE' or 'PAYPAL'.
        language (str): Language code (e.g. 'en').
        success_url (str): Redirect URL on success.
        cancel_url (str): Redirect URL on cancel.

    Returns:
        requests.Response: The response containing the payment link.
    """
    params = {
        "type": payment_provider,
        "id": reservation_id,
        "language": language,
        "success_url": success_url,
        "cancel_url": cancel_url,
    }
    return _legacy_request(
        "api/v1/reservation/payment/handler",
        method="GET",
        params=params,
        token=token,
    )
