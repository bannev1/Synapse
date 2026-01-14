from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import googleLocation
from app.util.search.siteMetadata import siteMedium, siteLocation, siteTitle
from app.util import convertCodeToCountry


class LocationalGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str], locations: list[str] = ['us', '']) -> None:
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'locational', depth, sites)

		
		# Custom attribute for this class
		self.locations = self.createTopicNodes(locations)



	def createTopicNodes(self, locations: list[str]) -> dict[str, TopicNode]:
		"""
		Create topic nodes given list of locational country codes
		"""

		topicNodes = []

		for location in locations:
			countryName = convertCodeToCountry(location)
			topicNodes.append(TopicNode(countryName, []))

		return topicNodes



	def construct(self) -> None:
		"""
		Construct a medium-type graph
		"""
		
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
			if medium in self.mediums.keys():
				self.mediums[medium].sourceNodes.append(node)

			# Otherwise create TopicNode
			else:
				self.mediums[medium] = TopicNode(medium, [])

			self.sources[node.source] = node

			# Get neighboring SourceNodes recursively
			node.neighbors = self.findNeighboringNodes(node)


	def findNeighboringNodes(self, node: SourceNode, currDepth: int = 1) -> list[SourceNode] | None:
		"""
		Get nodes neighbor for medium graph
		"""

		# Base case
		if currDepth == self.depth:
			return None
		
		# Get neighboring sources
		neighborSites = subsites(node.source)
		neighborNodes = []
		
		for site in neighborSites:
			# Check if source already exists
			if site in self.sources.keys():
				neighborNodes.append(self.sources[site])
			
			# Create new source
			else:
				# Get metadata
				medium = siteMedium(site)
				location = siteLocation(site)
				title = siteTitle(site)

				# Create node
				newNode = SourceNode(title, site, self.query, medium, location)

				self.sources[site] = newNode

				# Determine if can link to TopicNode
				if medium in self.mediums.keys():
					self.mediums[medium].sourceNodes.append(newNode)

				# Get neighboring nodes
				newNode.neighbors = self.findNeighboringNodes(newNode, currDepth+1)


	def parse(self):
		return super().parse()