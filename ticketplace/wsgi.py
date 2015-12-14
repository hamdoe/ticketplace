""" WSGI file for Heroku Deployment
"""
from ticketplace import create_app

app = create_app('ticketplace.settings.HerokuConfig', env='production')
