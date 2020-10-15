"""
twitter
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with twitter urls
"""

import re
from fire import exceptions

twitterurl = r'((?:(?:https?:)?\/\/)?(?:[\w]+\.)?(?:(?:twitter\.com))(?:\/)([\w]+)(\S+)?)'
replace = '[redacted twitter url]'


def findtwitter(text: str):
    search = re.findall(twitterurl, text.strip(
        '<>`*~#!"()[]\{\};:\''), re.MULTILINE)
    if search:
        return search
    else:
        return False


def replacetwitter(text: str):
    message = re.sub(twitterurl, replace, text.strip(
        '<>`*~#!"()[]\{\};:\''), 0, re.MULTILINE)
    if message:
        return message
    else:
        return False
