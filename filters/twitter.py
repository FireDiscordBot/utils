"""
twitter
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with twitter urls
"""

import re
from fire import exceptions

twitterurl = r'((?:https?:)?\/\/)?(?:[\w]+\.)?((?:twitter\.com))(\/)([\w]+)(\S+)?'
replace = '[redacted twitter url]'

def findtwitter(text: str):
	search = re.search(twitterurl, text.strip('<>`*~#!"()[]\{\};:\''))
	if search:
		return search.group(4)
	else:
		return False

def replacetwitter(text: str):
	message = re.sub(twitterurl, replace, text.strip('<>`*~#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False
