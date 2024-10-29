# Ecommerce api

Implement ecommerce api, just backend apis

## Run

- Run `chmod +x entrypoint.sh` to make `entrypoint.sh` can be executable.
- `docker compose up -d` to run containers and go to `127.0.0.1:8000` to test all apis.
- `docker compose exec web python manage.py createsuperuser` to create `admin`
- `docker compose exec db psql --username={dbusername} --dbname={databasename}` to interact with database.

## Tasks to complete

- [x] Build comment feature to rating products.
- [ ] Add zalopay to payment method.
- [ ] Build front-end.
- [ ] Build chat service.
