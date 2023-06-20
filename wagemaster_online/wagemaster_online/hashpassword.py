import os
import sys

# Add the project directory to the sys.path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wagemaster_online.settings")

# Import and initialize Django
import django

django.setup()

from django.contrib.auth.hashers import make_password

password = "Temp.2023"
hashed_password = make_password(password)
print(hashed_password)

