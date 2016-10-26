# Scheme Documentation

This app is all about surveys. Giving surveys, creating surveys, filling them out. 

So there are __3__ fundamental entities. 

- People
    + People should be the datasources for this project. 
- Surveys
    + ordered groups of questions that people fill out
        * Self-Report surveys
        * Observational surveys
- Answers
    + the store of the answers provided to each question.


## Different kinds of surveys 
__Self report surveys__ are a person filling out a survey about themselves.
__Observational surveys__ are a person filling out a survey about another person. 

They differ in how the data is displayed on the _/survey_ page. When it is a self report survey the primary key is simply the respondent while observational surveys use both the respondent and the subject (i.e. the person filling out the survey and who the survey is about) as keys. Both also use the date and time submitted as an extra key to allow multiple responses to the same survey. 

Although some surveys do not allow multiple submissions. This is controlled survey to survey using the __allow_multiple_submissions__ flag in the survey entity. 

When submitting an observational survey it is always necessary to choose who is responding and who the survey referring to and that will always be required.

When submitting a self-report survey you will only have to select a respondent. However that is required. 

In both cases you will have to input when the survey was submitted.

## Question and Answer behavior
Questions come in a variety of flavors depending on what you're trying to get out of your respondents. 

> You can ask them to describe the last dream you remember. 
> where they are free to write anything they would like. 
>
> You can ask them which of the following foods would are your favorite. 
> Where they can select any number of the following foods. 
> or maybe just their top 3 choices. 
>
> You can ask to rate 1-5 or 0-10 how their day was. 
> What's more higher can mean better or worse.


This project should allow you to ask any of those questions you like. It should also store a definition of the survey. i.e. What questions were asked in the survey and why they were included. 

This is done using the following scheme. 
Surveys contain many questions in a particular order and 
Questions can belong to many surveys.

A single question is supposed to get an answer of only one datatype. i.e. _"rate your day 1-4"_ expects the answer to be an _integer from 1-4_, while _"describe your day"_ would expect a _text answer_.

But what about _"please select your top 3 favorite foods"_? Well each Questions entity will only accept answers from a specific choice set. Now that choice set can only have one option, so you have to choose that or leave it blank. That is how _"describe your day"_ would work. You would provide one choice that accepts only a textual input. Where _"how good is your day from 1-4"_ could accept 1 of 4 possible answers very bad(1) to very good(4). 

In the later example each choice had associated with it a value. This is the default value of the choice. Be default you are not allowed to change the value, but if you enable the __allow_custom_values__ flag of the choice you will be prompted to change the value if you wish while submitting it. 

Once you fill out the survey you can submit it. Then all the answers associated will be created. 


## UI supported while submitting surveys

__At Present__

- box 
    + text box ~10 characters
- radio 
    + one selection
    + shows default value and a box for edits if allow_custom_value is true
- check
    + multiple selections possible
    + shows value and a box for edits if allow_custom_value is true
- bigbox (text box ~500 chars)
    + starts with default value

__In Future__

- date
    + a calendar allowing you to select dates
- datetime
    +  a calendar and clock allowing you to select date and time
-  slider 
    +  allowing you to select a range of numbers/dates/times/substring of default value 
-  person
    +  allow the person to indicate another person in the study. 
    +  or add a new person to the study if they aren't already there?






















--------------------------------------

# Installation and setup

these are instructions on how to set up everything not included in the git project. Including:

- The MySQL Server
- Django & starting a site
- Configuring the Django settings

first install a mysql server

Create a database and django user for this project in the server  
```mysql
CREATE DATABASE <database name> Character Set UTF8;
CREATE USER <django user name>@<host e.g. localhost> IDENTIFIED BY '<password for django user>';
GRANT ALL PRIVILEGES ON <database name>.* TO <django user name>@<host e.g. localhost>;
FLUSH PRIVILEGES;
```


To start the server on linux if it doesn't autostart run:
```bash
sudo /etc/init.d/mysql start
```

install django and django-extensions for python 2.7

```bash
pip install django
pip install django-extensions
```

configure the django settings and urls

in urls.py for the main site add
```python
url(r'^', include('db.urls', namespace='db')),
```
in settings.py add to      
```python
INSTALLED_APPS=[
'db',
'django_extensions',
]
```
change DATABASES to match the following
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database name>',
        'USER': '<django user name>',
        'PASSWORD': '<password for django user>',
        'HOST': '<host e.g. localhost>',
        'PORT': '<port on host. for localhost leave blank>',
    }
}
```

To set up the database run:
```bash
python manage.py makemigrations # to prepare changes to the database
python manage.py migrate # to make changes to the database
python manage.py createsuperuser # to log onto the admin site
```
