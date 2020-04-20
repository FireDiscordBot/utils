"""
paypal
~~~~~~~~~~~~~~~~~~~~~

An extension module to help with finding paypal.me urls
"""

import re
from fire import exceptions

paypalme = r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:paypal\.me))(\/)([\w\-]+)(\S+)?'
ppreplace = '[redacted paypal url]'

def findpaypal(text: str):
	search = re.search(paypalme, text.strip('<>`*~#!"()[]\{\};:\''))
	if search:
		return search.group(5)
	else:
		return False

def replacepaypal(text: str):
	message = re.sub(paypalme, ppreplace, text.strip('<>`*~#!"()[]\{\};:\''), 0, re.MULTILINE)
	if message:
		return message
	else:
		return False
