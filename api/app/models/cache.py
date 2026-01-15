from app.models.graph import Graph
from app.models.database import Database
from app.exceptions import GraphNotFound


class CacheGraph(Graph):
	def __init__(self, query: str, graphType: str, depth: int, sites: list[str]) -> None:
		"""
		Model for cache graph
		"""

		# Convert sources to CSV format
		sources = ','.join(list(sorted(sites)))

		# Find graph
		graphID = Database().fetch(f"SELECT id FROM cache WHERE query={query} AND graphType={graphType} AND depth={depth} AND sources={sources};")

		# Check if any
		if len(graphID) != 1:
			raise GraphNotFound(f"No cached graph for {query=}, {graphType=}, {depth=}")
		
		self.id = graphID[0]
		
		# Save attributes of inherited function
		super(Graph, self).__init__(query, graphType, depth, sites)



	def construct(self) -> None: 
		"""
		Create cached graph links
		"""
		
		# Retrieve topic nodes and source nodes
		self.topicNodes = Database().fetch(f'SELECT id, name FROM cacheTopicNodes WHERE graph={self.id};')
		self.sourceNodes = Database().fetch(f'SELECT id, name, source, location, medium, topics FROM cacheSourceNodes WHERE graph={self.id};')
		
		# Retrieve links
		self.topicSourceLinks = Database().fetch(f'SELECT topicNode, sourceNode FROM cacheTopicSourceJoinTable WHERE graph={self.id};')
		self.sourceLinks = Database().fetch(f'SELECT sourceNode1, sourceNode2 FROM cacheSourceSourceJoinTable WHERE graph={self.id};')


	def parse(self) -> dict:
		"""
		Convert cached retrieved graph into dictionary format
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



	@staticmethod
	def saveCache(graph: Graph):
		"""
		Save graph to the Cache database
		"""


	@staticmethod
	def clearOldCache() -> None:
		"""
		Clear expired cache
		"""
