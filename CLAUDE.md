# AI Context & Workflow
**Project:** JobpowercraftAI (formerly JobCraftAI)
**Last Updated:** 2025-01-24 20:25
**GCP Project:** my-project-3445-1696278622939

---

## Quick Start for AI Assistants

Before starting work on this project, follow this checklist:

1. Read `JobpowercraftAI-session-summary.md` for comprehensive session history and context
2. Review "Current Workflow Phase" section below to understand project state
3. Check "Next Steps" for prioritized tasks
4. Understand the CRITICAL email header injection vulnerability that must be fixed
5. Review recent decisions and architectural patterns established

---

## Project State

### Current Workflow Phase
**Phase:** Post-Refactoring - Security & Performance Improvements Implemented
**Code Quality:** 6.5/10 (Mediocre → Good)
**Status:** Partial implementation complete, critical vulnerability remains

### Progress Tracking
- [x] Brutal code analysis completed (3 iterations)
- [x] Critical security vulnerabilities identified
- [x] Cursor AI implementation phase (15 files modified)
- [x] Verification review completed
- [x] Session documentation created
- [ ] CRITICAL: Email header injection fix (NEXT PRIORITY)
- [ ] Legacy code cleanup
- [ ] Full Strategy Pattern migration
- [ ] Unit test coverage
- [ ] Production deployment

---

## Critical Information for AI Assistants

### CRITICAL VULNERABILITY - MUST FIX BEFORE PRODUCTION
**File:** `src/email_sender.py`
**Issue:** `_create_email_body()` method does NOT sanitize `company_name` or `position_title` parameters
**Risk:** Email header injection attack
**Example Attack:** `company_name = "Evil Corp\r\nBcc: attacker@evil.com"`
**Solution Required:** Add `_sanitize_email_field()` method with regex to strip newlines/carriage returns
**Priority:** IMMEDIATE (15 minutes)

### Security Improvements Already Implemented
1. Removed `--disable-web-security` flag from chrome_utils.py
2. Migrated API keys to environment variables (SecurePasswordManager)
3. Fixed browser pool sabotage (removed driver.quit() calls)
4. Created SecurityValidator class with SSRF protection

### Performance Improvements Already Implemented
1. Browser pooling (13x faster - reuse vs spawn)
2. Resume caching (1500x faster cache hits)
3. Code reduction (main.py: 1,495 → 1,432 lines)

### Architecture Improvements Already Implemented
1. Strategy Pattern for document generation (partial)
2. Type-safe enums (design_models.py)
3. Security utilities module (security_utils.py)
4. Browser pooling module (browser_pool.py)
5. Caching layer (resume_cache.py)

---

## Recent Session Summary (2025-01-24)

### Session Title
"Brutal Code Analysis + Cursor Implementation Review"

### Key Achievements
- **Code Quality:** 3.0/10 → 6.5/10 (+3.5 points, 117% improvement)
- **Issues Resolved:** 7/10 successfully fixed, 2/10 partially fixed, 1/10 CRITICAL remaining
- **Security:** 3/4 vulnerabilities patched
- **Performance:** 13x browser pooling + 1500x caching improvements
- **Architecture:** New modular structure established

### Three-Phase Approach
1. **Brutal Analysis (3 iterations)** - Identified 15 critical issues, rating 3/10
2. **Cursor Implementation** - Modified 15 files, created 5 new modules
3. **Verification Review** - Confirmed actual implementation vs claimed completion

### Key Findings
- Cursor AI claimed 7.5/10 ("all issues fixed")
- Actual verification showed 6.5/10 (modules existed but not fully integrated)
- Gap between "code generated" and "code properly integrated"
- Human verification essential for accurate assessment

---

## Next Steps (Prioritized)

### IMMEDIATE (Next Session - 15 min)
1. **FIX EMAIL HEADER INJECTION** (CRITICAL)
   - File: src/email_sender.py
   - Add _sanitize_email_field() method
   - Sanitize company_name and position_title
   - Test with malicious input

