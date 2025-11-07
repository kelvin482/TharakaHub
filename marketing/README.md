# Marketing App (Plug-and-Play)

This app adds a small "Marketing Marketplace" to your Django project without touching existing apps `jobs` or `users`.

## Quick Setup

1) Create DB tables:

```bash
python manage.py makemigrations marketing
python manage.py migrate
```

2) Enable the app (paste into `simple_backend/settings.py` near other INSTALLED_APPS entries):

```py
# in simple_backend/settings.py, inside INSTALLED_APPS:
INSTALLED_APPS += [
    'marketing',
]
```

3) Wire URLs (paste into `simple_backend/urls.py`):

```py
from django.urls import include, path

urlpatterns += [
    path('marketing/', include('marketing.urls', namespace='marketing')),
]
```

4) Run:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/marketing/`.

5) Create a test user:

```bash
python manage.py createsuperuser
# or
python manage.py shell -c "from django.contrib.auth import get_user_model;User=get_user_model();User.objects.create_user('demo','', 'demo')"
```

## What It Includes

- Models: `Category`, `MarketingJob`, `Proposal`, `Message`, `AnalyticsEvent` (see `marketing/models.py`).
- Forms: `JobForm`, `ProposalForm` (see `marketing/forms.py`).
- Views & URLs: listing, detail, create job, create proposal (AJAX-friendly), dashboard (see `marketing/views.py`, `marketing/urls.py`).
- Templates: under `marketing/templates/marketing/` only. No changes to `users`/`jobs` templates.
- Static: under `marketing/static/marketing/` only (CSS + JS).
- Admin registry with useful filters and search.

## AI Service Placeholder

Replace `marketing/services/ai.py::classify_job_text` with a real OpenAI call if desired:

```py
import os, openai
openai.api_key = os.environ['OPENAI_API_KEY']
# resp = openai.chat.completions.create(...)
# return resp.choices[0].message.content.strip()
```

Keep your key in an environment variable (e.g., `.env`, system env). Be mindful of cost and rate limits.

## Notes

- The app is self-contained. It does not modify `jobs` or `users` files.
- All templates live in `marketing/templates/marketing`; all static files live in `marketing/static/marketing`.
- One JSON endpoint exists for AJAX proposals: `POST /marketing/jobs/<pk>/proposal/` returns `{ok:true, proposal_id}` or errors.

## Minimal Navigation

- List: `/marketing/` or `/marketing/jobs/`
- Create: `/marketing/jobs/create/`
- Detail: `/marketing/jobs/<id>/`
- Dashboard: `/marketing/dashboard/`

Happy shipping!


