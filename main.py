import discord
import asyncio
import json
import re
import messageParser

with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

client = discord.Client()

@client.event
async def on_ready():
	print("Zazu bot coming online")

@client.event
async def on_message(message):
	if int(message.author.id) == int(settings["BotID"]):
		return

	print("received message: " + message.content)

	if message.content == "/kill" and int(message.author.id) in settings["Owners"]:
		await client.logout()
		await client.close()
		return
	elif message.content == "/help":
		client.send_message(message.channel, messageParser.listAvailableCommands())		

	res = messageParser.parseMessage(message)
	if not res == None:
		await client.send_message(message.channel, res)

client.run(settings["Token"])

