import re
import todo

availableCommands = {"todo": todo}

def parseMessage(message):
	msg = list(filter((lambda x: len(x) > 0), message.content.lstrip(" \n\t\r").split(" ")))
	print(str(msg))
	if msg[0][0] == '/' and msg[0][1:] in set(availableCommands.keys()):
		return availableCommands[msg[0][1:]].parseCommand(message, " ".join(msg)[1:])
	elif msg[0][0] == '/':
		return "Invalid command.\n" + listAvailableCommands()

	return None

def listAvailableCommands():
	commands = "Here's a list of all available commands: \n"
	for comm in list(availableCommands.keys()):
		commands += str(comm) + "\n"

	commands += "To see details on one specific command you can type the command followed by help."
	return commands