2. **Remove Legacy Deprecated Functions** (HIGH)
   - File: main.py lines 974-989
   - Delete old if/elif chains
   - Force Strategy Pattern usage

3. **Complete Strategy Pattern Migration** (HIGH)
   - Verify StrategyFactory is used everywhere
   - Remove fallback to old functions
   - Add unit tests

### SHORT-TERM (This Week)
4. Standardize code to English (remove Swedish/Italian)
5. Add unit tests for security validators
6. Complete code duplication elimination
7. Implement config caching

### LONG-TERM (This Month)
8. Comprehensive documentation update
9. Performance benchmarking
10. Achieve 80%+ test coverage
11. Production deployment preparation

---

## Context for AI Assistants

### Project Background
JobpowercraftAI automates job applications by:
- Scraping job postings from LinkedIn, TheHub.se, Arbetsförmedlingen
- Generating tailored resumes using LLMs (OpenAI/Anthropic/Google)
- Creating personalized cover letters
- Sending professional emails with attachments
- Tracking application statistics

**Technology Stack:**
- Python 3.10+
- Selenium (browser automation)
- LangChain (LLM orchestration)
- OpenAI/Anthropic/Google APIs
- SMTP (email sending)
- YAML (configuration)

### Current Focus
**Immediate:** Fix critical email header injection vulnerability
**Short-term:** Clean up legacy code, add tests
**Long-term:** Production-ready deployment with monitoring

### Patterns & Standards Established

#### Security Patterns
- **Environment Variables:** All API keys MUST be in environment variables, never hardcoded
- **Input Sanitization:** All user-controllable input MUST be sanitized before use in sensitive contexts
- **SSRF Protection:** URLs must be validated against internal IP ranges
- **Browser Security:** Never use --disable-web-security or similar dangerous flags

#### Performance Patterns
- **Browser Pooling:** Use singleton BrowserPool, never spawn per-job
- **Caching:** Use LRU cache for frequently accessed data (resumes, configs)
- **Resource Management:** Properly close/release resources, avoid driver.quit() in loops

#### Architecture Patterns
- **Strategy Pattern:** Use StrategyFactory for document type selection
- **Type Safety:** Use enums instead of magic strings
- **Modular Design:** Separate concerns (security, browser, caching, generation)
- **Dependency Injection:** Pass dependencies explicitly, avoid global state

#### Code Quality Standards
- **No Duplication:** Extract common logic to utility functions
- **Single Language:** Use English for all code, comments, and docs
- **Clear Naming:** Use descriptive variable/function names
- **Documentation:** Document all security-critical functions
- **Testing:** Aim for 80%+ test coverage

---

## Known Issues Summary

### CRITICAL (Must fix before production)
1. Email header injection in email_sender.py

### HIGH (Fix this week)
2. Legacy deprecated functions not removed
3. Incomplete Strategy Pattern migration

### MEDIUM (Fix this month)
4. Swedish/Italian mixed with English
5. Code duplication remains
6. Missing security unit tests

### LOW (Future improvements)
7. Config caching not implemented
8. Documentation needs update
9. Performance benchmarking incomplete

---

## Git Workflow

### Repository Information
- **GitHub:** https://github.com/NeoNemesis/JobpowercraftAI.git
- **Branch:** master
- **Authentication:** HTTPS (username + token)

### Commit Guidelines
- Use descriptive commit messages
- Reference issue numbers when applicable
- Include "why" not just "what" in commit descriptions
- Group related changes in single commits

### Current Branch Status
- Modified files: 15
- New files: 40+ (modules + documentation)
- Deleted files: 3
- Next commit: Should include all session changes with comprehensive message

---

## File Locations

### Core Application
- `main.py` - Main application entry point (1,432 lines)
- `config.py` - Configuration management
- `src/email_sender.py` - Email functionality (CRITICAL VULNERABILITY HERE)

