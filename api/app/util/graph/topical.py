from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.topical import getTopics
from app.util.search.google import googleSites
from app.util.search.siteMetadata import siteLocation, siteMedium


class TopicalGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str]) -> None:
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'topical', depth, sites)



	def construct(self) -> None:
		"""
		Construct topical graph
		"""

		# Get topics
		self.createTopicNodes()
		
		# Iterate through topics and populate with sourceNodes


	def createTopicNodes(self) -> list[TopicNode]:
		"""
		Construct topic nodes
		"""

		topics = getTopics(self.query)

		for topic in topics:



	def parse(self): # Inherit parse method
		return super().parse()