# Test Case: TC-01-BOLA
**Vulnerability:** Broken Object Level Authorization (BOLA) / IDOR
**Target Endpoint:** `GET /api/orders/{order_id}`
**OWASP Category:** API1:2023 Broken Object Level Authorization

## Description
The application allows authenticated users to access order details by providing an `order_id` in the URL. However, it fails to verify if the requesting user is the actual owner of the order.

## Prerequisites
1. Two valid user accounts: `attacker@example.com` and `victim@example.com`.
2. A valid authentication token (JWT) for `attacker@example.com`.
3. An existing order belonging to `victim@example.com` (e.g., Order ID: `5`).

## Steps to Reproduce
1. Log in as `attacker@example.com` and obtain a Bearer token.
2. Intercept or construct an HTTP GET request to `/api/orders/5` using Burp Suite or cURL.
3. Include the attacker's Bearer token in the `Authorization: Bearer <token>` header.
4. Send the request.

## Expected Secure Behavior
The server should check if the `customer_id` associated with Order #5 matches the `user_id` inside the attacker's JWT. It should return a `403 Forbidden` response.

## Vulnerable Behavior Observed
The server processes the request and returns a `200 OK` response containing the sensitive order details (total amount, status, victim's ID) belonging to the victim.

## Evidence Request Example
```bash
curl -X GET "http://localhost:8000/api/orders/5" \
     -H "Authorization: Bearer ATTACKER_JWT_TOKEN"
```

## Evidence Response Example
```json
{
  "total_amount": 999.99,
  "id": 5,
  "customer_id": 2, 
  "status": "pending"
}
```
*(Notice that `customer_id` is 2, while the attacker's ID might be 1).*
