"""
invite
~~~~~~~~~~~~~~~~~~~~~

An extension module to help finding and replacing discord invite links
"""

import re
from fire import exceptions

inv = r'(http|https)?(:)?(\/\/)?(discordapp|discord|oh-my-god).(gg|io|me|com|wtf|com\/invite)\/(\w+:{0,1}\w*@)?(\S+)(:[0-10]+)?(\/|\/([\w#!:.?+=&%@!]))?'
invreplace = '[redacted invite]'

def findinvite(text: str):
	text = text.replace('>', '').replace('<', '').replace('_', '').replace('*', '').replace('~', '')
	search = re.search(inv, text)
	if search:
		return search.group(7)
	else:
		return False

def replaceinvite(text: str):
	message = re.sub(inv, invreplace, text, 0, re.MULTILINE)
	if message:
		return message
	else:
		return False