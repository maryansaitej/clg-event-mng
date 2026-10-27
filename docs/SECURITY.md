# Security
Enforce all roles and ownership server-side. Email is normalized, passwords BCrypt-hashed, signup cannot choose ADMIN. HttpOnly SameSite=Lax session cookies; Secure in production. CSRF tokens are required on every mutation, including login/logout. Sessions expire after 8 hours of inactivity and are rotated on login. Reset tokens expire after 30 minutes, are stored SHA-256 hashed and consumed once; account authVersion invalidates existing sessions after reset. User-facing errors omit SQL/stack traces.

A bounded per-IP sliding window protects auth endpoints; a production reverse proxy must enforce request limits and trusted forwarding. All forms validate length/format and temporal/monetary constraints. Description text renders escaped by React. HTTPS image and social URLs only. No card data, client-set prices, or client-success in production. Development checkout is an explicit provider simulation only. Production fails closed unless a real provider is installed; free events remain supported when payments are disabled.

Database row locks and uniqueness guard registrations; all seat-mutating paths take locks in consistent order. Capacity counts confirmed registrations plus unexpired pending holds. Club/event cancellation revokes active bookings and records development refunds. CSV escapes formula-like values and quotes cells. Production requires TLS, private database access, backups, platform logging/monitoring, and configured email delivery.

Reference: https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html

## Final hardening

Administrative hiding is distinct from cancellation and removes public access to the content. Profile and club updates serialize with security-sensitive changes so they cannot restore an old auth version or club approval state. Deserialization rejects unknown fields and fractional values for integer amounts/capacities. Hold expiry never extends beyond the registration deadline. HTML descriptions are plain text; broken poster links reveal a typographic fallback.

Administrator bootstrap is an opt-in server environment operation. It requires a validated email and 12–72 character password, hashes the password, refuses role promotion, and never rewrites an existing administrator's credentials. Remove bootstrap variables after first deployment. College ID, department and year are self-reported; institutions needing verified eligibility must connect an authoritative student directory.
