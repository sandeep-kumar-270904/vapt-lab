import requests
import json
import time

# Configuration for the VAPT-Lab Assessment Platform API
PLATFORM_URL = "http://localhost:8001/api"

print("Starting VAPT-Lab Platform Data Seeding...")
print("Note: This script seeds the tracking platform with findings.")
print("It does NOT execute exploits against the target application.\n")

# 1. Create a new Assessment
print("[*] Creating Assessment...")
assessment_data = {
    "target_name": "MarketHub Web & API (Vulnerable Lab)",
    "description": "Authorized Q3 Security Assessment against the MarketHub infrastructure."
}
resp = requests.post(f"{PLATFORM_URL}/assessments/", json=assessment_data)
if resp.status_code != 200:
    print(f"Failed to create assessment: {resp.text}")
    exit(1)

assessment_id = resp.json()["id"]
print(f"[+] Assessment created with ID: {assessment_id}")

# 2. Define Findings based on our Test Cases
findings = [
    {
        "title": "SQL Injection in Product Search",
        "severity": "Critical",
        "description": "The `/api/products` endpoint is vulnerable to SQL injection via the `search` parameter. Input is directly interpolated into the SQL query without sanitization or parameterization.",
        "impact": "An attacker can extract, modify, or delete all data in the database, potentially leading to a full system compromise.",
        "remediation": "Use parameterized queries or SQLAlchemy's ORM filtering capabilities (e.g., `.filter(Product.name.ilike(...))`).",
        "cvss_score": "9.8 (CRITICAL)",
        "evidence": {
            "description": "Exploiting the search parameter using a boolean OR bypass.",
            "request_payload": "GET /api/products?search=test%25%27%20OR%20%271%27%3D%271 HTTP/1.1\nHost: localhost:8000",
            "response_payload": "HTTP/1.1 200 OK\n\n[{\"id\": 1, \"name\": \"Laptop\"}, {\"id\": 2, \"name\": \"Hidden Product\"}]"
        }
    },
    {
        "title": "Broken Object Level Authorization (BOLA)",
        "severity": "High",
        "description": "The `/api/orders/{order_id}` endpoint does not verify if the requesting user actually owns the specified order.",
        "impact": "An attacker can sequentially enumerate `order_id` values and read the private order details of all customers.",
        "remediation": "Implement an ownership check: `if order.customer_id != current_user.id: raise 403 Forbidden`.",
        "cvss_score": "7.5 (HIGH)",
        "evidence": {
            "description": "Accessing another user's order using a standard customer token.",
            "request_payload": "GET /api/orders/5 HTTP/1.1\nAuthorization: Bearer ATTACKER_TOKEN",
            "response_payload": "HTTP/1.1 200 OK\n\n{\"id\": 5, \"customer_id\": 2, \"total_amount\": 999.99}"
        }
    },
    {
        "title": "Broken Function Level Authorization (BFLA)",
        "severity": "High",
        "description": "The `/api/users/{user_id}/role` endpoint lacks administrative checks, allowing any authenticated user to change roles.",
        "impact": "Privilege escalation. Any customer can elevate their own account to `admin`.",
        "remediation": "Add a check to verify that `current_user.role == UserRole.admin` before processing the role update.",
        "cvss_score": "8.8 (HIGH)",
        "evidence": {
            "description": "Standard user elevating themselves to admin.",
            "request_payload": "PUT /api/users/1/role?role=admin HTTP/1.1\nAuthorization: Bearer ATTACKER_TOKEN",
            "response_payload": "HTTP/1.1 200 OK\n\n{\"role\": \"admin\"}"
        }
    },
    {
        "title": "Stored Cross-Site Scripting (XSS)",
        "severity": "Medium",
        "description": "The `/api/reviews` endpoint stores raw HTML/JavaScript submitted in the `comment` field without sanitization.",
        "impact": "When viewed by an administrator, the malicious script executes in their browser, potentially stealing admin session tokens.",
        "remediation": "HTML-encode all user input before storing it, or use a strict sanitization library like DOMPurify on the frontend.",
        "cvss_score": "5.4 (MEDIUM)",
        "evidence": {
            "description": "Storing a malicious script in a review.",
            "request_payload": "POST /api/reviews HTTP/1.1\n\n{\"product_id\": 1, \"rating\": 5, \"comment\": \"<script>alert(1)</script>\"}",
            "response_payload": "HTTP/1.1 201 Created"
        }
    }
]

# 3. Insert Findings into Platform
print("\n[*] Populating Findings...")
for f in findings:
    finding_data = {
        "title": f["title"],
        "description": f["description"],
        "severity": f["severity"],
        "impact": f["impact"],
        "remediation": f["remediation"],
        "cvss_score": f["cvss_score"]
    }
    
    res = requests.post(f"{PLATFORM_URL}/findings/{assessment_id}", json=finding_data)
    if res.status_code == 200:
        finding_id = res.json()["id"]
        print(f"  [+] Logged: {f['title']}")
        
        # Insert Evidence
        ev = f["evidence"]
        ev_data = {
            "description": ev["description"],
            "request_payload": ev["request_payload"],
            "response_payload": ev["response_payload"]
        }
        ev_res = requests.post(f"{PLATFORM_URL}/findings/{finding_id}/evidence", json=ev_data)
        if ev_res.status_code != 200:
            print(f"      [-] Failed to add evidence: {ev_res.text}")
    else:
        print(f"  [-] Failed to log finding: {res.text}")

print("\n[+] Data seeding complete!")
print(f"You can now generate the final report via: GET {PLATFORM_URL}/reports/{assessment_id}/markdown")
