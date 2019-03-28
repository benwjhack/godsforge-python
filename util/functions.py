import random


def foldr(cons, nils, xs):
	if len(xs) == 0:
		return nils
	head = xs[0]
	tail = xs[1:]
	return cons(head, foldr(cons, nils, tail))

def unfold(nil, head, tail, x):
	if nil(x):
		return []
	return [head(x)] + unfold(nil, head, tail, tail(x))

def add(a, b):
	return a+b

def _or(a, b):
	return a or b

def shuffled(xs): # Return a shuffled permuation of xs
	ys = xs[:]
	random.shuffle(ys) # Shuffles in place
	return ys

def id(x): return x


