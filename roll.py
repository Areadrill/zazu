import re, os, sys

pattern = re.compile("roll (help|(?:(?:\d+d\d+\s?)+))")

def parseCommand(message, msg):
	m = pattern.match(msg)
	if m:
		if m.group(1) == "help":
			return help()
		else:
			return processRolls(m.group(1))
	else:
		return "Malformed roll command.\n" + help()

def help():
	return """\
	Usage: /roll [number of dice]d[number of faces on the die]
	You can do several rolls at a time by writing them all in sequence.
	For example, this is a valid command: /roll 1d20 2d6 1d1000
	"""

def processRolls(rolls):
	result = "Here are your rolls:\n"

	individualRolls = rolls.split(" ")
	for r in individualRolls:
		result += r + ": "
		pr = r.split("d")
		accum = 0
		for i in range(int(pr[0])):
			res = getRoll(int(pr[1]))
			accum += res
			result += str(res) + ", "
		result += "Total: " + str(accum) + "\n"
		
	return result




#As random as I can make it...
def getRoll(number):
	res = int.from_bytes(os.urandom(50), byteorder=sys.byteorder) % number
	return res if not res == 0 else number