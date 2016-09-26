# Installation and setup

these are instructions on how to set up everything not included in the git project


in mysql run the following
CREATE DATABASE db_JamesLi Character Set UTF8;
CREATE USER dev@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON db_JamesLi.* TO dev@localhost;
FLUSH PRIVILEGES;

> To start the server if it doesn't autostart
> run:
> sudo /etc/init.d/mysql start

run 'pip install django-extensions' which is required for something

in urls         add     url(r'^', include('db.urls', namespace='db')),
in settings.py  add     'db','django_extensions',
                change DATABASES to match the following
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_JamesLi',
        'USER': 'dev',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}


run python manage.py makemigrations
python manage.py migrate

create a superuser
for now I've been using 
russell
passwordpassword