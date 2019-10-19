"""
slack
~~~~~~~~~~~~~~~~~~~~~

An extension module to help communicating with Slack
"""

import aiohttp
import discord
import json
import os
from pathlib import Path
from fire import exceptions

with open(Path(os.environ['LOCALAPPDATA'] + "/Programs/Python/Python37-32/Lib/site-packages/fire/config.json"), 'r') as cfg:
	config = json.load(cfg)

SIGNING_SECRET = config['signing_secret']

async def sendvanity(slug: str, user: discord.Member, guild: discord.Guild):
	message = {
		"token":config['slackbot'],
		"channel":"CP7SH4G8K",
		"attachments":[
		   {
				"title":"Vanity URL Request",
				"fields":[
					{
						"title":"Guild",
						"value":f'{guild.name} ({guild.id})'
					},
					{
						"title":"User",
						"value":f'{user.name} ({user.id})'
					},
					{
						"title":"Requested Slug",
						"value":slug
					}
				],
				"author_name":"Fire",
				"author_icon":"https://cdn.discordapp.com/avatars/444871677176709141/4bafec4cf070f01ddf4a5428947813e6.png?size=1024"
			},
			{
				"fallback":"Please choose an option!",
				"title":"Please choose an option!",
				"callback_id":f'vanity_{guild.id}',
				"attachment_type":"default",
				"actions":[
					{
						"name":"ignore",
						"text":"Ignore",
						"type":"button",
						"value":"ignore",
						"style":"primary"
					},
					{
						"name":"delete",
						"text":"Delete",
						"type":"button",
						"value":"delete",
						"style":"danger"
					}
				]
			}
		]
	}
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + config['slackbot']
	}
	async with aiohttp.ClientSession(headers=headers) as s:
		async with s.post('https://slack.com/api/chat.postMessage', json=message) as r:
			response = await r.json()
	if not response['ok']:
		raise exceptions.PushError(f'An error occurred while posting a message to Slack\n{response["error"]}')
	return response['message']

async def updatevanitymsg(ignore: bool, message: dict):
	if ignore:
		message['attachments'][1] == {
			"title":"Ignored!",
			"color": "#4CAF50"
		}
		data = {
			"token": config['slackbot'],
			"channel": "CP7SH4G8K",
			"ts": message['ts'],
			"attachments": message['attachments']
		}
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config['slackbot']
		}
		print(headers)
		async with aiohttp.ClientSession(headers=headers) as s:
			async with s.post('https://slack.com/api/chat.update', json=data) as r:
				response = await r.json()
				if response['ok']:
					return True
				else:
					raise exceptions.PushError(f'An error occurred while updating a message on Slack\n{response["error"]}')
	else:
		message['attachments'][1] == {
			"title":"Deleted!",
			"color": "#D32F2F"
		}
		data = {
			"token": config['slackbot'],
			"channel": "CP7SH4G8K",
			"ts": message['ts'],
			"attachments": message['attachments']
		}
		async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as s:
			async with s.post('https://slack.com/api/chat.update', json=data) as r:
				response = await r.json()
				if response['ok']:
					return True
				else:
					raise exceptions.PushError(f'An error occurred while updating a message on Slack\n{response["error"]}')
