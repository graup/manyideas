ssh graup@ssh.pythonanywhere.com /bin/bash -l <<'EOF'
  source ~/thesis-experiment/.env
  mkdir -p ~/backup
  cd ~/backup
  echo "Backing up $MYSQL_USER@$MYSQL_HOST:$MYSQL_DB to $(date "+%Y_%m_%d__%H_%M").sql ..."
  MYSQL_PWD=$MYSQL_PASSWORD mysqldump -h "$MYSQL_HOST" -u "$MYSQL_USER" "$MYSQL_DB" > $(date "+%Y_%m_%d__%H_%M").sql;
  echo "done";

EOF
