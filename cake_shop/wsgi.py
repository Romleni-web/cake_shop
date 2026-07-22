import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cake_shop.settings')
application = get_wsgi_application()

# Run migrations automatically on Vercel startup if they haven't run
if os.getenv('VERCEL') == '1':
    from django.core.management import execute_from_command_line
    try:
        # This is a bit slow but ensures the DB is ready
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        execute_from_command_line(['manage.py', 'seed_data'])
    except Exception as e:
        print(f"Migration error: {e}")

app = application
