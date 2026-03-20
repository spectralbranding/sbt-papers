# /security-scan

Run security scan using Trivy.

## Usage

```
/security-scan
```

## Instructions

When invoked, Claude should run:

```bash
trivy fs . --scanners secret,misconfig
```

## What It Scans

- **Secrets**: API keys, passwords, tokens in code
- **Misconfigurations**: Dockerfile, Kubernetes, Terraform issues
- **Vulnerabilities**: Known CVEs in dependencies (if enabled)

## Output Format

Trivy outputs findings in severity order:

```
=== Security Scan Results ===

Scanning current directory...

SECRET: High - AWS Access Key found
  File: config/settings.py:42
  Match: AKIA...

MISCONFIG: Medium - Dockerfile runs as root
  File: Dockerfile:1
  Suggestion: Add USER directive

Summary:
  CRITICAL: 0
  HIGH: 1
  MEDIUM: 1
  LOW: 0
```

## Pre-Commit Integration

This scan runs automatically via pre-commit hook. Manual scan is useful for:
- Checking before committing
- Scanning specific directories
- Full project audit

## Fix Suggestions

Common fixes:
- **Secrets**: Use environment variables or sops-encrypted files
- **Root user**: Add `USER nonroot` to Dockerfile
- **Vulnerabilities**: Update dependencies

## Related

- [SECRETS.md](../knowledge-base/SECRETS.md) - Secrets management
- Pre-commit hooks in `.pre-commit-config.yaml`
