from app.models.graph import Graph
from app.models.database import Database


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


	@staticmethod
	def clearOldCache() -> None:
		"""
		Clear expired cache
		"""

	
	@staticmethod
	def checkIDexists(id: str) -> bool:
		"""
		Check if ID exists in Cache database
		"""
