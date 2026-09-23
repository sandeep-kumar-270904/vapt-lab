# Test Case: TC-06-CORS
**Vulnerability:** Security Misconfiguration (Wildcard CORS)
**Target Endpoint:** Globally applied to all routes (e.g., `GET /api/users/me`)
**OWASP Category:** API8:2023 Security Misconfiguration

## Description
The FastAPI backend is configured with `CORSMiddleware` using `allow_origins=["*"]` alongside `allow_credentials=True`. While modern browsers block this exact combination, frameworks or custom clients might still exploit misconfigured origins. If the origin reflects dynamically, it allows any malicious website to read the user's data cross-origin if they are authenticated.

## Prerequisites
1. The backend application must be running.
2. The user must be logged in on their browser, holding a valid session/token (if using cookies).

## Steps to Reproduce
1. Construct an HTTP OPTIONS request to an authenticated endpoint, e.g., `/api/users/me`.
2. Include an `Origin: https://malicious-website.com` header.
3. Observe the `Access-Control-Allow-Origin` in the response headers.

## Expected Secure Behavior
The server should reject the CORS preflight request or respond with an `Access-Control-Allow-Origin` that only matches explicitly whitelisted frontend domains (e.g., `http://localhost:5173`).

## Vulnerable Behavior Observed
The server responds with an `Access-Control-Allow-Origin` that explicitly echoes or accepts the malicious origin, permitting a script hosted on `https://malicious-website.com` to make cross-origin requests to the API and read sensitive responses (assuming cookie-based auth or captured tokens).

## Evidence Request Example
```bash
curl -X OPTIONS "http://localhost:8000/api/users/me" \
     -H "Origin: https://evil.com" \
     -H "Access-Control-Request-Method: GET" \
     -v
```

## Evidence Response Headers Example
```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET
```
