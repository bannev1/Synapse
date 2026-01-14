from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search import getTopics, subsites
from app.util.search.google import google, googleSites
from app.util.search.siteMetadata import siteLocation, siteMedium
from config import Config


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
		for topicNode in self.topicNodes:
			topicalQuery = f'{self.query} {topicNode.name}'

			sourceNodes: list[SourceNode] = [] # List of source nodes for this topic
			sourceNodeSites: list[str] = None

			# Check if need to get all sites or just one site
			if len(self.sites) > 0:
				# Only get sources/titles no need by site
				sourceNodeSites = [source for value in googleSites(topicalQuery, self.sites).values() for source in value]
			else:
				sourceNodeSites = google(topicalQuery, amtResults=Config.AMT_RESULTS_TOPICAL)

			# Create source nodes for each site
			for site in sourceNodeSites:
				# Check to see if site already exists
				if site in self.sources.keys():
					# Add this topic to the SourceNode
					self.sources[site].topics.append(topicNode.name)
					sourceNodes.append(self.sources[site])
				
				# Otherwise create new SourceNode
				else:
					# Get metadata for node (location & medium)
					location = siteLocation(site)
					medium = siteMedium(site)

					# Create node
					node = SourceNode(site['Title'], site['Source'], self.query, [topicNode.name], medium, location)
					sourceNodes.append(node)
					self.sources[site] = node # Add site to sources

					# Find neighbors
					node.neighbors = self.findNeighboringNodes(node)


	def createTopicNodes(self) -> list[TopicNode]:
		"""
		Construct topic nodes
		"""

		topics = getTopics(self.query)

		self.topicNodes = []

		# Go through each topic
		for topic in topics:
			topicNode = TopicNode(topic, [])
			self.topicNodes.append(topicNode)

		return self.topicNodes
	

	def findNeighboringNodes(self, node: SourceNode) -> list[SourceNode]:
		"""
		Get neighboring SourceNodes
		"""


	def parse(self): # Inherit parse method
		return super().parse()