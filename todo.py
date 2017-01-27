import sqlite3
from datetime import datetime
import re

pattern = re.compile("todo (add (.+)|delete (\d+)|list|help)")

conn = sqlite3.connect("zazuDB.db")
c = conn.cursor()


def parseCommand(message, msg):
	m = pattern.match(msg)
	if m:
		if m.group(1).split(" ")[0] == "add":
			addToDo(message.author.id, message.channel.id, m.group(2), message.channel.is_private)
			return "Added your item to the ToDo list"
		elif m.group(1).split(" ")[0] == "delete":
			return "Deleted your item from the ToDo list" if not deleteToDo(m.group(2), message.channel.id) == -1 else "You dont't have permission to delete this item"
		elif m.group(1).split(" ")[0] == "list":
			todoList = "Todo list:\n"
			res = listToDoUser(str(message.author.id)) if message.channel.is_private else listToDoChannel(str(message.channel.id))

			for itemId, txt, done in res:
				todoList += str(itemId) + " - " + "~~" + txt + "~~\n" if  not done else str(itemId) + " - " + txt + "\n"

			return todoList
		elif m.group(1) == "help":
			return help()

		#elif m.group(1).split(" ")[0] == "complete":
		#elif m.group(1).split(" ")[0] == "undo":
	else:
		return "Malformed todo command\n" + help()

def help():
	return """\
		Usage: /todo [option] [value] - where option is:

		add: Adds an item to the channel's or your personal todo list. Expects a value that will be the title of the todo item
		delete: Deletes an item from the channel or your personal todo list. Expects an integer values correponding to the identifier of the item you want to delete
		list: Lists yours or the channel's todo list. Expects no value
	"""	

def addToDo(user, channel, content, isPrivate):
	try:
		c.execute("INSERT INTO ToDo VALUES(null, ?, ?, ?, ?, ?, ?)", ("TRUE" if isPrivate else "FALSE", user, channel, content, "FALSE", datetime.now()))
		conn.commit()
	except :
		print("Unexpected error: " + sys.exc_info())

def deleteToDo(itemId, channel):
	c.execute("SELECT channel FROM ToDo WHERE itemId = ?", (itemId,))
	res = c.fetchall()[0][0]
	if int(res) != int(channel):
		return -1
	try:
		c.execute("DELETE FROM ToDo WHERE itemId = ?", (itemId,))
		conn.commit()
	except :
		print("Unexpected error: " + sys.exc_info())

def listToDoUser(user):
	c.execute("SELECT itemId, content, done FROM ToDo WHERE isPrivate = 'TRUE' AND user = ?", (user,))
	return c.fetchall()

def listToDoChannel(channel):
	c.execute("SELECT itemId, content, done FROM ToDo WHERE channel = ?", (channel,))
	return c.fetchall()

