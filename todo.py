import sqlite3
from datetime import datetime

conn = sqlite3.connect("zazuDB.db")
c = conn.cursor()

def addToDo(user, channel, content, isPrivate):
	try:
		c.execute("INSERT INTO ToDo VALUES(null, ?, ?, ?, ?, ?, ?)", ("TRUE" if isPrivate else "FALSE", user, channel, content, "FALSE", datetime.now()))
		conn.commit()
	except :
		print("Unexpected error: " + sys.exc_info())
def deleteToDo(itemId, channel):
	c.execute("SELECT channel FROM ToDo WHERE itemId = ?", (itemId,))
	res = c.fetchall()[0][0]
	print(res)
	print(channel)
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

