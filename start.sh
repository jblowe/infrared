while true; do
  nohup python app.py  >> server.log 2>&1
  echo "$(date): server crashed. Restarting in 5s..." >> server.log
  sleep 5
done
