# Code Review Security Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Security-focused code review workflows

---

## Overview

Systematic security review workflow for code changes. Detects OWASP Top 10 vulnerabilities, secrets leaks, and insecure patterns.

## When to Use This Skill

- Before merging pull requests
- After implementing authentication/authorization
- When handling sensitive data
- Regular security audits
- Pre-release security checks

## Security Checks

### 1. OWASP Top 10
- SQL Injection (parameterized queries?)
- XSS (output escaping?)
- Authentication bypass (session validation?)
- Broken access control (authorization checks?)
- Security misconfiguration (defaults changed?)
- Sensitive data exposure (encryption?)
- Insufficient logging
- SSRF (URL validation?)
- Deserialization (safe parsing?)
- Component vulnerabilities (outdated deps?)

### 2. Secrets & Credentials
- API keys in code
- Passwords hardcoded
- Tokens in environment
- Private keys committed
- Database credentials

### 3. Input Validation
- User input sanitized?
- File uploads validated?
- Path traversal prevented?
- Command injection blocked?
- JSON/XML parsing safe?

### 4. Cryptography
- Strong algorithms (AES-256, RSA-2048+)
- Secure random number generation
- Proper key management
- Certificate validation
- TLS version enforcement

### 5. Dependencies
- Known vulnerabilities (CVEs)
- Outdated packages
- Supply chain risks
- License compliance

## Workflow

### Phase 1: Automated Scanning

```bash
# Secrets scanning
trivy fs --scanners secret .

# Dependency vulnerabilities
trivy fs --scanners vuln .

# Python security issues
uv run bandit -r src/

# JavaScript/Node
npm audit

# Static analysis
uv run flake8 --select=S
```

### Phase 2: Manual Review

**Authentication/Authorization**:
- [ ] User input validated before auth checks
- [ ] Session tokens cryptographically strong
- [ ] Password requirements enforced (length, complexity)
- [ ] Rate limiting on login attempts
- [ ] Multi-factor authentication considered
- [ ] Authorization checked on every protected resource

**Data Handling**:
- [ ] Sensitive data encrypted at rest
- [ ] Encryption in transit (TLS 1.2+)
- [ ] PII handling compliant (GDPR, etc.)
- [ ] Secure data deletion implemented
- [ ] Backup encryption configured

**API Security**:
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] CORS configured correctly
- [ ] API keys rotatable
- [ ] Error messages don't leak info

### Phase 3: Context Review

**File-Specific Patterns**:

For `.env` / config files:
- No secrets committed
- Template files only (.env.template)
- Documentation references secrets management

For authentication code:
- Timing attack prevention
- Password hashing (bcrypt, argon2)
- Session expiry configured
- Logout clears sessions

For database code:
- Parameterized queries only
- Connection pooling secure
- Least privilege principle
- Query timeouts configured

For API endpoints:
- Authentication required
- Authorization granular
- Input validation comprehensive
- Output encoding applied

### Phase 4: Reporting

```
Security Review Report - 2026-02-05
====================================

Repository: my-project
Branch: feature/user-auth
Reviewer: Claude Code
Files: 12 changed

CRITICAL ISSUES: 2
- src/auth/login.py:45 - Hardcoded database password
- src/api/users.py:123 - SQL injection vulnerability

HIGH PRIORITY: 5
- No rate limiting on /api/login
- Passwords stored with MD5 (use bcrypt)
- Session tokens not cryptographically random
- CORS allows all origins (*)
- Error messages expose stack traces

MEDIUM PRIORITY: 8
- Outdated dependency: requests 2.25.0 (CVE-2023-xxx)
- Missing CSRF protection on forms
- No input length limits on text fields
- Logging includes sensitive data
- TLS 1.0 allowed (require 1.2+)
- Missing security headers (CSP, HSTS)
- No API request throttling
- Weak password requirements (6+ chars)

RECOMMENDATIONS:
1. Fix critical: Remove hardcoded password, fix SQL injection
2. Upgrade authentication: bcrypt, rate limiting, strong sessions
3. Update dependencies: requests, flask, etc.
4. Add security headers: helmet.js or equivalent
5. Implement CSRF protection
6. Review logging: exclude sensitive data
7. Strengthen password policy: 12+ chars, complexity

OWASP Top 10 Coverage:
✅ A01:2021 - Broken Access Control (reviewed)
❌ A02:2021 - Cryptographic Failures (MD5 usage)
❌ A03:2021 - Injection (SQL injection found)
✅ A04:2021 - Insecure Design (reviewed)
⚠️  A05:2021 - Security Misconfiguration (TLS 1.0)
✅ A06:2021 - Vulnerable Components (scanned)
⚠️  A07:2021 - Authentication Failures (weak passwords)
✅ A08:2021 - Data Integrity Failures (reviewed)
✅ A09:2021 - Logging Failures (reviewed)
✅ A10:2021 - SSRF (reviewed)

Score: 6/10 Critical Issues Block Merge
```

