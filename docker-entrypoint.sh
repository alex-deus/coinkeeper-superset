#!/usr/bin/env bash

args=("$@")

case "${1}" in
    "bash")
        shift
        exec bash -c "${args[@]:1}"
        ;;
    "wait")
        exec bash -c "while true; do sleep 20; done"
        ;;
    "debug")
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    "run")
            exec gunicorn project.wsgi:application \
              --workers ${GUNICORN_WORKERS:-2} \
              --timeout ${GUNICORN_TIMEOUT:-120} \
              --log-level=${GUNICORN_LOG_LEVEL:-info} \
              --bind=${GUNICORN_BIND:-0.0.0.0:8000} \
              --log-config gunicorn_log.conf
            ;;
    "manage")
        shift
        exec ./manage.py ${args[@]:1}
        ;;
esac
