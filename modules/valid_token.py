from datetime import datetime


def token_end_date(date):
    now = datetime.now()
    if now < date:
        return 'date valid'

