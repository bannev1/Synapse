from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import googleLocation
from app.util.search.siteMetadata import siteMedium, siteLocation, siteTitle
from app.util.search import subsites
from app.util import convertCodeToCountry
from config import Config


class LocationalGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str], locations: list[str] = ['us', '']) -> None:
		# Custom attribute for this class
		self.locations = self.createTopicNodes(locations)
		
		# Save attributes of inherited function
		super(Graph, self).__init__(query, 'locational', depth, sites)



	def createTopicNodes(self, locations: list[str]) -> dict[str, TopicNode]:
		"""
		Create topic nodes given list of locational country codes
		"""

		topicNodes = {}

		for location in locations:
			countryName = convertCodeToCountry(location)
			topicNodes[location] = [TopicNode(countryName, [])]

		return topicNodes



	def construct(self) -> None:
		"""
		Construct a locational-type graph
		"""
		
		# Get base SourceNodes (only sites)
		searchedSites = googleLocation(self.query, self.locations.keys(), amtResults=Config.AMT_RESULTS_LOCATIONAL)

		# Create SourceNodes
		for code, location in self.locations.items():
			for site in searchedSites[code]:
				# Get metadata
				medium = siteMedium(site['Source'])

				# Create new SourceNode
				node = SourceNode(site['Title'], site['Source'], self.query, medium, location)

				self.locations[code].sourceNodes.append(node)
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
				if location in self.locations.keys():
					self.locations[location].sourceNodes.append(newNode)

				# Get neighboring nodes
				newNode.neighbors = self.findNeighboringNodes(newNode, currDepth+1)


	def parse(self):
		return super().parse()