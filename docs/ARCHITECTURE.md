# Architecture and implementation plan

Empty repository inspected on 2026-09-10. There is no existing application to preserve.

## Decisions
A single Java 21 Spring Boot service serves a versioned-in-source REST contract under /api. A React/TypeScript/Vite SPA proxies /api in development; production uses a same-origin reverse proxy. PostgreSQL is authoritative, with Flyway migrations and Hibernate validate. No Docker required. H2 in PostgreSQL mode is used only for fast tests. Production never seeds demo accounts. Sites hosting was evaluated: its Workers runtime cannot execute Java, so the required stack takes precedence; deployment needs a Java host and PostgreSQL.

Session authentication uses BCrypt, an HttpOnly SameSite cookie, server-side session expiry, CSRF protection, and session fixation protection. Sessions are intentionally single-instance; use Spring Session before horizontal scaling. A public signup may create STUDENT or an unapproved CLUB organization; ADMIN cannot self-register.

## Domain
User 1:0..1 Club (owner); User 1:many Membership many:1 Club; Club 1:many Event; User 1:many Registration many:1 Event; Registration 1:many Payment. Unique emails, club/event slugs, student-event registrations, student-club memberships. Money is integer paise, INR. Dates are UTC instants; clients display local time. Club membership is immediate JOINED with an extensible state column.

Event lifecycle: DRAFT → PUBLISHED → CANCELLED or COMPLETED. Published events can be edited before start with registration-safe constraints; cancellation refunds confirmed development payments and invalidates registrations. Events are retained for history. Availability derives from lifecycle, dates, deadline, and active registrations. Pending payment holds expire after 15 minutes. Every registration/payment/cancellation mutation locks the event row before reading capacity; database uniqueness provides the second barrier. Event ownership is checked in the service.

## API contract
JSON errors: {message, fields?}. 400 invalid; 401 unauthenticated; 403 forbidden; 404 missing; 409 business conflict; 429 rate limit. Lists use {items,page,size,total,totalPages}, bounded to 60. DTOs do not expose entities.

Public: GET /api/auth/csrf, GET /api/auth/me, POST /api/auth/signup, POST /api/auth/login, POST /api/auth/logout, POST /api/auth/forgot-password, POST /api/auth/reset-password; GET /api/events?q=&category=&price=&when=&sort=&page=; GET /api/events/{slug}; GET /api/clubs; GET /api/clubs/{slug}.
Student: GET/PUT /api/profile; GET /api/memberships; POST/DELETE /api/clubs/{id}/membership; GET /api/registrations; POST /api/events/{id}/registrations; DELETE /api/registrations/{id}; POST /api/registrations/{id}/payment (development only, outcome SUCCESS or FAILED).
Club: GET/PUT /api/club/profile; GET/POST /api/club/events; GET/PUT /api/club/events/{id}; POST /api/club/events/{id}/publish; POST /api/club/events/{id}/cancel; GET /api/club/events/{id}/registrations; GET /api/club/events/{id}/export.
Admin: GET /api/admin/summary; GET /api/admin/clubs, /events, /users; PATCH /api/admin/clubs/{id} with APPROVED/REJECTED; POST /api/admin/events/{id}/cancel.

## Order
1. Foundation/docs/schema/auth. 2. Club and event operations. 3. Discovery/detail UI. 4. Membership/registration/payments. 5. Role dashboards/admin/export. 6. Responsive/accessibility refinement. 7. Integration/adversarial/browser checks, builds, and handoff.

## Risks
Final-slot races: serialize on event row in PostgreSQL. Mock payment abuse: profile/config gate; production startup fails with mock enabled. Account takeover: BCrypt, expiring one-use reset tokens stored hashed, login throttling, session revocation on password reset. Oversharing: DTOs and owner-gated registrants/exports. CSV injection: prefix formula-like cells. External media: HTTPS URL selection only, no server-side fetch; no arbitrary upload pipeline. No invented SMTP/payment credentials.

## Final implementation refinements

V2 adds administrative event visibility. POST /api/admin/events/{id}/hide removes the public page; upcoming bookings are cancelled/refunded while history remains. GET /api/config exposes only development/payment capability flags. GET /api/events/{id}/registration and GET /api/clubs/{id}/membership return the authenticated student's state without scanning a paginated list. GET /api/registrations?when=upcoming|past|all filters on the server.

Club decisions/profile edits use row locks; booking/publishing take a shared club lock while checking approval. Profile updates lock the user row to avoid overwriting an auth-version change from password recovery. Registration lists batch students, events, organizers, seat counts and payments. Club lists batch membership counts. Pending hold expiry is capped by the registration deadline.

Production is the default profile. APP_ADMIN_EMAIL / APP_ADMIN_PASSWORD provide one-time, server-only administrator provisioning; an existing non-admin email is never promoted. Development/test profile checks prohibit demo seed or mock payment activation in production. Local runtime and test launchers copy the built JAR before starting, protecting live class loading from subsequent builds.
