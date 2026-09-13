# Connect
A Django-based student/teacher management system with CRUD, authentication,
search/filter/sort, and permission-based access control.

## Setup
1. Clone the repo and create a virtual environment:
python -m venv venv
.\venv\scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Copy `.env.example` to `.env`, then generate a secret key and paste it in:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Paste the output as the value of `DJANGO_SECRET_KEY` in your `.env` file.

4. Run migrations:
python manage.py migrate

5. Create a superuser (for admin access and initial permissions):
python manage.py createsuperuser

6. Run the development server:
python manage.py runserver

## Notes
- If you get locked out during login testing, run `python manage.py axes_reset`
  to clear failed-attempt lockouts.
- Run tests with `python manage.py test`.
