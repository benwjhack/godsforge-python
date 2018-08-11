import dill as pickle
import os

BACKUP_DIRECTORY = "backup/"
EXTENSION = ".save"
DEFAULT_FILE = "default"
PROTOCOL = 0

def save(thing, fileName=DEFAULT_FILE):
	with open(BACKUP_DIRECTORY+fileName+EXTENSION, "w") as file:
		pickle.dump(thing, file, PROTOCOL)

def load(fileName=DEFAULT_FILE):
	with open(BACKUP_DIRECTORY+fileName+EXTENSION) as file:
		return pickle.load(file)

def isSaveFile(fileName=DEFAULT_FILE):
	return os.path.isfile(BACKUP_DIRECTORY+fileName+EXTENSION)
