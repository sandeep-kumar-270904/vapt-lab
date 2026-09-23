# Test Case: TC-03-SQLI
**Vulnerability:** SQL Injection (SQLi)
**Target Endpoint:** `GET /api/products?search={query}`
**OWASP Category:** API8:2023 Security Misconfiguration / Traditional Injection

## Description
The product search endpoint takes user input from the `search` query parameter and interpolates it directly into a raw SQL query string without using parameterized queries or ORM sanitization.

## Prerequisites
1. The backend application must be running.
2. (Optional) Basic user authentication if the endpoint requires it, though in our lab it is public.

## Steps to Reproduce
1. Construct an HTTP GET request to `/api/products`.
2. Provide a malicious SQL payload in the `search` parameter: `test%' OR '1'='1`.
3. URL-encode the payload: `test%25%27%20OR%20%271%27%3D%271`
4. Send the request to: `GET /api/products?search=test%25%27%20OR%20%271%27%3D%271`

## Expected Secure Behavior
The application should treat the input strictly as a string literal and search for products containing the exact text `test%' OR '1'='1`. It should return `[]` (empty list) or safely filter the database.

## Vulnerable Behavior Observed
The SQL engine evaluates the injected OR clause (`OR '1'='1'`), overriding the `LIKE` clause. The server returns a `200 OK` response containing every single product in the database, bypassing intended search restrictions. Further manipulation could allow UNION-based data extraction.

## Evidence Request Example
```bash
curl -X GET "http://localhost:8000/api/products?search=test%25%27%20OR%20%271%27%3D%271"
```

## Evidence Response Example
```json
[
  {"id": 1, "name": "Laptop", "price": 1200.0, "stock": 10},
  {"id": 2, "name": "Hidden Internal Product", "price": 0.0, "stock": 0},
  ...
]
```
