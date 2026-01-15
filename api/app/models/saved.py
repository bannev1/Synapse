from app.models.graph import Graph
from app.models.database import Database
from app.exceptions import GraphNotFound


class SavedGraph(Graph):
	def __init__(self, query: str, type: str, id: str) -> None:
		"""
		Model for saved ID graphs
		"""
		
		# Save attributes of inherited function
		super(Graph, self).__init__(query, type, -1, [])

		# Save own attributes
		self.id = id



	def save() -> None:
		"""
		Save this graph to the Saved database
		"""



	def update() -> None:
		"""
		Update the database at this graph's ID with its new/updated attributes
		"""


	@staticmethod
	def retrieveByID(id: str) -> 'SavedGraph':
		"""
		Retrieve SavedGraph
		"""

		# Find graph
		graph = Database().fetch(f"SELECT name, graphType, sources WHERE id={id};")

		if len(graph) != 1:
			raise GraphNotFound(f"SavedGraph database does not contain a record for a graph with ID {id}")

	
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
