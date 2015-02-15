# academicstoday-webapp
## Description
A open-source platform for online course-based learning and education.

## Support
You can financially support the project by either:
* direct donation: 1NdWWNyHJJd5oFhtzAFtApNaHjSuAbGmXZ

## Features
* Students log in and enrol in the provided courses
* Watch educational online videos lectures for courses
* Fill out quizzes tests and assignments to get graded on
* Earn certificates of completion of courses

## System Requirements
* Python 3.4.x
* Postgres SQL DB 9.4
* pip 1.5.x

## Dependencies
* Django 1.7.4
* psycogp2 2.6

## Build Instructions
### Application
For Linux and OSX users, run these commands:

1. First clone the project locally and then go into the directory
  ```
  $ git clone https://github.com/AcademicsToday/academicstoday-webapp.git 
  $ cd academicstoday-webapp
  ```

2. Setup our virtual environment
  ```
  (OSX)
  $ python3 -m venv env

  (Linux)
  $ virtualenv env
  ```

3. Now lets activate virtual environment
  ```
  $ source env/bin/activate
  ```

4. OSX USERS ONLY: If you are using ‘Postgres.app’, you’ll need to have pg_config setup in your $PATH. If you already have set this up, skip this step, else simply run this command in the console to set the path manually.

  ```
  $ export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
  ```

5. Now lets install the libraries this project depends on.
  ```
  $ pip install -r requirements.txt
  ```

### Database
We are almost done! Just follow these instructions and the database will be setup for the application to use.

1. Load up your postgres and enter the console. Then to create our database, enter:
  ```
  # create database academicstoday_db;
  ```

2. To confirm it was created, run this line, you should see the database in the output
  ```
  # \l
  ```

3. Enter the database
  ```
  # \c academicstoday_db
  ```

4. If you haven’t created an administrator for your previous projects, create one now by entering:
  ```
  # CREATE USER bart WITH PASSWORD '123password';
  # GRANT ALL PRIVILEGES ON DATABASE academicstoday_db to bart;
  ```

5. Your database "academicstoday_db" is now setup with an admin user account "bart" using the passowrd "123password”. 

### Application + Database
Run the following commands to populate the database.
  ```
  $ cd academicstoday_project
  $ python manage.py makemigrations
  $ python manage.py migrate 
  ```

Finally, we just need to populate the database with initial content and we’re finished! To do this, look into the file ***scripts/initalization.sql*** file and run this script. You are now ready!


## Usage
To run the web-app, you’ll need to run the server instance and access the page from your browser. 

Start up the web-server:
  ```
  $ cd academicstoday_project
  $ python manage.py runserver
  ```

In your web-browser, load up the following url
  ```
  http://127.0.0.1:8000/
  ```

Congratulations, you are all setup to run the web-app! Have fun coding!

## License
This web-app is licensed under the Apache 2.0 license. See [LICENSE.md](LICENSE.md) for more information.

## Developers
* Bartlomiej Mika
* Michael Murray
* Sebastian Rydzewski
