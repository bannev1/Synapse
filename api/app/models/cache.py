from app.models.requestGraph import RequestGraph
from app.models.database import Database
from app.exceptions import GraphNotFound


class CacheGraph(RequestGraph):
	def __init__(self, query: str, graphType: str, depth: int) -> None:
		"""
		Model for cache graph
		"""

		# Find graph
		graphID = Database().fetch(f"SELECT id FROM cache WHERE query={query} AND graphType={graphType} AND depth={depth};")

		# Check if any
		if len(graphID) <= 0:
			raise GraphNotFound(f"No cached graph for {query=}, {graphType=}, {depth=}")
		
		self.id = graphID[0]
		
		# Save attributes of inherited function
		super().__init__({
			'name': query,
			'type': graphType,
			'depth': depth
		})



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

		# Clear old cache
		self.clearOldCache()


	
	def parse(self) -> dict:
		"""
		Convert cached retrieved graph into dictionary format
		"""

		return super().parse()



	@staticmethod
	def saveCache(graph: RequestGraph) -> None:
		"""
		Save graph to the Cache database
		"""

		# Parse graph
		parsed = graph.parse()

		# Save base graph
		graphID = Database().modifyAndReturn(f"""
			INSERT INTO cache (query, graphType, depth) 
			VALUES ({graph.query}, {graph.type}, {graph.depth}) 
			RETURNING id;""")['id']

		# Save all sourceNodes
		sourceNodes = {} # Dict of (source, id)

		for node in parsed['sources']:
			nodeTopics = ','.join(node['topics']) 
			nodeID = Database().modifyAndReturn(f"""
				INSERT INTO cacheSourceNodes (graph, name, source, sourceName, location, medium, topics)
				VALUES ({graphID}, {node['name']}, {node['source']}, {node['sourceName']}, {node['location']}, {node['medium']}, {nodeTopics})
				RETURNING id;""")['id']
			
			sourceNodes[node['source']] = nodeID
		
		
		# Save all topic nodes
		topicNodes = {} # Dict of (topic, id)
		
		for topic in parsed['topics']:
			topicID = Database().modifyAndReturn(f"""
				INSERT INTO cacheTopicNodes (graph, name)
				VALUES ({graphID}, {topic})
				RETURNING id;""")['id']
			
			topicNodes[topic] = topicID

		# Save topic-source links
		for link in parsed['topicLinks']:
			topicID = topicNodes[link['target']]
			sourceID = sourceNodes[link['source']]

			Database().modify(f"""
							INSERT INTO cacheTopicSourceJoinTable (graph, topicNode, sourceNode)
					 		VALUES ({graphID}, {topicID}, {sourceID});""")

		# Save source-source links
		for link in parsed['sourceLinks']:
			node1 = sourceNodes[link['target']]
			node2 = sourceNodes[link['source']]

			Database().modify(f"""
							INSERT INTO cacheSourceSourceJoinTable (graph, sourceNode1, sourceNode2)
					 		VALUES ({graphID}, {node1}, {node2});""")


	@staticmethod
	def clearOldCache() -> None:
		"""
		Clear expired cache
		"""

		# Remove 30 day old records from cache (as cascade set so others will delete subsequently)
		Database().modify("DELETE FROM cache WHERE STR_TO_DATE(timestamp,%Y-%m-%d %H:%M:%S) < (NOW() - INTERVAL 30 DAY);")
