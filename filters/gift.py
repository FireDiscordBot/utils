"""
gifts
~~~~~~~~~~~~~~~~~~~~~

An extension module to help finding and replacing discord gift links
"""

import re
from fire import exceptions

gift = r'(?:http|https)?(?::)?(?:\/\/)?((?:canary\.|ptb\.)?discord(?:app)?.(?:com\/gifts|gift)\/([a-zA-Z0-9\-]+))'
giftreplace = '[redacted gift]'

def findgift(text: str):
	found = []
	[found.append(i) for i in re.findall(gift, text, re.MULTILINE) if i and i not in found]
	return found

def replacegift(text: str):
	text = re.sub(gift, giftreplace, text, 0, re.MULTILINE)
	return text