## Tools Integration

### Trivy (Secrets & Vulnerabilities)
```bash
trivy fs --scanners secret,vuln --severity CRITICAL,HIGH .
```

### Bandit (Python Security)
```bash
uv run bandit -r src/ -f json -o security-report.json
```

### Safety (Python Dependencies)
```bash
uv run safety check --json
```

### npm audit (Node Dependencies)
```bash
npm audit --audit-level=moderate
```

### Semgrep (Pattern Matching)
```bash
semgrep --config=auto src/
```

## Common Vulnerability Patterns

### SQL Injection

**Bad**:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Good**:
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### XSS

**Bad**:
```python
return f"<h1>Welcome {username}</h1>"
```

**Good**:
```python
from markupsafe import escape
return f"<h1>Welcome {escape(username)}</h1>"
```

### Hardcoded Secrets

**Bad**:
```python
API_KEY = "sk_live_abc123def456"
```

**Good**:
```python
import os
API_KEY = os.environ["API_KEY"]
```

### Path Traversal

**Bad**:
```python
filepath = f"/uploads/{filename}"
return send_file(filepath)
```

**Good**:
```python
from werkzeug.utils import secure_filename
filename = secure_filename(filename)
filepath = os.path.join(UPLOAD_DIR, filename)
if not filepath.startswith(UPLOAD_DIR):
raise ValueError("Invalid filename")
return send_file(filepath)
```

### Insecure Deserialization

**Bad**:
```python
import pickle
data = pickle.loads(user_input)
```

**Good**:
```python
import json
data = json.loads(user_input)
```

### Command Injection

**Bad**:
```python
import os
os.system(f"ping {user_host}")
```

**Good**:
```python
import subprocess
subprocess.run(["ping", "-c", "4", user_host], check=True)
```

### Weak Cryptography

**Bad**:
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Good**:
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### SSRF

**Bad**:
```python
import requests
url = request.args.get("url")
response = requests.get(url)
```

**Good**:
```python
import requests
from urllib.parse import urlparse

url = request.args.get("url")
parsed = urlparse(url)

# Whitelist allowed domains
if parsed.netloc not in ["api.example.com", "cdn.example.com"]:
raise ValueError("Invalid URL")

response = requests.get(url)
```

### Insecure Random

**Bad**:
```python
import random
token = random.randint(100000, 999999)
```

**Good**:
```python
import secrets
token = secrets.token_urlsafe(32)
```

## Automation

Can be integrated into:
- Pre-commit hooks (quick checks)
- Pull request reviews (comprehensive)
- CI/CD pipeline (block on critical)
- Scheduled audits (weekly/monthly)

### Pre-commit Hook Example

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running security checks..."

# Check for secrets
trivy fs --scanners secret --exit-code 1 . || exit 1

# Check Python security
if [ -d "src" ]; then
uv run bandit -r src/ -ll || exit 1
fi

# Check dependencies
if [ -f "pyproject.toml" ]; then
uv run safety check || exit 1
fi

echo "Security checks passed"
```

### CI/CD Pipeline Example

```yaml
# .github/workflows/security.yml
name: Security Review

on: [pull_request]

jobs:
security:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v3

- name: Run Trivy
uses: aquasecurity/trivy-action@master
with:
scan-type: 'fs'
scanners: 'secret,vuln'
severity: 'CRITICAL,HIGH'
exit-code: '1'

- name: Run Bandit
run: |
pip install bandit
bandit -r src/ -ll

- name: Run Safety
run: |
pip install safety
safety check --json
```

## Fleet-Specific Patterns

### Bitwarden Secrets Manager

**Check for**:
- No hardcoded secrets (should use Bitwarden)
- .env files only have non-secret config
- .envrc properly configured
- .env.template documents secret sources

**Example review**:
```python
# Bad: Hardcoded API key
ANTHROPIC_API_KEY = "sk-ant-api03-xxx"

