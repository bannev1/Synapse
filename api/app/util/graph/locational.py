from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import googleLocation
from app.util.search.siteMetadata import siteMedium, siteLocationAndName, siteTitle
from app.util.search import subsites
from app.exceptions import UnavailableLink
from config import Config


class LocationalGraph(Graph):
	def __init__(self, query: str, depth: int, locations: list[str] = Config.DEFAULT_LOCATIONS) -> None:
		# Save locations
		self.locationList = locations

		# Save attributes of inherited function
		super().__init__(query, 'locational', depth)

		


	def createTopicNodes(self, locations: list[str]) -> dict[str, TopicNode]:
		"""
		Create topic nodes given list of locational country codes
		"""

		topicNodes = {}

		for location in locations:
			topicNodes[location] = TopicNode(location, [])

		return topicNodes



	def construct(self) -> None:
		"""
		Construct a locational-type graph
		"""

		# Create topic nodes
		self.topicNodes = self.createTopicNodes(self.locationList) # For topic nodes

		# Get base SourceNodes (only sites)
		searchedSites = googleLocation(self.query, self.locationList)

		# Create SourceNodes
		for code in self.topicNodes.keys():
			for site in searchedSites[code]:
				# Get metadata
				medium = siteMedium(site['Link'])

				# Create new SourceNode
				node = SourceNode(site['Title'], site['Link'], site['Source'], self.query, medium, code, [code], [])

				self.topicNodes[code].sourceNodes.append(node)
				self.sources[node.source] = node

				# Get neighboring SourceNodes recursively
				node.neighbors = self.findNeighboringNodes(node)




	def findNeighboringNodes(self, node: SourceNode, currDepth: int = 1) -> list[SourceNode]:
		"""
		Get nodes neighbor for medium graph
		"""

		# Base case
		if currDepth == self.depth:
			return []
		
		# Get neighboring sources
		neighborSites = subsites(node.source, Config.MAX_SUBSITES)
		neighborNodes = []
		
		for site in neighborSites:
			# Check if source already exists
			if site in list(self.sources.keys()):
				neighborNodes.append(self.sources[site])
			
			# Create new source
			else:
				try:
					# Get metadata
					title = siteTitle(site)
					medium = siteMedium(site)

					info = siteLocationAndName(site)
					location = info['location']
					sourceName = info['sourceName']


					# Merge topics
					topics = list(set(node.topics + [location])) # Also remove duplicates

					# Create node
					newNode = SourceNode(title, site, sourceName, self.query, medium, location, topics, [])

					self.sources[site] = newNode

					# Determine if can link to TopicNode
					if location in self.locationList:
						self.topicNodes[location].sourceNodes.append(newNode)

					# Get neighboring nodes
					newNode.neighbors = self.findNeighboringNodes(newNode, currDepth+1)
				
				# If failed, means link unavailable and skip
				except UnavailableLink:
					continue

		return neighborNodes
