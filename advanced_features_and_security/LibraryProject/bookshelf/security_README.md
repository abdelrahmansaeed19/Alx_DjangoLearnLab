# Django Security Measures

## ✅ Settings

- `DEBUG = False`: Disables detailed error pages in production.
- `SECURE_BROWSER_XSS_FILTER`: Adds X-XSS-Protection header.
- `SECURE_CONTENT_TYPE_NOSNIFF`: Prevents MIME sniffing.
- `X_FRAME_OPTIONS = 'DENY'`: Protects against clickjacking.
- `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`: Forces cookies over HTTPS.

## ✅ Templates

- All forms use `{% csrf_token %}` for CSRF protection.

## ✅ Views

- Use Django ORM for all database queries.
- Forms use `is_valid()` to sanitize inputs.

## ✅ CSP (Content Security Policy)

- Added via `django-csp`.
- Default content loading is restricted to `'self'`.

## ✅ Testing Checklist

- ❏ Attempt form submission without CSRF token → should raise 403.
- ❏ Try injecting `<script>` in input → should be escaped.
- ❏ Try SQL injection (`' OR 1=1 --`) → should be ignored or cause validation error.
- ❏ View CSP headers in browser → ensure they’re present.
