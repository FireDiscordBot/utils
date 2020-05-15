"""
twitter
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with twitter urls
"""

import re
from fire import exceptions

twitterurl = r'((?:https?:)?\/\/)?(?:[\w]+\.)?((?:twitter\.com))(\/)([\w]+)(\S+)?'
twitterembed = r'(?:The latest Tweets from .+ \(@(\w+)\)|.+ \(@(\w+)\) \| Twitter)'
replace = '[redacted twitter url]'

def findtwitter(text: str):
	search = re.search(twitterurl, text.strip('<>`*~#!"()[]\{\};:\''))
	esearch = re.search(twitterembed, text.strip('<>`*~#!"()[]\{\};:\''))
	if search:
		return search.group(4)
	elif esearch:
		return f'https://twitter.com/{esearch.group(2)}' if esearch.group(2) else f'https://twitter.com/{esearch.group(1)}'
	else:
		return False

def replacetwitter(text: str):
	message = re.sub(twitterurl, replace, text.strip('<>`*~#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False
