import json, util.input as input

with open("ask.json", "r") as file:
	data = json.loads(file.read())

print data
input.getInput(data["prompt"])
