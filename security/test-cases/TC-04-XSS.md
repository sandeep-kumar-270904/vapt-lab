# Test Case: TC-04-XSS
**Vulnerability:** Stored Cross-Site Scripting (XSS)
**Target Endpoint:** `POST /api/reviews` & `GET /api/reviews/{product_id}`
**OWASP Category:** API8:2023 Security Misconfiguration / Traditional XSS

## Description
The application allows users to submit product reviews. The `comment` field is saved to the database without input sanitization or HTML encoding. When other users view the reviews, the frontend renders the unsanitized payload, leading to arbitrary JavaScript execution in their browsers.

## Prerequisites
1. An attacker account with a valid JWT.
2. A victim account or an administrator viewing the product.
3. A valid `product_id` (e.g., `1`).

## Steps to Reproduce
1. Log in as the attacker.
2. Send a `POST` request to `/api/reviews` containing a malicious XSS payload in the `comment` field: `<script>alert(document.cookie)</script>`.
3. Log in as the victim.
4. Navigate to the product page or hit the `GET /api/reviews/1` endpoint.

## Expected Secure Behavior
The server should either reject the input containing HTML tags, or HTML-encode it before storage/retrieval (e.g., converting `<script>` to `&lt;script&gt;`).

## Vulnerable Behavior Observed
The server accepts the raw HTML payload. When the victim retrieves the reviews, the payload is returned verbatim. If the frontend (React) uses `dangerouslySetInnerHTML` to render it, the script executes, popping an alert box and exposing the victim's session/tokens.

## Evidence Request Example
```bash
curl -X POST "http://localhost:8000/api/reviews" \
     -H "Authorization: Bearer ATTACKER_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1, "rating": 5, "comment": "<script>alert(\"XSS\")</script>"}'
```

## Evidence Response Example (GET)
```json
[
  {
    "id": 1,
    "product_id": 1,
    "user_id": 1,
    "rating": 5,
    "comment": "<script>alert(\"XSS\")</script>"
  }
]
```
