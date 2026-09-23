# Test Case: TC-05-DATA-EXPOSURE
**Vulnerability:** Excessive Data Exposure
**Target Endpoint:** `GET /api/users/{user_id}`
**OWASP Category:** API3:2023 Broken Object Property Level Authorization (formerly Excessive Data Exposure)

## Description
The user profile endpoint uses a Pydantic schema (`UserResponse`) that explicitly includes the `password_hash` field. Even if a user is legally authorized to view a profile, the API returns highly sensitive backend properties that should never leave the server boundary.

## Prerequisites
1. An authenticated user (e.g., `attacker@example.com`).
2. A valid target `user_id` (e.g., `2` for an administrator).

## Steps to Reproduce
1. Log in as the attacker.
2. Send a `GET` request to `/api/users/2`. (Note: In our vulnerable lab, BOLA is also present here, allowing access to user 2).
3. Observe the JSON response body.

## Expected Secure Behavior
The API should return public or authorized profile information (e.g., email, role, created_at) but strictly omit internal security fields like `password_hash`.

## Vulnerable Behavior Observed
The API returns the user's Bcrypt `password_hash`. The attacker can now take this hash offline and use tools like Hashcat or John the Ripper to crack the administrator's password.

## Evidence Request Example
```bash
curl -X GET "http://localhost:8000/api/users/2" \
     -H "Authorization: Bearer ATTACKER_JWT_TOKEN"
```

## Evidence Response Example
```json
{
  "email": "admin@example.com",
  "id": 2,
  "role": "admin",
  "created_at": "2026-09-23T00:00:00Z",
  "password_hash": "$2b$12$NqL9/..."
}
```
