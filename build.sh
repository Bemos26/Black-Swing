#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create superuser if not exists
python ensure_superuser.py

# Populate default services
python populate_services.py

# Import manual images
python manage.py import_images
