
def breadth_search(connectorf, start, end):
	
	queue = [start]
	d = {start: 0} # Distance dict
	p = {} # Predecessor dict
	
	finished = False
	
	while queue and not finished:
		c = queue.pop(0)
		ns = connectorf(c)
		for n in ns:
			if n in d: continue
			queue.append(n)
			p[n] = c
			d[n] = d[c] + 1
			if n == end:
				finished = True
				break
	
	if not finished:
		return None # If end was never found, return null value
	
	c = end
	path = [c] # Reverse engineer the path from the predecessor array
	
	while c != start:
		c = p[c]
		path.append(c)
	
	return path[::-1], d[end]
