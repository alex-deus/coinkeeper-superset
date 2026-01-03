#!/bin/bash
set -e

echo "===> Upgrading DB"
superset db upgrade

echo "===> Creating admin user"
superset fab create-admin \
  --username "$SUPERSET_ADMIN_USERNAME" \
  --firstname Admin \
  --lastname User \
  --email "$SUPERSET_ADMIN_EMAIL" \
  --password "$SUPERSET_ADMIN_PASSWORD" || true

echo "===> Initializing roles & permissions"
superset init

echo "===> Starting Superset"
superset run \
  -h 0.0.0.0 \
  -p 8088 \
  --with-threads \
  --reload
