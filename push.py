"""
push
~~~~~~~~~~~~~~~~~~~~~

An extension module to help communicating with services like Pushover
"""

import aiohttp
import json
import os
from pathlib import Path
from fire import exceptions

with open("config.json", 'r') as cfg:
	config = json.load(cfg)

async def pushover(msg: str, url: str = "https://api.gaminggeek.club/", url_title: str = 'Click here!'):
	'''Function to send messages to pushover'''
	headers = {
		'USER-AGENT': 'Fire',
		'CONTENT-TYPE': 'application/json'}
	async with aiohttp.ClientSession(headers=headers) as session:
		token = config['pushovertoken']
		user = config['pushoveruser']
		async with session.post(f"https://api.pushover.net/1/messages.json?token={token}&user={user}&message={msg}&url={url}&url_title={url_title}") as resp:
			status = resp.status
			if status == 200:
				return True
			else:
				raise exceptions.PushError(f"Pushover request was unsuccessful!\n Status code: {status}")
