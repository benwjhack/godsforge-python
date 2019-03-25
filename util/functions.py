import random


def foldr(cons, nils, xs):
	if len(xs) == 0:
		return nils
	head = xs[0]
	tail = xs[1:]
	return cons(head, foldr(cons, nils, tail))

def add(a, b):
	return a+b

def shuffled(xs): # Return a shuffled permuation of xs
	ys = xs[:]
	random.shuffle(ys) # Shuffles in place
	return ys
