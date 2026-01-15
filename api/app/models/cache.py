from app.models.graph import Graph
from app.models.database import Database
from app.exceptions import GraphNotFound


class CacheGraph(Graph):
	def __init__(self, query: str, type: str, depth: int, sites: list[str]) -> None:
		"""
		Model for cache graph
		"""

		# Save attributes of inherited function
		super(Graph, self).__init__(query, type, depth, sites)



	def saveCache() -> None:
		"""
		Save this graph to the Cache database
		"""


	@staticmethod
	def retrieveCache(query: str, graphType: str, depth: int, sites: list[str]) -> 'CacheGraph':
		"""
		Retrieve CacheGraph
		"""

		# Convert sources to CSV format
		sources = ','.join(list(sorted(sites)))

		# Find graph
		graphID = Database().fetch(f"SELECT id FROM cache WHERE query={query} AND graphType={graphType} AND depth={depth} AND sources={sources};")

		# Check if any
		if len(graphID) == 0:
			raise GraphNotFound(f"No cached graph for {query=}, {graphType=}, {depth=}")
		


	@staticmethod
	def clearOldCache() -> None:
		"""
		Clear expired cache
		"""
