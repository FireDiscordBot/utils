"""
skus
~~~~~~~~~~~~~~~~~~~~~

An extension module to help finding and replacing discord store sku links
"""

import re
from fire import exceptions

sku = r'(?:http|https)?(?::)?(?:\/\/)?((?:canary\.|ptb\.)?discord(?:app)?.com\/store\/skus\/(\d{16,18})\/.+)'
skureplace = '[redacted sku]'

def findsku(text: str):
	found = []
	[found.append(i) for i in re.findall(sku, text, re.MULTILINE) if i and i not in found]
	return found

def replacesku(text: str):
	text = re.sub(sku, skureplace, text, 0, re.MULTILINE)
	return text
