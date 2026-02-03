from app.models.graph import Graph


class RequestGraph(Graph):
	def __init__(self, graph: dict | None) -> None:
		"""
		Graph class/model to specifically handle JSON format graphs (from requests)
		"""

		# Set graph
		self.graph = graph

		# Save attributes of inherited method if graph not None otherwise run construct method
		if graph != None:
			super(RequestGraph, self).__init__(graph['name'], graph['type'], graph['depth'], graph['sources'])
		else:
			self.construct()

			# Save attributes after graph constructed
			super(RequestGraph, self).__init__(graph['name'], graph['type'], graph['depth'], graph['sources'])



	def construct(self) -> None:
		"""
		Redundant method, overriding to avoid NotImplemented error
		"""

		return



	def parse(self):
		"""
		Parse graph in JSON format
		"""

		# Create base graph
		self.graph = {
			'name': self.query,
			'type': self.type,
			'depth': self.depth,
			'topics': [],
			'sources': [],
			'topicLinks': [],
			'sourceLinks': []
		}

		# Retrieve topicNodes
		topics = {}
		for topic in self.topicNodes:
			topics[topic['id']] = topic['name']
			
		self.graph['topics'] = list(topics.values())

		# Retrieve sourceNodes
		sources = {}
		for source in self.sourceNodes:
			# Add node as dictionary
			sources[source['id']] = {
				'source': source['source'],
				'name': source['name'],
				'topics': source['topics'].split(','), # Convert CSV to list object
				'medium': source['medium'],
				'location': source['location'],
				'neighbors': []
			}

		# Make topic to source links
		for topicLink in self.topicSourceLinks:
			self.graph['topicLinks'].append({
				'target': topics[topicLink['topicNode']],
				'source': sources[topicLink['sourceNode']]['source']
			})
		
		# Make source links
		for sourceLink in self.sourceLinks:
			node1 = sources[sourceLink['sourceNode1']]
			node2 = sources[sourceLink['sourceNode2']]

			self.graph['sourceLinks'].append({
				'target': node1['source'],
				'source': node2['source']
			})

			# Add as neighbor
			node1['neighbors'].append(node2['source'])

		# Add to main graph
		self.graph['sources'] = list(sources.values())

		return self.graph


