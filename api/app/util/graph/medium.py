from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import google, googleSites
from app.util.search.siteMetadata import siteMedium, siteLocation, siteTitle
from config import Config


class MediumGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str]) -> None:
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'medium', depth, sites)



	def construct(self) -> None:
		"""
		Construct a medium-type graph
		"""

		mediums = {} # Store all main mediums with corresponding topic node
		
		# Get base SourceNodes (only sites)
		sourceSites = [source for value in googleSites(self.query, self.sites).values() for source in value]

		# Create SourceNodes
		for site in sourceSites:
			# Get metadata
			medium = siteMedium(site['Source'])
			location = siteLocation(site['Source'])

			# Create new SourceNode
			node = SourceNode(site['Title'], site['Source'], self.query, medium, location)
			
			# Check if topicnode for medium exists
			if medium in mediums.keys():
				mediums[medium].sourceNodes.append(node)

			# Otherwise create TopicNode
			else:
				mediums[medium] = TopicNode(medium, [])

			# Get neighboring SourceNodes recursively
			node.neighbors = self.findNeighboringNodes()


	def findNeighboringNodes(self, node, currDepth = 1):
		"""
		Get nodes neighbor for medium graph
		"""

		# Base case
		if currDepth == self.depth:
			return None
		


	def parse(self):
		return super().parse()
