
def numGenerator(startNum=0, increment=1):
	num = startNum
	while 1:
		yield num
		num += increment

def getNumGenerator():
	return numGenerator()

