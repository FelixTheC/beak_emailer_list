while true
do
  now=$(date +"%s")
  next_job=$(python manage.py run_schedule)
  waiting_seconds=$((next_job-now))
  echo "$(date): the next job process will start in $waiting_seconds seconds"

  sleep $waiting_seconds || sleep 10m
done