# Test Case: TC-02-BFLA
**Vulnerability:** Broken Function Level Authorization (BFLA)
**Target Endpoint:** `PUT /api/users/{user_id}/role`
**OWASP Category:** API5:2023 Broken Function Level Authorization

## Description
The endpoint for updating a user's role is intended to be an administrative function. However, the endpoint does not strictly verify if the requesting user holds the `admin` role before executing the state-changing action.

## Prerequisites
1. A standard user account (e.g., `attacker@example.com` with ID `1`) configured with the `customer` role.
2. A valid authentication token (JWT) for `attacker@example.com`.

## Steps to Reproduce
1. Log in as `attacker@example.com` and obtain a Bearer token.
2. Confirm the attacker's current role is `customer` by calling `GET /api/users/me`.
3. Construct an HTTP PUT request to `/api/users/1/role?role=admin`.
4. Include the attacker's Bearer token in the `Authorization: Bearer <token>` header.
5. Send the request.

## Expected Secure Behavior
The server should verify the role inside the JWT. Recognizing the user is a `customer`, it should reject the request with a `403 Forbidden` response.

## Vulnerable Behavior Observed
The server accepts the request and updates the attacker's role in the database to `admin`, returning a `200 OK` response with the updated user object. The attacker has successfully escalated their privileges.

## Evidence Request Example
```bash
curl -X PUT "http://localhost:8000/api/users/1/role?role=admin" \
     -H "Authorization: Bearer ATTACKER_JWT_TOKEN" \
     -H "Content-Length: 0"
```

## Evidence Response Example
```json
{
  "email": "attacker@example.com",
  "id": 1,
  "role": "admin",
  "created_at": "2026-09-23T00:00:00Z"
}
```
