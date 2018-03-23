
def getInput(prompt, options):
	print prompt
	options = [i.lower() for i in options]
	answer = None
	while not answer:
		reply = raw_input().lower()
		for option in options:
			if option in reply:
				if answer:
					if reply.startswith(option): answer = option
				else:
					answer = option
		if not answer:
			print "Enter a valid option"
	return options.index(answer)