# Good: From environment (loaded by direnv/Bitwarden)
import os
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
```

### sops + age Encryption

**Check for**:
- Encrypted files use .encrypted suffix
- .sops.yaml configured correctly
- age public key in config
- No plaintext secrets in git

**Example review**:
```bash
# Bad: .env committed with secrets
git add .env

# Good: Encrypted version committed
sops -e .env > .env.encrypted
git add .env.encrypted
```

### Trivy Integration

**Check for**:
- Pre-commit hook includes trivy
- CI pipeline runs trivy
- No secrets in git history
- Dependencies scanned for CVEs

**Example review**:
```bash
# Run comprehensive scan
trivy fs --scanners secret,vuln,config --severity CRITICAL,HIGH,MEDIUM .
```

## Related Skills

- python-dev: Python security patterns
- documentation-audit: Documentation review
- fleet-ops: Deployment security

## Related Commands

- `/security-scan` - Run security tools
- `/review` - General code review
- `/pre-commit` - Format, lint, test

## References

- SECRETS.md - Secret management patterns
- CODING_PRINCIPLES.md - Secure coding principles
- CI_TROUBLESHOOTING.md - CI security checks
- BITWARDEN_SECRETS.md - Bitwarden integration
- SOPS_AGE.md - File encryption

## Examples

### Example 1: Pre-Merge Security Review

**User**: "Security review PR #123 before merging"

**Agent**:
1. Runs trivy for secrets and vulns
2. Manual review of changed files
3. Checks authentication/authorization
4. Validates input handling
5. Reviews crypto usage
6. Generates detailed report
7. Blocks merge if critical issues

**Commands**:
```bash
# Automated scans
trivy fs --scanners secret,vuln --severity CRITICAL,HIGH .
uv run bandit -r src/ -ll
uv run safety check

# Manual review
git diff main...feature/user-auth
```

**Report**:
```
Security Review: PR #123
========================

Critical Issues: 1
- src/auth/login.py:45 - Hardcoded database password

High Priority: 2
- No rate limiting on /api/login
- Passwords stored with MD5

Recommendation: DO NOT MERGE until critical issues resolved
```

### Example 2: Dependency Audit

**User**: "Audit Python dependencies for vulnerabilities"

**Agent**:
1. Runs safety check
2. Checks for known CVEs
3. Identifies outdated packages
4. Recommends updates
5. Generates upgrade plan

**Commands**:
```bash
# Check dependencies
uv run safety check --json

# Scan with trivy
trivy fs --scanners vuln --severity HIGH,CRITICAL .

# List outdated packages
uv pip list --outdated
```

**Report**:
```
Dependency Audit Report
=======================

Critical Vulnerabilities: 2
- requests 2.25.0 (CVE-2023-32681) - Upgrade to 2.31.0+
- flask 2.0.1 (CVE-2023-30861) - Upgrade to 2.3.2+

High Priority: 5
- cryptography 38.0.0 (outdated) - Upgrade to 42.0.0+
- pillow 9.0.0 (CVE-2023-44271) - Upgrade to 10.2.0+
- urllib3 1.26.5 (outdated) - Upgrade to 2.1.0+
- certifi 2022.12.7 (outdated) - Upgrade to 2024.2.2+
- setuptools 65.0.0 (CVE-2024-6345) - Upgrade to 70.0.0+

Upgrade Command:
uv pip install --upgrade requests flask cryptography pillow urllib3 certifi setuptools
```

### Example 3: Authentication Implementation Review

**User**: "Review new JWT authentication implementation"

**Agent**:
1. Reviews JWT token generation
2. Checks token validation
3. Verifies secret management
4. Tests for timing attacks
5. Reviews session management
6. Validates refresh token flow
7. Checks rate limiting

**Review Checklist**:
```
JWT Authentication Review
=========================

Token Generation:
✅ Secret loaded from environment (not hardcoded)
✅ Strong algorithm (HS256 with 256-bit key)
❌ No token expiration set (add exp claim)
⚠️  No token refresh mechanism (consider refresh tokens)

Token Validation:
✅ Signature verified
✅ Algorithm validated (no "none" allowed)
❌ No issuer/audience validation (add iss/aud claims)
✅ Timing attack prevention (constant-time comparison)

Session Management:
✅ Session tokens cryptographically random
❌ No session expiry (add timeout)
⚠️  Sessions not invalidated on logout (clear server-side)

Rate Limiting:
❌ No rate limiting on /auth/login (add throttling)
❌ No account lockout after failed attempts

