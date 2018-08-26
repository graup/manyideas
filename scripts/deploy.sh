ssh graup@ssh.pythonanywhere.com /bin/bash -l << EOF
  cd ~/thesis-experiment/thesis-experiment/backend/
  workon backend
  echo "Updating code..."
  git pull
  echo "Updating packages..."
  pip install -r requirements.txt -q
  DJANGO_SETTINGS_MODULE='config.settings.test' python manage.py test
  python manage.py collectstatic --noinput
  python manage.py migrate
EOF