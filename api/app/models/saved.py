from app.models.graph import Graph
from app.models.database import Database


class SavedGraph(Graph):
	def __init__(self, query: str, type: str, depth: int, sites: list[str], id: str) -> None:
		"""
		Model for saved ID graphs
		"""
		
		# Save attributes of inherited function
		super(Graph, self).__init__(query, type, depth, sites)



	def save() -> str:
		"""
		Save this graph to the Saved database and return its ID
		"""



	def update() -> str:
		"""
		Update the database at this graph's ID with its new/updated attributes
		"""


	@staticmethod
	def retrieveByID(id: str) -> 'SavedGraph':
		"""
		Retrieve SavedGraph
		"""

	
	@staticmethod
	def checkIDexists(id: str) -> bool:
		"""
		Check if ID exists in SavedGraph database
		"""


	
	@staticmethod
	def createID() -> str:
		"""
		Method to generate a new SavedGraph ID
		"""
