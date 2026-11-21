# Connect

A Django-based student and teacher management system with CRUD, login and logout, search, filter and sort, and permission-based access control.

## Features

- Create, view, update and delete students and teachers
- Search by name, ID, subject or email, filter by subject, sort, and paginate (5 per page)
- Permission-based access: each action (view, add, change, delete) needs its own Django permission
- "My details" page for the logged-in student or teacher
- About page with student and teacher counts by subject
- Login lockout after 5 failed attempts (django-axes)
- Custom 403, 404 and 500 error pages

## Setup

1. Clone the repo and create a virtual environment: `python3 -m venv venv` then `source venv/bin/activate` (on Windows: `.\venv\Scripts\activate`)

2. Install dependencies: `pip install -r requirements.txt`

3. Copy `.env.example` to `.env`, then generate a secret key and paste it in as the value of `DJANGO_SECRET_KEY`: `python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

4. Run migrations: `python3 manage.py migrate`

5. Create a superuser (for admin access and initial permissions): `python3 manage.py createsuperuser`

6. Run the development server: `python3 manage.py runserver`

7. Open `http://127.0.0.1:8000/connect/login/` and log in.

## Notes

- If you get locked out during login testing, run `python3 manage.py axes_reset` to clear failed-attempt lockouts.
- Run tests with `python3 manage.py test`.
