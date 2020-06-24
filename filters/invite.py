"""
invite
~~~~~~~~~~~~~~~~~~~~~

An extension module to help finding and replacing discord invite links
"""

import re
from fire import exceptions

dgg = r'(?:http|https)?(?::)?(?:\/\/)?((?:dis|discord|invite).(?:gd|gg|io|me)\/([a-zA-Z0-9\-]+))'
dappcom = r'(?:http|https)?(?::)?(?:\/\/)?((?:discord(?:app)?|watchanimeattheoffice).com\/invite\/([a-zA-Z0-9\-]+))'
vanity = r'(?:http|https)?(?::)?(?:\/\/)?((?:oh-my-god|(?:h\.|i\.)?inv|floating-through|get-out-of-my-parking|i-live-in|i-need-personal)\.(?:wtf|space)\/([a-zA-Z0-9\-]+))'
invreplace = '[redacted invite]'

def findinvite(text: str):
	found = []
	for r in [dgg, dappcom, vanity]:
		[found.append(i) for i in re.findall(r, text, re.MULTILINE) if i and i not in found]
	return found

def replaceinvite(text: str):
	for regex in [dgg, dappcom, vanity]:
		text = re.sub(regex, invreplace, text, 0, re.MULTILINE)
	return text
