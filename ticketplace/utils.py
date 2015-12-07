""" Utility functions used throughout the project """

import datetime


def kst_now():
    """ Current datetime with timezone of KST """
    kst = datetime.timezone(datetime.timedelta(hours=9))  # Korea Standard Time
    return datetime.datetime.now(tz=kst)