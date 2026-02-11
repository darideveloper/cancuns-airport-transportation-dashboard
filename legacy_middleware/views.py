from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests

from .services import fetch_legacy_autocomplete


class AutocompleteProxyView(APIView):
    """
    Proxy view for the legacy autocomplete API.
    """

    permission_classes = [AllowAny]  # Since it's public for the frontend

    def post(self, request, *args, **kwargs):
        keyword = request.data.get("keyword")
        if not keyword:
            return Response(
                {"error": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            legacy_response = fetch_legacy_autocomplete(keyword)
            legacy_response.raise_for_status()
            return Response(legacy_response.json(), status=status.HTTP_200_OK)
        except requests.HTTPError as e:
            # Handle HTTP errors from legacy API
            if e.response.status_code == 422:
                return Response(
                    e.response.json(), status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif 400 <= e.response.status_code < 500:
                # Pass through client errors roughly? Or generic 400?
                # Design says "providing necessary feedback if it's a validation error".
                try:
                    return Response(e.response.json(), status=e.response.status_code)
                except:
                    return Response(
                        {"error": "Upstream client error"},
                        status=e.response.status_code,
                    )
            else:
                # 5xx errors from upstream -> 502 Bad Gateway
                return Response(
                    {"error": "Upstream service unavailable"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
        except requests.RequestException:
            # Network errors -> 502 Bad Gateway
            return Response(
                {"error": "Upstream service unreachable"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
