import discord
import asyncio
import json
import re
from sys import argv

with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

client = discord.Client()

@client.event
async def on_ready():
	print("Zazu bot coming online")

@client.event
async def on_message(message):
	print("received message: " + message.content)
	if message.content == "/stop":
		await client.logout()
	elif message.content == "/kill":
		await client.logout()
		await client.close()
		
	elif re.match("[hH]i", message.content):
		await client.send_message(message.channel, "Suh dud")	


client.run(settings["Token"])

