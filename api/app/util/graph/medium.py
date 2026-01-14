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

		mediums = [] # Store all main mediums
		
		# Get base SourceNodes (only sites)
		sourceSites = [source for value in googleSites(self.query, self.sites).values() for source in value]

		# Create SourceNodes
		for site in sourceSites:
			# Get metadata
			medium = siteMedium(site['Source'])
			location = siteLocation(site['Source'])

			mediums.append(medium)

			# Create new SourceNode
			node = SourceNode(site['Title'], site['Source'], self.query, medium, location)

			# Get neighboring SourceNodes recursively


	def findNeighboringNodes(self, node, currDepth = 1):
		return super().findNeighboringNodes(node, currDepth)


	def parse(self):
		return super().parse()