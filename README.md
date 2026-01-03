- init
```shell
cp .docker/web/.env.debug .docker/web/.env
cp .docker/superset/.env.debug .docker/superset/.env
docker compose -f .docker/compose.yml up -d --build
docker compose -f .docker/compose.yml exec web ./manage.py migrate
docker compose -f .docker/compose.yml exec web ./manage.py create_super_user
docker compose -f .docker/compose.yml exec pg bash -c "psql -d $POSTGRES_DB -U $POSTGRES_USER < /tmp/schema.sql"
```
- import data
  - export from mobile app
  - put file to ./rows.csv
  - execute `docker compose -f .docker/compose.yml exec web ./manage.py import_transactions`

- open [localhost:8000/admin/](http://localhost:8000/admin/) and sing-in as **admin**:**admin**
- open [localhost:8088](http://localhost:8088/) and sing-in as **admin**:**admin**
