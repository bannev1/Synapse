from app.models import Graph
from app.models.nodes import SourceNode, TopicNode


class LocationalGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str]) -> None:
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'locational', depth, sites)


	def parse(self):
		return super().parse()