# Quick Project Restart Instructions
## MacOS Database
Let us setup our database:

  ```sql
  drop database academicstoday_db;
  create database academicstoday_db;
  \c academicstoday_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE academicstoday_db to django;
  ALTER USER django CREATEDB;
  ALTER ROLE django SUPERUSER;
  -- CREATE EXTENSION postgis;
  ```

## Ubuntu Database
Let us setup our database:

  ```sql
  sudo -i -u postgres
  psql

  DROP DATABASE academicstoday_db;
  CREATE DATABASE academicstoday_db;
  \c academicstoday_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE academicstoday_db to django;
  ALTER USER django CREATEDB;
  -- ALTER ROLE django SUPERUSER;
  -- CREATE EXTENSION postgis;
  ```

## CentOS 7 Database:

  ```sql
  sudo -i -u postgres;
  dropdb academicstoday_db;
  createdb academicstoday_db;
  psql academicstoday_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE academicstoday_db to django;
  ALTER USER django CREATEDB;
  ALTER ROLE django SUPERUSER;
  -- CREATE EXTENSION postgis;
  ```

## Restart Script
The following instructions can be used to restart AT without any sample data.
These instructions are recommended for production environments.

Just copy and paste this into your command console.

```bash
python manage.py makemigrations; \
python manage.py migrate_schemas; \
python manage.py populate_public; \
python manage.py setup_fixtures; \
python manage.py populate_site;
```
