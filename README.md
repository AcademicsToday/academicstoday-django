![alt tag](https://github.com/AcademicsToday/academicstoday-django/blob/master/docs/media/logo.png)
# academicstoday-django
## Description
A open-source platform for online course-based learning and education.

## Features
* Students log in and enroll in the provided courses
* Watch educational online videos lectures for courses
* Fill out quizzes tests and assignments to get graded on
* Earn certificates of completion of courses

## System Requirements
* Python 3.6.x+
* Postgres SQL DB 9.6+

## Dependencies
See [requirements.txt](https://github.com/AcademicsToday/py-academicstoday/blob/master/requirements.txt) for more information.

## Build Instructions
### Application
For Linux and OSX users, run these commands:

1. First clone the project locally and then go into the directory
  ```
  $ git clone https://github.com/AcademicsToday/academicstoday-django;
  $ cd academicstoday-django;
  ```

2. Setup our virtual environment
  ```
  $ virtualenv -p python3.6 env
  ```

3. Now lets activate virtual environment
  ```
  $ source env/bin/activate
  ```

4. Now lets install the libraries this project depends on.
  ```
  $ pip install -r requirements.txt
  ```

### Database
We are almost done! Just follow these instructions and the database will be setup for the application to use.

#### MacOS Database
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

#### Ubuntu Database
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

#### CentOS 7 Database:

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

### Application + Database
Run the following command to create your custom settings instance. Note: Please write all your application passwords here as it won't be tracked on git.

  ```
  $ cd academicstodayacademicstoday
  $ cp secret_settings_example.py secret_settings.py
  ```

Run the following commands to populate the database.
  ```
  cd ../academicstoday;
  python manage.py makemigrations;
  python manage.py migrate_schemas;
  python manage.py populate_public;
  python manage.py setup_fixtures;
  python manage.py populate_site;
  ```

Update your hosts file to support our applications domain.
  ```
  sudo vi /etc/hosts
  ```

  Append to the file...
  ```
  127.0.0.1       academicstoday.com
  127.0.0.1       academicstoday.ca
  ```


  refresh
  ```
  dscacheutil -flushcache
  ```


## Usage
To run the web-app, you’ll need to run the server instance and access the page from your browser.

Start up the web-server:
  ```
  $ sudo ./manage.py runserver academicstoday.ca:80
  ```

In your web-browser, load up the following url
  ```
  http://academicstoday.ca/
  ```

Congratulations, you are all setup to run the web-app! Have fun coding!

## License
This web-app is licensed under the Apache 2.0 license. See [LICENSE.md](LICENSE.md) for more information.

## Developers
* Bartlomiej Mika
* Michael Murray
* Sebastian Rydzewski
