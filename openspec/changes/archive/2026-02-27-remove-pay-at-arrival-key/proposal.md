# Proposal: Remove 'pay_at_arrival' key from Reservation API

## Summary
This proposal aims to "completely remove" the `pay_at_arrival` key from the reservation creation process. This key, used to indicate cash payment upon arrival in the legacy system, is redundant with `payment_method` and should be eliminated from the codebase, documentation, and API integration.

## Problem
The `pay_at_arrival` key is used in several places (documentation, tests) and is sent to the legacy API as part of the reservation payload. It creates confusion with `payment_method` and adds unnecessary complexity to the API contract.

## Proposed Changes
1.  **Middleware:** In `ReservationCreateProxyView`, explicitly remove `pay_at_arrival` from the request data before proxying it to the legacy API. This ensures that even if a client sends it, it won't reach the upstream system.
2.  **Tests:** Remove `pay_at_arrival` from all test payloads in `legacy_middleware/tests/test_views.py`. Ensure that "cash" reservations are correctly handled by either omitting `payment_method` or setting it to `CASH`.
3.  **Documentation:** Remove all mentions of `pay_at_arrival` in `docs/*.md` and `openspec/specs/reservation-proxy/spec.md`. Update these docs to emphasize the use of `payment_method` instead.

## Impact
- **Client Impact:** Clients sending `pay_at_arrival` will no longer see it reflected in the upstream system (as it's stripped), but their reservations should still succeed if the legacy API defaults to cash or respects `payment_method`.
- **System Integrity:** Removing redundant keys simplifies the API contract and reduces potential for conflicting parameters (e.g., `payment_method="STRIPE"` and `pay_at_arrival=1`).
