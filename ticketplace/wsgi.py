""" WSGI file for Heroku Deployment
"""
from ticketplace import create_app

app = create_app('ticketplace.settings.ProdConfig', env='prod')
