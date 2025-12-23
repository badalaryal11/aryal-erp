---
description: How to deploy changes to PythonAnywhere
---

1. Log in to your [PythonAnywhere Dashboard](https://www.pythonanywhere.com/).
2. Open a **Bash** console.
3. Navigate to your project directory (adjust path if necessary):
   ```bash
   cd ~/aryal-erp
   ```
4. Pull the latest changes from GitHub:
   ```bash
   git pull origin main
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```
7. Reload the web app:
   - Go to the **Web** tab.
   - Click the green **Reload** button.
