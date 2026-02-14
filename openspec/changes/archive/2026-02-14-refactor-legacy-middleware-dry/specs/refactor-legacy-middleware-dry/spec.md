# legacy-proxy-infrastructure Specification Delta

## ADDED Requirements

### Requirement: Shared Legacy Proxy Infrastructure
> As a system developer, I want to use a shared base class for legacy proxy views so that authentication and error handling are consistent and DRY. The system **SHALL** provide a base view class for all legacy proxy endpoints to inherit from.

#### Scenario: Base View usage
- **Given** several proxy views (`QuoteProxyView`, `ReservationCreateProxyView`)
- **When** I inspect their implementation
- **Then** they should both inherit from a common `BaseLegacyProxyView`
- **And** they should use a shared method for executing upstream requests with retry logic.

### Requirement: Unified Legacy Service Helper
> As a system developer, I want a shared helper function for making legacy API requests so that payload injection and header construction are DRY. The system **MUST** use a centralized private helper in `services.py` for all legacy POST requests.

#### Scenario: Service helper usage
- **Given** `fetch_quote` and `fetch_reservation_create` services
- **When** I inspect their implementation
- **Then** they should both utilize a private `_post_to_legacy` helper function
- **And** individual services should only be responsible for their specific payload modifications (like `rate_group` or `site_id`).

### Requirement: Consistent Upstream Error Mapping
> As a system, I want to map all upstream errors to standard DRF responses in a single place to ensure consistency across all proxy endpoints. The system **SHALL** use a standardized error mapping mechanism in the base proxy view.

#### Scenario: Error mapping consistency
- **Given** an upstream error (e.g., 500 from legacy, or a timeout)
- **When** any proxy endpoint receives this error
- **Then** it should return a standardized 502 Bad Gateway response with a consistent JSON structure.
