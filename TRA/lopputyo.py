import time

"""
Tekstitiedostossa tieverkko:
Ensimmäisellä rivillä kaupunkien lkm. ja teiden lkm.
Sen jälkeen omalla rivillään tiet lukukolmikkona:
lähtökaupunki, maalikaupunki, tien korkeus(hinta)
Viimeisellä rivillä on kaupunki, johon reittiä etsitään.
"""

def kysy_data(): 
	"""Kysyy käyttäjältä tiedoston, josta data luetaan"""
	while True:
		datatiedosto = str(input("Give the text file for reading data (With the .txt extension!): "))
		return datatiedosto

def kasittele_data(tiedosto):
	"""Opens the data file, reads it and saves the data in an array and variables. After done, closes the data file"""
	f = open(tiedosto, "r")
	print(" ")
	print("Reading data...")
	print(" ")
	data_array = [] #Alustus taulukolle, johon tallennetaan kaupunkien väliset tiet ja niiden korkeudet
	textrow_1 = f.readline().split()
	node_amount = int(textrow_1[0])
	road_amount = int(textrow_1[1])   #Ottaa datasta talteen solmujen(kaupunkien) ja teiden lukumäärän
	for i in range(int(road_amount)):
		data_row = f.readline().split()
		data_array.append(data_row)
	goal_node = int(f.readline())      #Verkon data ja päätepiste talteen
	f.close()
	return data_array, node_amount, road_amount, goal_node

def isCyclic(graph, newEdge):
	"""
	Checks if a new edge makes the graph cyclic. Takes the graph as an array of connected nodes.
	For example, [[3,4,8],[5,10,11]]
	New edge is given as a pair of two nodes.
	"""
	for i in graph:
		if newEdge[0] in i and newEdge[1] in i:
			return True
	return False

def Union(a,b):
	"""Creates a union from two lists"""
	c = []
	for i in a + b:
		if i not in c:
			c.append(i)
	return c

def connectEdges(connectedTrees, duplicateNodes):
	"""
	Connects two separate trees into a single tree using the common node.
	connectedTrees will be merged using the duplicateNodes.
	for example [[1,3,5,6],[2,6,8,10]] -> [1,2,3,5,6,8,10] duplicateNodes = 6
	for example[[3,5,6],[6,8],[8,10,13]] -> [3,5,6,8,10,13], duplicateNodes = 6,8
	"""
	for j in duplicateNodes:
		toBeMerged = []	#List that will take in two lists(trees) to be merged in the next for-loop
		toBeRemoved = []
		for i in connectedTrees:
			if j in i:
				toBeMerged.append(i)
				toBeRemoved.append(i)

		for i in toBeRemoved:
			connectedTrees.remove(i)

		mergedTree = Union(toBeMerged[0],toBeMerged[1])
		connectedTrees.append(mergedTree)


def Kruskal(data_array, nodeAmount):
	"""
	This function creates a minimumSpanningTree using Kruskal's algorithm
	The function takes the data_array as a parameter and creates a MST as a similar
	type of a data array. The result is a array with each index of the array having 3 values (start,end,weight)
	"""
	nodesWithPaths = []		#List of nodes with at least one connection
	minimumTree = []		#The result tree will be stored in this list
	connectedTrees = []		#list of trees already existing in the forest

	arranged_data = sorted(data_array,key=lambda data_array: int(data_array[2]))

	print("Creating MST...")
	print(" ")
	while len(minimumTree) < (int(nodeAmount) - 1):
		for i in arranged_data:
			duplicates = []
			newEdge = [i[0],i[1]]
			if not isCyclic(connectedTrees,newEdge):
				minimumTree.append(i)
				connectedTrees.append([i[0],i[1]])
				if i[0] in nodesWithPaths:
					duplicates.append(i[0])
				if i[1] in nodesWithPaths:
					duplicates.append(i[1])
				nodesWithPaths.append(i[0])
				nodesWithPaths.append(i[1])
				if len(nodesWithPaths) != len(set(nodesWithPaths)):
					connectEdges(connectedTrees,duplicates)
				nodesWithPaths = list(set(nodesWithPaths))
	print("MST Created!")
	print(" ")
	return minimumTree

def getAdjacents(arrangedMST, node_amount):
	"""
	Returns a list of adjacent nodes for every node.
	"""
	adjacents = []
	for i in range(node_amount):
		adjacents.append([])
	for i in range(node_amount-1):
		startnode = arrangedMST[i][0]
		endnode = arrangedMST[i][1]
		adjacents[int(startnode)-1].append(int(endnode))
		adjacents[int(endnode)-1].append(int(startnode))
	return adjacents

def highestPath(path, MST):
	"""Takes the final path and the original MST array with the path weight info.
	Then finds the highest connection on the path.
	"""
	highest = 0
	for i in range(len(path) - 1):
		start = path[i]
		end = path[i + 1]
		for j in MST:													#Find the path weights from the MST array, time complexity for this could probably be way lower
			if start == int(j[0]) and end == int(j[1]) or start == int(j[1]) and end == int(j[0]):
				if int(j[2]) > highest:
					highest = int(j[2])
	return highest

def DFS (MST, node_amount, goalNode):
	"""
	Finds the path from the start node to the finish node by performing
	a depth-first search on the minimum spanning tree
	"""
	try:
		arrangedByStartNode = sorted(MST,key=lambda MST: int(MST[0]))	#Arrange MST by start node	
		adjacents = getAdjacents(arrangedByStartNode, node_amount)		#get adjacent nodes for every node as an array f. ex. adjacents 1 and 3 for node 2 would be shown as [[2][1,3][2]]
		for i in adjacents:
			i.sort()													#sorting the adjacents in ascending order, so that we will later visit the largest number node first
		curr = 1														#current node
		currPath = [1]													#list of nodes traversed, the end result path will be stored here, always has the node 1 in the beginning
		pred = [0] * node_amount										#previous node, where we got to the current node from. Every index will contain the predecessor for the node. pred[0] will always be 0
		pred[0] = "alku"												#Special predecessor for the start node

		while curr != goalNode:
			if curr not in currPath:
				currPath.append(curr)	
			currAdjacents = adjacents[curr-1]							#Get the adj. nodes for the current node
			
			if pred[curr-1] in currAdjacents:
				currAdjacents.remove(pred[curr-1])							#Remove the predecessor from the list of adjacents

			if currAdjacents:	#Jumps to the next node, deletes it from list of adjacents in previous node and assings the previous node as the predecessor for the next one.
				prev = curr
				curr = currAdjacents.pop()
				pred[curr-1] = prev					
			else:					#This should back up until we find a branch with undiscovered nodes if there's a dead end
				curr = pred[curr-1]
				del currPath[-1]

	except IndexError:
		print("error :(")
		return 0
		
	currPath.append(goalNode)
	print("Final path is: " + str(currPath))
	print("Final Node " + str(goalNode) + " found")

	highestPoint = highestPath(currPath, MST)
	print("Highest point on the path is: " + str(highestPoint))
	return 0

def main():
	while True:
		try:
			data_array, node_amount, road_amount, goal_node = kasittele_data(kysy_data())
			start_time = time.time()
			minimumSpanningTree = Kruskal(data_array, node_amount)
			minimumPath = DFS(minimumSpanningTree, node_amount, goal_node)
			end_time = time.time()
			total_time = (end_time - start_time)
			print("--- %s seconds ---" % (total_time))

			break
		except FileNotFoundError:
			print("")
			print("No such file found! Enter a file that exists in the same directory as main.py!")
			print("")

main()

