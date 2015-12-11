from ticketplace.controllers.eduticket import eduticket
import os


@eduticket.route('/migrate')
def migrate():
    try:
        os.system('python3 migrate.py db upgrade')
        return 'DB migration succeed!'
    except Exception:
        return 'DB migration failed!'
