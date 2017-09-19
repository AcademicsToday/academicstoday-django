# Developer Notes:
Here are the libraries that this project utilizes, please update this list as
new libraries get added.

```bash
pip install django                       # Our MVC Framework
pip install Pillow                       # Req: ImageField
pip install python-dotenv                # Environment Variables
pip install psycopg2                     # Postgres SQL ODBC
pip install djangorestframework          # RESTful API Endpoint Generator
pip install django_filter                # Filter querysets dynamically
pip install django-crispy-forms          #
pip install django-cors-headers          # Allow External Cors Headers
pip install gunicorn                     # Web-Server Helper
pip install django-tenants               # Multi-Tenancy Handler
pip install django-rq                    # Redis Queue Library
pip install rq-scheduler                 # Redis Queue Scheduler Library
pip install django-anymail[mailgun]       # Developer Mail Service
```

And run this command to save:

```
pip freeze > requirements.txt
```


## MacOS Libraries

Read https://gis.stackexchange.com/a/229941
```bash
brew tap osgeo/osgeo4mac
brew install gdal2
pip3 install gdal
```

```bash
brew install jpeg
```