Recommendations:
1. Add token expiration (15 min access, 7 day refresh)
2. Implement refresh token rotation
3. Add iss/aud claims for validation
4. Add session expiry (24 hours)
5. Implement logout session clearing
6. Add rate limiting (5 attempts/min per IP)
7. Add account lockout (10 failed attempts)
```

### Example 4: API Endpoint Security

**User**: "Review security of new /api/users endpoint"

**Agent**:
1. Checks authentication requirement
2. Validates authorization granularity
3. Reviews input validation
4. Tests for injection vulnerabilities
5. Checks output encoding
6. Validates error handling
7. Reviews rate limiting

**Review**:
```python
# Endpoint code
@app.route("/api/users/<user_id>", methods=["GET", "POST"])
def user_endpoint(user_id):
# Agent review findings:

# CRITICAL: No authentication required
# Fix: Add @require_auth decorator

# CRITICAL: No authorization check
# Fix: Verify current_user.id == user_id or current_user.is_admin

# HIGH: user_id not validated
# Fix: Validate user_id is numeric, in range

# HIGH: SQL injection possible
query = f"SELECT * FROM users WHERE id = {user_id}"
# Fix: Use parameterized queries

# MEDIUM: No rate limiting
# Fix: Add @rate_limit("100/hour") decorator

# MEDIUM: Error messages expose details
except Exception as e:
return {"error": str(e)}
# Fix: Return generic error, log details server-side

# Recommended fix:
@app.route("/api/users/<int:user_id>", methods=["GET", "POST"])
@require_auth
@rate_limit("100/hour")
def user_endpoint(user_id):
# Authorization
if current_user.id != user_id and not current_user.is_admin:
return {"error": "Forbidden"}, 403

# Input validation
if not (1 <= user_id <= 999999):
return {"error": "Invalid user ID"}, 400

# Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

try:
# ... logic ...
except Exception as e:
logger.error(f"Error in user_endpoint: {e}")
return {"error": "Internal server error"}, 500
```

## Advanced Patterns

### Security Headers

**Check for**:
```python
# Flask/FastAPI
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["X-XSS-Protection"] = "1; mode=block"
response.headers["Content-Security-Policy"] = "default-src 'self'"
```

### CORS Configuration

**Bad**:
```python
CORS(app, origins="*")
```

**Good**:
```python
CORS(app, origins=["https://example.com"], supports_credentials=True)
```

### File Upload Security

**Check for**:
- File type validation (whitelist, not blacklist)
- File size limits
- Virus scanning (if needed)
- Storage outside webroot
- Random filenames

**Example**:
```python
from werkzeug.utils import secure_filename
import os
import uuid

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
@require_auth
def upload_file():
if "file" not in request.files:
return {"error": "No file"}, 400

file = request.files["file"]

# Validate filename
if not allowed_file(file.filename):
return {"error": "Invalid file type"}, 400

# Validate size
file.seek(0, os.SEEK_END)
size = file.tell()
if size > MAX_FILE_SIZE:
return {"error": "File too large"}, 400
file.seek(0)

# Generate random filename
ext = file.filename.rsplit(".", 1)[1].lower()
filename = f"{uuid.uuid4()}.{ext}"
filepath = os.path.join(UPLOAD_DIR, filename)

file.save(filepath)
return {"filename": filename}, 200
```

### Database Security

**Check for**:
- Parameterized queries (never string interpolation)
- Least privilege database user
- Connection pooling
- Query timeouts
- No sensitive data in logs

**Example**:
```python
# Bad
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Good
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# Good: ORM
user = User.query.filter_by(email=email).first()
```

## Scorecard

Use this to generate a security score:

```
Security Scorecard
==================

Authentication: 7/10
✅ Password hashing (bcrypt)
✅ Session management
❌ No MFA support
⚠️  Weak password policy

Authorization: 8/10
✅ Role-based access control
✅ Resource-level permissions
✅ Admin separation
⚠️  No audit logging

Input Validation: 6/10
✅ Type checking
❌ No length limits
❌ No sanitization
⚠️  Partial XSS protection

Cryptography: 9/10
✅ Strong algorithms
✅ TLS 1.2+
✅ Secure random
✅ Proper key management

Dependencies: 5/10
⚠️  2 critical CVEs
⚠️  5 outdated packages
✅ License compliance

Secrets Management: 10/10
✅ Bitwarden integration
✅ No hardcoded secrets
✅ Environment variables
✅ sops encryption

Overall Score: 75/100 (Pass)
```

---

**End of Skill**
