#Ticketplace
[![Build Status](https://travis-ci.org/Ticketplace/ticketplace.svg)](https://travis-ci.org/Ticketplace/ticketplace)

# Installation

## Clone the repository

  > git clone https://github.com/ticketplace/ticketplace.git

  > cd ticketplace

## Initiate a virtual environment

  > virtualenv env

## Activate the virtual environment

**unix**:
 
  > source ./env/bin/activate

**windows**:
 
  > env\Scripts\activate.bat

## Install libraries

  > pip install -r requirements.txt

## Well, that was easy

  > python manage.py runserver

# Configuration

## Make local settings file

  > touch ticketplace/local_settings.py

(Filename must be exactly 'ticketplace/local_settings.py')
  
## Example settings file

```python

from ticketplace.settings import DevelopmentConfig
   
   
   class LocalConfig(DevelopmentConfig):
       """ Configuration for local.
       """
       SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:h@110w0r1d@localhost/ticketplace'
       EXAMPLE_VARIABLE = 'TROLOLOLO'
```

## Optionally set environment variables

DATABASE_URL : Sqlalchemy database url. This overrides SQLALCHEMY_DATABASE_URI setting from class based settings file.

DATABASE_TEST_URL : Sqlalchemy database url for testing. (e.g. `make test`)

# Run test

## Set environment varibles for test

  > export DATABASE_TEST_URL=postgres://example@localhost/example
  
## Run test and pray for only dots

  > make test
