# Verification

Verified locally on 10 September 2026 with Java 21, PostgreSQL 17, Node 22 and Chromium.

| Check | Result |
|---|---|
| Spring integration suite, H2 PostgreSQL mode | 23 passed |
| Same integration suite, PostgreSQL 17 | 23 passed |
| Frontend business logic and accessible components | 16 passed |
| Playwright full-stack workflows | 8 passed |
| ESLint and TypeScript | Passed |
| Prettier and Google Java Format | Passed |
| React production build | Passed |
| Executable Spring Boot JAR | Passed |
| Flyway V1 and V2 / Hibernate validate | Passed on H2 and PostgreSQL |
| Phone / tablet / desktop | 390, 768 and 1440px checked |
| Automated WCAG 2 A/AA + WCAG 2.1 AA checks | No serious or critical findings on tested screens |

Run `./scripts/check.sh`, `./scripts/test-postgres.sh`, and `./scripts/test-browser.sh` from the root. Browser tests start their own Java API and Vite server on ports 8082/5174, with a separate `campus_commons_e2e` database. They use the latest packaged JAR, so run check.sh before test-browser.sh. Generated test registrations/accounts are isolated from the normal preview. Test-created published events are hidden and test clubs rejected after the relevant workflow.

## Behaviors covered

- Real SecurityFilterChain, session creation/rotation, CSRF on login and mutations, logout, wrong credentials and anonymous access.
- Signup rejects ADMIN escalation; clubs begin pending; hashes never appear in response DTOs.
- Students cannot access club/admin resources; clubs cannot read, edit, cancel, export or inspect another organizer's event registrations.
- Draft privacy, approval-gated publishing, invalid fees/capacity/dates, malformed dates and unexpected request fields.
- Free registration bypasses payments; duplicate registrations fail; six concurrent students contend for one seat and exactly one succeeds.
- Closed/cancelled events and eligibility violations reject registration; expired holds free seats and cannot be paid.
- Paid holds, failure/retry, server-set amount, idempotent success, ownership, cancellation/refunds and event cancellation.
- Admin hiding removes the public page and refunds upcoming development bookings.
- Membership join/leave is idempotent and student-only.
- Reset links are one-use and revoke prior sessions; production cannot activate the development payment provider.
- Capacity and price are protected after booking; CSV neutralizes spreadsheet formulas.
- Browser student signup/login, profile persistence, search/filter/empty states, event detail, free/paid registration, join/leave, cancellation/refund, club preview/draft/publish/export and admin approval.
- Nested-route refresh, missing event, unauthenticated protected navigation, backend failure, mobile menu, desktop/tablet/phone overflow and automated accessibility scans.

## Review and repairs

Verification found and fixed an authentication cache-observer problem after login, repository access through a Spring proxy, malformed definition-list semantics, helper text included in accessible field names, stale registration reads before locks, oversized title wrapping, mobile filter truncation, and build-output files inadvertently included in lint. Registration and club lists now batch related data. Running servers use copied JARs so a later build cannot overwrite their class-loading source.

Public screens and event details received screenshot review. Forms use explicit labels with separate descriptions/errors, visible keyboard focus, semantic controls and Radix confirmation/preview dialogs. Reduced-motion is respected. Screenshots and traces are in frontend/test-results and frontend/playwright-report, excluded from Git.

## Performance evidence and limits

The complete production frontend is approximately 560 KB uncompressed across route chunks; the main browser bundle is about 105 KB gzipped plus about 8 KB CSS. Forms/validation and workspace screens load separately. The executable JAR is about 57 MB. Local Vite startup was under a second; the Java API started in roughly four seconds, excluding first-run dependencies and BCrypt seed creation. The development launcher caps JVM heap at 384 MB and the database pool at eight connections.

These measurements are from this machine, not a load-test guarantee. Chromium automation and targeted axe scans do not replace manual assistive-technology testing. External SMTP, live payment webhooks/refunds, TLS hosting, backups, campus identity verification and multi-instance session storage require deployment infrastructure and were not claimed as verified. There is no real payment adapter enabled in production.
