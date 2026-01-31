import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
django.setup()

from django.contrib.auth.models import User

# Change these to whatever you want your "Boss" account to be
username = 'Hemja_boss'
password = 'SecretPassword123' 

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, '', password)
    print(f"Successfully created superuser: {username}")
else:
    # If the user exists, we will just reset the password to be sure
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Updated credentials for: {username}")