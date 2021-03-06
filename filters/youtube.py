"""
youtube
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with youtube related data (e.g. url regex)
"""

import re
from fire import exceptions

channel = r'(?:https|http)\:\/\/(?:[\w]+\.)?youtube\.com\/(?:c\/|channel\/|user\/)?([a-zA-Z0-9\-]{1,})'
video = r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be|invidio.us))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?'
ytreplace = '[redacted youtube url]'

def findchannel(text: str):
	search = re.search(channel, text.strip('<>`*~_#!"()[]\{\};:\''))
	if search:
		return search.group(1)
	else:
		return False

def replacechannel(text: str):
	message = re.sub(channel, ytreplace, text.strip('<>`*~_#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False

def findvideo(text: str):
	search = re.search(video, text.strip('<>`*~_#!"()[]\{\};:\'').replace('/embed/', '/watch?v='))
	if search:
		return search.group(5)
	else:
		return False

def replacevideo(text: str):
	message = re.sub(video, ytreplace, text.strip('<>`*~_#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False
