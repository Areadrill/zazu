#TODO: descriptions on Transactions
import sqlite3
from datetime import datetime
import re

pattern = re.compile("dtracker (help|addTrans [^\s]+ (?:\[\s*(?:[^\s,]+, )*[^\s,]+\s*\]|all) \d+(?:(?:,|\.)\d+)?|addMock [^\s]+ [^\s]+|delTrans (?:\d)+|delMock [^\s]+|list [^\s]+|listTrans [^\s]+|create [^\s]+|join (?:[^\s]+)? [^\s]+|leave (?:[^\s]+)? [^\s]+)")

conn = sqlite3.connect("zazuDB.db")
c = conn.cursor()

def parseCommand(message, msg):
	m = pattern.match(msg)
	if m:
		mm = m.group(1).split(" ")
		if m.group(1) == "help":
			return help()
		elif mm[0] == "addTrans":
			group = mm[1]
			amount = mm[-1]
			people = list(map((lambda x: x.strip(" \n\t\r][,")), mm[-2:1:-1])) if mm[2] != "all" else mm[2]
			
			if addTransaction(group, amount, message.author.id, people):
				return "Added transaction to the group"
			else:
				return "Failed to add transaction"
		elif mm[0] == "addMock":	
			group = mm[1]
			name = mm[-1]

			if addMock(group, name, message.author.id):
				return "Mock user added"
			else:
				return "Couldn't add mock user"
		elif mm[0] == "delTrans":
			tid = mm[1]

			if deleteTransaction(tid):
				return "Deleted transaction successfully"
			else:
				return "Couldn't delete transaction"
		elif mm[0] == "delMock":
			mid = mm[1]

			if deleteMock(mid):
				return "Deleted mock user successfully"
			else:
				return "Couldn't mock user transaction"
		elif mm[0] == "join":
			try:
				if joinGroup(mm[1], getUserId(mm[2])[0] if len(mm) == 3 else message.author.id):
					return "Joined group"
				else:
					return "Couldn't join group"
			except: 
				return "Mock user doesn't exist"
		elif mm[0] == "leave":
			try:
				if leaveGroup(mm[1], getUserId(mm[2])[0] if len(mm) == 3 else message.author.id):
					return "Left group"
				else:
					return "Couldn't leave group"
			except: 
				return "Mock user doesn't exist"
		elif mm[0] == "create":
			if createGroup(mm[1]):
				return "Created new group"
			else:
				return "Couldn't create group"
		elif mm[0] == "listTrans":
			return listTransactions(mm[1])
	else:
		return "Malformed dtracker command.\n" + help()


def help():
	return """\
	Usage: /dtracker under construction
	"""

def getGroupId(gName):
	c.execute("SELECT groupId FROM Group WHERE name = ?", (gName,))
	return c.fetchone()

def getUserId(uName):
	c.execute("SELECT userId FROM User WHERE name = ?", (p,))
	pid = c.fetchone()

def addTransaction(group, amount, issuer, people):
	try:
		c.execute("INSERT INTO Transaction VALUES(null, ?, ?, ?, ?)", (issuer, getGroupId(group)[0], float(amount), datetime.now()))
		for p in people:
			c.execute("INSERT INTO UsersInTransaction VALUES(?, ?)", (getUserId(p)[0], group))
		conn.commit()
		return True
	except :
		print("Unexpected error: " + sys.exc_info())
		return False

def addMock(group, name, creator):
	try:
		if len(getUserId(name)) != 0:
			return False
		c.execute("INSERT INTO User VALUES(null, ?, ?, ?, ?)", (name, "TRUE", creator, datetime.now()))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def deleteTransaction(tid):
	try:
		c.execute("DELETE FROM Transaction WHERE transId = ?", (tid ,))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def deleteMock(mid):
	try:
		c.execute("DELETE FROM User WHERE userId = ?", (tid ,))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def joinGroup(group, uid):
	try:
		c.execute("INSERT INTO UsersInGroup VALUES(?, ?)", (uid, getGroupId(group)[0]))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def leaveGroup(group, uid):
	try:
		c.execute("DELETE FROM UsersInGroup WHERE groupId = ? AND userId = ?", (getGroupId(group)[0], uid))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def createGroup(name):
	try:
		c.execute("INSERT INTO Group VALUES(null, ?, ?)", (name, datetime.now()))
		conn.commit()
		return True
	except:
		print("Unexpected error: " + sys.exc_info())
		return False

def listTransactions(gName):
	try:
		c.execute("SELECT * FROM Group WHERE groupId = ?", (getGroupId(gName)[0],))
		transactions = c.fetchall()

		
		return transactions
	except:
		print("Unexpected error: " + sys.exc_info())
		return "Couldn't get transactions"