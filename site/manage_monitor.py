import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from main.file_monitor import start_monitoring

if __name__ == "__main__":
    start_monitoring()
