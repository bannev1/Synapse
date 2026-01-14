from app.models import Graph
from app.models.nodes import SourceNode, TopicNode


class LocationalGraph(Graph):
	def __init__(self, query: str, depth: int) -> None:
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'locational', depth)