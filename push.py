"""
push
~~~~~~~~~~~~~~~~~~~~~

An extension module to help communicating with services like Pushbullet or Pushover
"""

import aiohttp
import json
import os
from pathlib import Path
from fire import exceptions

with open("/home/geek/.local/lib/python3.7/site-packages/fire/config.json", 'r') as cfg:
	config = json.load(cfg)

async def pushbullet(msgtype: str, title: str, message: str, link: str = "https://discordapp.com/channels/@me"):
	'''Function to send messages to pushbullet'''
	headers = {
		'USER-AGENT': 'Fire',
		'CONTENT-TYPE': 'application/json',
		'ACCESS-TOKEN': config['pushbullet']}
	body = {
		'type': f'{msgtype}',
		'title': f'{title}',
		'body': f'{message}',
		'url': f'{link}'} 
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.post("https://api.pushbullet.com/v2/pushes", json=body) as resp:
			status = resp.status
			if status == 200:
				return True
			else:
				json = await resp.json()
				if json['error_code'] == 'pushbullet_pro_required':
					raise exceptions.PushError(f'Pushbullet request was unsuccessful\nReason: Pushbullet Pro Required (Free has a 500/month limit)')
				else:
					raise exceptions.PushError(f"Pushbullet request was unsuccessful!\n Status code: {status}")

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
