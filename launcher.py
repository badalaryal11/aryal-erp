import os
import sys
import time
import webbrowser
import threading
from django.core.management import execute_from_command_line

def open_browser():
    """Wait a moment for the server to start, then open the browser."""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    # Set the settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Run migrations to ensure the DB (possibly in ~/.aryal-erp) is ready
    print("Checking database...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
    except Exception as e:
        print(f"Migration error (might be ignored if just checking): {e}")

    # Start the browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start the Django server
    # --noreload is important for PyInstaller apps to avoid spawning subprocesses that crash
    print("Starting server...")
    execute_from_command_line(['manage.py', 'runserver', '--noreload'])
