# TharakaHub – Django Project Overview

This repository contains a small Django application with two apps: `users` (accounts, dashboard and navigation) and `jobs` (job/assignment posting and applications). It uses SQLite by default and Django templates for the UI. This doc explains the structure and the data flow so you can navigate or extend the project safely without changing current behavior.

## Project Layout

```
simple_backend/
├── manage.py
├── db.sqlite3                         # SQLite database
├── media/                              # uploaded user files (if any)
├── static/                             # static assets collected/served in dev
├── simple_backend/                     # root settings/urls/wsgi
├── jobs/                               # job posting + applications
└── users/                              # auth, dashboard, pages, assets
```

## Core Concepts and Data Models

- `jobs.models.Job`
  - Fields: `poster`, `assignee`, `title`, `description`, `department`, `unit`, `price`, `deadline`, `status`, `is_active`, timestamps
  - Status choices: `POSTED`, `IN_PROGRESS`, `COMPLETED`, `ARCHIVED`
- `jobs.models.Application`
  - Links a `User` applicant to a `Job`
  - Status choices: `PENDING`, `ACCEPTED`, `DECLINED`
  - Uniqueness: a user can apply to a job only once (`unique_together`)

Notes:
- In the UI, “Active” in the dashboard corresponds to `Application.status == ACCEPTED`. Code maps this label without changing the stored values.

## URLs at a Glance

- Users app
  - `/users/` → Home
  - `/users/dashboard/` → Main dashboard (applications overview + incoming applications)
  - `/users/projects/` and `/users/dashboard/projects/` → Projects view (derived from jobs)
  - `/users/dashboard/clients/` → Clients aggregated from jobs you’re assigned to
  - `/users/messages/` → Lightweight inbox built from `Application` rows
  - `/users/earnings/` → Earnings summary derived from assigned jobs
  - `/users/portfolio/` → Completed jobs as portfolio items
  - Auth: `/users/login/`, `/users/register/`, `/users/logout/`
- Jobs app
  - `/jobs/` → Job list (grouped by department)
  - `/jobs/<pk>/` → Job detail
  - `/jobs/<job_id>/apply/` → Apply to a job (POST only)
  - `/jobs/application/<app_id>/<new_status>/` → Change application status (job poster only)

## How Key Flows Work

### A) Posting and Applying to Jobs
1. A logged-in user creates a job at `/jobs/create/` (view: `jobs.views.create_job`).
2. Another user opens the job detail and applies via POST to `/jobs/<job_id>/apply/` (`jobs.views.apply_job`). Duplicate applications are prevented.
3. The job poster sees incoming applications on their dashboard. They can Accept/Decline using the route above, which updates `Application.status`.

### B) Dashboard – Applications Section
- `users.views.dashboard` aggregates your applications:
  - Counts by status using SQL `GROUP BY`
  - Maps `ACCEPTED → ACTIVE` for display
  - Supplies `incoming_applications` (applications to jobs you posted)

Template `users/templates/users/dashboard.html` renders:
- Your Applications (Pending, Active, Declined)
- Incoming Applications (Accept/Decline buttons visible only while `PENDING`)

### C) Projects View (Derived from Jobs)
- `users.views.projects` loads jobs where you are `poster` or `assignee` and maps job `status` to a simple progress for the UI. It renders `users/dashboardfiles/projects.html` with a `projects` list shaped like: `{ title, description, progress, status }`.

### D) Clients View
- `users.views.clients_view` groups assigned jobs by their `poster` to build a clients list with minimal fields (name, email, phone, company, jobs list). It renders `users/dashboardfiles/clients.html`.

### E) Messages View (Lightweight Inbox)
- `users.views.messages_view` creates an in-memory inbox from `Application` rows involving the current user (as applicant or job poster). This avoids new tables while providing a functional sidebar list of conversations for the template.

### F) Earnings View
- `users.views.earnings` computes basic totals from your assigned jobs:
  - Completed jobs this month → `total_earnings_month`
  - Posted/In progress → `pending_payments`
  - All completed minus withdrawals (assumed `0`) → `available_balance`
  - Recent jobs power the transactions table. The template shows charts using static demo data (safe to keep as-is).

### G) Portfolio View
- `users.views.portfolio` exposes recently completed assigned jobs as `portfolio` items; the template displays them in a grid.

## Templates & Styling

- Global layout: `users/templates/users/base.html` provides the nav bar, footer, and loads `users/static/users/css/style.css` and page-specific CSS.
- Dashboard styles live in `users/static/users/css/dashboard.css`. Accept/Decline buttons use modern, scoped classes like `.btn.pill.accept` and `.btn.pill.decline` to avoid conflicts.
- Jobs listing and detail templates live under `jobs/templates/jobs/`.

## Permissions & Safety Checks

- Most dashboard and job actions are guarded by `@login_required`.
- Application status changes verify that the current user is the `job.poster` and reject unauthorized attempts.
- Duplicate applications are prevented with `get_or_create` and a database `unique_together` constraint.

## Local Development

1. Create and activate a virtual environment; install dependencies.
2. Run migrations (already applied if `db.sqlite3` exists):
   ```bash
   python manage.py migrate
   ```
3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```
5. Visit:
   - `http://127.0.0.1:8000/users/dashboard/`
   - `http://127.0.0.1:8000/jobs/`

## Notes on Status Labels

- Application statuses stored: `PENDING`, `ACCEPTED`, `DECLINED`.
- Dashboard label “Active” is a display alias for `ACCEPTED`. The view maps it, so templates can keep showing “Active” without changing the database.

## Extending Safely

- Add new features by composing around existing models (`Job`, `Application`).
- If you introduce new tables (e.g., Payments, Messages), keep the current pages powered by the existing lightweight derivations until the new models are wired to the templates.

This documentation is descriptive only—no functional changes were made.
