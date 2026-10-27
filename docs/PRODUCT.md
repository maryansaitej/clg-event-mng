# Campus Commons
A fictional college's shared calendar and club directory. Students discover, join, register, and manage commitments. Clubs apply for approval, maintain identity, publish events, and manage attendance. Administrators approve organizations and moderate events.

## Screens
/ and /events: content-first discovery with category, free/paid, date, search and sort. /events/:slug: poster, organizer, schedule, rules, eligibility, deadline and registration. /clubs and /clubs/:slug: directory, membership and events. /login, /register, /forgot-password, /reset-password: account flows.
/app: upcoming commitments and joined clubs. /app/registrations, /app/clubs, /app/profile: personal workspace.
/club: overview, drafts and upcoming events. /club/events, /club/events/new, /club/events/:id/edit, /club/events/:id/registrations, /club/profile: organization workspace.
/admin with clubs/events/users sections: approvals and moderation.

## Policies
Students alone register and join clubs. Clubs cannot publish until approved. Free registration immediately confirms; paid registration holds a seat for 15 minutes and confirms after a server-owned provider result. Registration cancellation is allowed until the event starts when the organizer enables it; development payments are refunded. Capacity cannot be reduced below occupied seats; the price is frozen once registrations exist. Email/password recovery has a local development inbox; production requires configured mail delivery. Demo data is clearly fictional and limited to development.

Administrators can hide an event independently of retaining its historical record. Hidden events disappear from public discovery and detail pages; upcoming registrations are cancelled and simulated payments refunded. Club rejection suppresses the club's public presence and publishing. Students can leave a joined club from their own workspace even when its public page is unavailable.
