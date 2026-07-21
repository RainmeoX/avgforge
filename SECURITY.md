# Security Policy

## Supported Versions

AVGForge is committed to providing security updates for the following versions:

| Version | Supported          | Status       |
|---------|--------------------|--------------|
| 1.0.x   | ✅ Active support  | Current GA   |
| 0.9.x   | ⚠️ Critical only   | End-of-life  |
| < 0.9   | ❌ Not supported   | Deprecated   |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue,
please follow responsible disclosure:

### 🔒 Private Disclosure

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report vulnerabilities privately:

1. **Email:** `security@avgforge.example`
2. **Subject:** `[SECURITY] AVGForge Vulnerability Report`
3. **Include:**
   - Description of the vulnerability
   - Affected versions
   - Reproduction steps (proof of concept)
   - Potential impact assessment
   - Suggested fix (if any)

### Response Timeline

| Stage | Target SLA |
|-------|------------|
| Acknowledgment of report | 24 hours |
| Initial assessment | 72 hours |
| Fix development | 7-14 days (severity-dependent) |
| Patch release | 30 days (critical) / 90 days (high) |
| Public disclosure | After patch release + 14-day grace period |

### Severity Classification

We use the [CVSS v3.1](https://www.first.org/cvss/) scoring system:

| Severity | CVSS Score | Examples |
|----------|------------|----------|
| **Critical** | 9.0-10.0 | Remote code execution, arbitrary file access |
| **High** | 7.0-8.9 | Path traversal, XSS in preview engine |
| **Medium** | 4.0-6.9 | Information disclosure, DoS |
| **Low** | 0.1-3.9 | Minor info leak, cosmetic issues |

## Security Measures

### Project File Safety

AVGForge processes JSON project files. We implement:

- **Path traversal protection** — All file paths are validated against project root
- **JSON schema validation** — Malformed inputs are rejected before processing
- **Asset path sanitization** — No absolute paths or `..` traversal allowed
- **Size limits** — Project files exceeding 100MB are rejected

### Web Preview Security

The web preview engine runs locally and includes:

- **Content Security Policy** headers
- **Sandboxed iframe** for project preview
- **No external network requests** (fully offline)
- **Input sanitization** for all user-provided text

### Build Output Safety

Generated HTML files:

- **No inline event handlers** (CSP-compliant)
- **Escaped user content** (XSS prevention)
- **No eval() or Function()** on user data
- **Base64-encoded assets** (no path leakage)

## Best Practices for Users

### Project Hygiene

```bash
# Always validate projects before building
avgforge check --strict

# Use Git for version control (enables rollback)
git init my-project && cd my-project
avgforge init . --template blank
git add . && git commit -m "Initial project"

# Review asset references periodically
avgforge asset refs --unused
```

### CI/CD Security

```yaml
# .github/workflows/build.yml
- name: Build project
  run: |
    avgforge check --strict
    avgforge build html --output dist/
  env:
    AVGFORGE_NO_NETWORK: "true"  # Disable all network features
```

### Asset Handling

- **Scan imported assets** for malware before adding to project
- **Use trusted sources** for BGM, SE, and voice files
- **Audit third-party extensions** before installation
- **Review build output** before distribution

## Known Security Considerations

### 1. Local File Access

AVGForge reads and writes files within the project directory. Ensure:
- Project directories are not world-writable on multi-user systems
- CI/CD runners have appropriate filesystem permissions
- Build outputs are scanned before distribution

### 2. Web Preview Server

The preview server binds to `localhost` by default. **Do not expose it to
public networks** without additional authentication.

### 3. Extension System

Third-party extensions can execute arbitrary Python code. Only install
extensions from trusted sources and review their code before use.

## Compliance

AVGForge is designed to support compliance with:

- **OWASP Top 10** — Web preview follows OWASP guidelines
- **NIST SP 800-53** — Suitable for federal information systems (with commercial license)
- **GDPR** — No personal data collection; all processing is local
- **SOC 2 Type II** — Documentation available for enterprise customers

## Contact

- **Security reports:** `security@avgforge.example`
- **PGP key:** [Download from /security/pgp-key.asc](security/pgp-key.asc)
- **General inquiries:** `community@avgforge.example`

## Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities.
Contributors are acknowledged (with permission) in our security advisories.

---

Last updated: 2026-07-21