### New Security Infrastructure
- `src/security_utils.py` - SecurityValidator, SSRF protection
- `src/utils/browser_pool.py` - Singleton browser pooling
- `src/utils/resume_cache.py` - LRU caching for resumes
- `src/utils/design_models.py` - Type-safe enums
- `src/libs/resume_and_cover_builder/document_strategy.py` - Strategy Pattern

### Configuration Files
- `data_folder/plain_text_resume.yaml` - Resume data
- `data_folder/secrets.yaml.example` - Example secrets (DO NOT COMMIT ACTUAL secrets.yaml)
- `data_folder/email_config.yaml.example` - Example email config

### Documentation
- `JobpowercraftAI-session-summary.md` - Comprehensive session analysis
- `README.md` - Project overview and setup
- `GEMINI.md` / `CLAUDE.md` - This file (AI context)
- Swedish documentation files - Should be translated to English

---

## Testing Strategy

### Security Tests (Priority: HIGH)
```python
# Test email header injection prevention
def test_email_sanitization():
    malicious_input = "Company\r\nBcc: attacker@evil.com"
    sanitized = _sanitize_email_field(malicious_input)
    assert "\r" not in sanitized
    assert "\n" not in sanitized

# Test SSRF protection
def test_ssrf_protection():
    validator = SecurityValidator()
    assert not validator.validate_url("http://127.0.0.1/admin")
    assert not validator.validate_url("http://192.168.1.1/")
```

### Performance Tests (Priority: MEDIUM)
```python
# Test browser pool performance
def test_browser_pool_performance():
    pool = BrowserPool()
    start = time.time()
    for _ in range(10):
        browser = pool.get_browser()
    duration = time.time() - start
    assert duration < 5.0  # Should be much faster than spawning

# Test cache performance
def test_resume_cache():
    cache = ResumeCache()
    # First access - cache miss
    start = time.time()
    resume1 = cache.get_resume("test.yaml")
    miss_time = time.time() - start

    # Second access - cache hit
    start = time.time()
    resume2 = cache.get_resume("test.yaml")
    hit_time = time.time() - start

    assert hit_time < miss_time / 100  # 100x faster minimum
```

### Integration Tests (Priority: HIGH)
```python
# Test full job application flow
def test_job_application_flow():
    # Should not spawn multiple browsers
    # Should use cached resumes when possible
    # Should sanitize all email inputs
    # Should not leak credentials
```

---

## Performance Metrics to Track

### Browser Pooling
- Time to get browser instance (target: <0.5s)
- Number of browser spawns per 100 jobs (target: 1-2)
- Memory usage over time (target: stable)

### Caching
- Cache hit rate (target: >80%)
- Cache miss time vs hit time (target: >100x difference)
- Memory usage (target: <500MB)

### Application Processing
- Time per job application (target: <30s)
- Success rate (target: >90%)
- Email delivery rate (target: >95%)

---

## Development Environment Setup

### Required Environment Variables
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
# Add others as needed
```

### Recommended Tools
- Python 3.10+
- Chrome/Chromium browser
- Git
- IDE with Python support (VS Code, PyCharm)
- pytest for testing
- black for code formatting
- pylint for linting

---

## Session History

### Session 2025-01-24: Brutal Code Analysis + Cursor Implementation Review
- **Duration:** ~3-4 hours
- **Rating Change:** 3.0/10 → 6.5/10
- **Issues Fixed:** 7/10
- **Key Achievement:** Systematic identification and resolution of critical issues
- **Remaining Work:** Email header injection, legacy cleanup, testing

---

## Important Notes

1. **NEVER commit secrets** - Always use environment variables or .env files (gitignored)
2. **ALWAYS sanitize user input** - Especially in email, SQL, command execution contexts
3. **VERIFY Cursor claims** - AI tools can hallucinate completion, always verify integration
4. **TEST security fixes** - Use malicious input to verify protection works
5. **DOCUMENT security decisions** - Future developers need to understand why

---

*Last Updated: 2025-01-24*
*Next Session Priority: Fix email header injection vulnerability*
*GCP Project: my-project-3445-1696278622939*
