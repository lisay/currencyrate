import graph

test  = graph.PriorityQueue()


test.insert((0, 'p'))
test.insert((2, 'y'))
test.insert((3, 'w'))
test.insert((4, 'e'))
test.insert((5, 't'))
test.insert((6, 'r'))

print test.keys
print test.dic
while not test.isEmpty():
	print test.deleteMin()
