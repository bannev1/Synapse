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
		topicNodes = Database().fetch(f'SELECT id, name FROM cacheTopicNodes WHERE graph={self.id}')


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
