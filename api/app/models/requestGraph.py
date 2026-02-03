from app.models.graph import Graph
from app.util.search import subsites
from app.util.search.siteMetadata import siteLocation, siteMedium, siteTitle


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
			self.graph = {}
			self.construct() # Construct graph

		# Add base parts
		self.graph['topics'] = []
		self.graph['sources'] = []

		self.sourceNodes = []
		self.topicNodes = []

		# Parse/construct graph
		self.parse()



	def construct(self) -> None:
		"""
		Redundant method, overriding to avoid NotImplemented error
		"""

		return



	def parse(self):
		"""
		Parse graph in JSON format
		"""


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

		# Clear graph
		self.graph['topicLinks'] = []
		self.graph['sourceLinks'] = []

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



	def addNode(self, source: str) -> None:
		"""
		Method to add a node by its URL
		"""

		name = siteTitle(source)
		location = siteLocation(source)
		medium = siteMedium(source)
		topics = []
		neighbors = []

		subsources = subsites(source)

		# Make links (if any)
		for subsource in subsources:
			if subsource in self.sites:
				# Add link
				self.graph['sourceLinks'].append({
					'target': subsource,
					'source': source
				})

				neighbors.append(subsource)

				# Add to neighbor
				for i, sourceNode in enumerate(self.sourceNodes):
					if sourceNode['source'] == subsource:
						self.sourceNodes[i]['neighbors'] += f',{source}'

						topics.append(sourceNode['topics'].split(',')) # Add topics

		# Add node to sourceNodes
		self.sourceNodes.append({
			'source': source,
			'name': name,
			'location': location,
			'medium': medium,
			'topics': ','.join(list(set(topics))),
			'neighbors': neighbors
		})
