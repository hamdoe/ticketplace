""" Utility functions used throughout the project """

import datetime


def kst_now():
    """ Current datetime with timezone of KST """
    kst = datetime.timezone(datetime.timedelta(hours=9))  # Korea Standard Time
    return datetime.datetime.now(tz=kst)


def construct_email_content_from_dict(d):
    """Simple email format to display contents in dictionary"""
    return '\n'.join('%s: %s' % (k, v) for k, v in d.items())