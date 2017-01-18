import discord
import asyncio
import json
import re
import todo
from sys import argv

with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

client = discord.Client()

@client.event
async def on_ready():
	print("Zazu bot coming online")

@client.event
async def on_message(message):
	print("received message: " + message.content + str(message.channel.is_private))
	if message.content == "/stop":
		await client.logout()
		return
	elif message.content == "/kill":
		await client.logout()
		await client.close()
		return

	m = re.match("/todo add (.*)", message.content)
	if m:
		todo.addToDo(message.author.id, message.channel.id, m.group(1), message.channel.is_private)
		await client.send_message(message.channel, "Added your item to the ToDo list")
		return

	m = re.match("/todo delete (\d+)", message.content)
	if m:
		res = todo.deleteToDo(int(m.group(1)), message.channel.id)
		if res == -1:
			await client.send_message(message.channel, "You don't have permissions to delete this item")
			return	
		await client.send_message(message.channel, "Deleted the item from the ToDo list")

	m = re.match("/todo list", message.content)
	if m:
		todoList = "Todo list:\n"
		res = todo.listToDoUser(str(message.author.id)) if message.channel.is_private else todo.listToDoChannel(str(message.channel.id))

		for item in res:
			itemId, txt, done = item
			todoList += str(itemId) + " - " + "~~" + txt + "~~\n" if  not done else str(itemId) + " - " + txt + "\n"

		await client.send_message(message.channel, todoList)
		
	if re.match("[hH]i", message.content):
		await client.send_message(message.channel, "Suh dud")	


client.run(settings["Token"])

