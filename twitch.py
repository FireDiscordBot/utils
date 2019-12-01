"""
twitch
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with twitch urls
"""

import re
from fire import exceptions

twitchurl = r'((?:https?:)?\/\/)?(?:[\w]+\.)?((?:twitch\.tv))(\/)([\w]+)(\S+)?'
replace = '[redacted twitch url]'

def findtwitch(text: str):
	search = re.search(twitchurl, text.strip('<>`*~#!"()[]\{\};:\''))
	if search:
		return search.group(4)
	else:
		return False

def replacetwitch(text: str):
	message = re.sub(twitchurl, replace, text.strip('<>`*~#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False
