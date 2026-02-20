from app.models.graph import Graph
from app.util.search import subsites
from app.util.search.siteMetadata import siteLocationAndName, siteMedium, siteTitle


class RequestGraph(Graph):
	def __init__(self, graph: dict | None) -> None:
		"""
		Graph class/model to specifically handle JSON format graphs (from requests)
		"""

		# Set graph
		self.graph = graph

		# Define attributes
		self.query = ''
		self.type = ''
		self.depth = -1
		self.sourceNodes = []
		self.topics = []
		self.topicLinks = []
		self.sourceLinks = []

		# Save attributes of inherited method if graph not None otherwise run construct method
		if graph != None:
			# Set attributes
			self.sourceNodes = graph['sources']
			self.topics = graph['topics']
			self.topicLinks = graph['topicLinks']
			self.sourceLinks = graph['sourceLinks']

			# Call constructor of parent function
			super().__init__(graph['name'], graph['type'], graph['depth'])

			# Set self.sources
			for source in self.sourceNodes:
				self.sources[source['id']] = source
		else:
			self.graph = {}
			self.construct()


	def construct(self) -> None:
		"""
		Redundant method, overriding to avoid NotImplemented error
		"""

		return



	def parse(self):
		"""
		Parse graph in JSON format
		"""

		self.graph = {
			'name': self.query,
			'depth': self.depth,
			'type': self.type,
			'topics': self.topics,
			'sources': self.sourceNodes,
			'topicLinks': self.topicLinks,
			'sourceLinks': self.sourceLinks
		}

		return self.graph



	def getAllSources(self) -> list[str]:
		"""
		Method to return a list of all URLs used by SourcedNodes
		"""

		return list(self.sources.keys())



	def addNode(self, source: str) -> None:
		"""
		Method to add a node by its URL
		"""

		allSites = self.getAllSources() # Get all sites

		# Check if source already exists
		if source in allSites:
			return None

		# Get node attributes
		name = siteTitle(source)
		location = siteLocationAndName(source)
		medium = siteMedium(source)
		topics = []
		neighbors = []

		subsources = subsites(source)

		# Make links (if any)
		for subsource in subsources:
			if subsource in allSites:
				# Add link
				self.sourceLinks.append({
					'target': subsource,
					'source': source
				})

				neighbors.append(subsource)

				# Add to neighbor
				for i, sourceNode in enumerate(self.sourceNodes):
					if sourceNode['source'] == subsource:
						self.sourceNodes[i]['neighbors'].append(source)

						topics.append(sourceNode['topics']) # Add topics

		# Add node to sourceNodes
		self.sourceNodes.append({
			'id': source,
			'source': source,
			'name': name,
			'location': location,
			'medium': medium,
			'topics': list(set(topics)),
			'neighbors': neighbors
		})



	def deleteNode(self, source: str) -> None:
		"""
		Method to delete a node given its source/ID
		"""

		# Delete node from Source list using list comprehension
		self.sourceNodes = [node for node in self.sourceNodes 
								 if node['id'] != source]
		
		# Delete node reference from topic links
		self.topicLinks = [link for link in self.topicLinks
					 			if link['source'] != source]
		
		# Delete node reference from source links
		self.sourceLinks = [link for link in self.sourceLinks
					  			 if link['target'] != source and \
									link['source'] != source]



	def nodePath(self, source: str) -> list[str] | None:
		"""
		Method to find the IDs of nodes (including topic node) needed to traverse to reach given node
		
		Returns None if no path found
		"""

		foundPath = None # To store final path

		# Make sure source exists
		if source not in self.getAllSources():
			return None

		# Iteratively search through topic links as starting point
		for link in self.topicLinks:
			startPath = [link['target']] # Path starts with topic node
			
			# Use helper method to recursively find path
			path = self.nodePathRecursive(link['source'], startPath[:], source)

			# Check if found
			if path != None:
				# Check if found a path before
				if foundPath != None:
					# Set foundPath to smallest of two
					if len(foundPath) > len(path):
						foundPath = path
				
				# Otherwise set newly found path
				else:
					foundPath = path
		
		# Return path (or None if not found)
		return foundPath



	def nodePathRecursive(self, currNode: str, path: list[str], target: str) -> list[str] | None:
		"""
		Helper method to recursively traverse the graph to find target node
		"""

		# Add this node to traversed
		path.append(currNode)

		# Base case to check if found target node
		if currNode == target:
			return path
		
		currSourceNode = self.sources[currNode] # Get current node attributes

		foundPath = None

		# Otherwise iterate through each neighbor and find 
		for neighbor in currSourceNode['neighbors']:
			if neighbor not in path: # Make sure not going in a circle
				recursivePath = self.nodePathRecursive(neighbor, path[:], target)

				# Check if found
				if recursivePath != None:
					# Check if foundPath exists
					if foundPath != None:
						# Set foundPath to smallest of two
						if len(foundPath) > len(recursivePath):
							foundPath = recursivePath

					# Otherwise set foundPath to newly found path
					else:
						foundPath = recursivePath
		
		# Return foundPath
		return foundPath
