from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search import getTopics, subsites
from app.util.search.google import google
from app.util.search.siteMetadata import siteLocationAndName, siteMedium, siteTitle
from app.exceptions import FailedSearchException
from config import Config


class TopicalGraph(Graph):
	def __init__(self, query: str, depth: int) -> None:
		# Save attributes of inherited function
		super().__init__(query, 'topical', depth)



	def construct(self) -> None:
		"""
		Construct topical graph
		"""

		# Get topics
		self.createTopicNodes()
		
		# Iterate through topics and populate with sourceNodes
		for topic, topicNode in self.topicNodes.items():
			topicalQuery = f'{self.query} {topic}'

			sourceNodes: list[SourceNode] = [] # List of source nodes for this topic

			sourceNodeSites = google(topicalQuery)

			# Create source nodes for each site
			for site in sourceNodeSites:
				if 'wikipedia' not in site['Link']: # Don't add wikipedia
					# Check to see if site already exists
					if site['Link'] in list(self.sources.keys()):
						# Add this topic to the SourceNode
						self.sources[site['Link']].topics.append(topicNode.name)
						sourceNodes.append(self.sources[site['Link']])
					
					# Otherwise create new SourceNode
					else:
						# Get metadata for node (location & medium)
						info = siteLocationAndName(site['Link'])
						location = info['location']
						sourceName = info['sourceName']

						medium = siteMedium(site['Link'])

						# Create node
						node = SourceNode(site['Title'], site['Link'], sourceName, self.query, medium, location, [topic], [])
						sourceNodes.append(node)
						self.sources[site['Link']] = node # Add site to sources

						# Find neighbors
						node.neighbors = self.findNeighboringNodes(node)

						# Add link
						self.topicNodes[topic].sourceNodes.append(node)



	def createTopicNodes(self) -> dict[str, TopicNode]:
		"""
		Construct topic nodes
		"""

		topics = getTopics(self.query)

		self.topicNodes = {}

		# Make sure not too many topics
		if len(topics) > Config.MAX_TOPICS:
			topics = topics[:Config.MAX_TOPICS]

		# Go through each topic
		for topic in topics:
			topicNode = TopicNode(topic, [])
			self.topicNodes[topic] = topicNode

		return self.topicNodes
	

	def findNeighboringNodes(self, node: SourceNode, currDepth: int = 1) -> list[SourceNode]:
		"""
		Get neighboring SourceNodes
		"""

		# Base case
		if currDepth == self.depth:
			return None
		

		# Get neighboring sites
		neighboringSites = subsites(node.source, Config.MAX_SUBSITES)
		neighboringNodes = []

		for site in neighboringSites:
			if 'wikipedia' not in site: # Don't add wikipedia
				# Check if site already is a SourceNode
				if site in self.sources.values():
					neighboringNodes.append(self.sources[site])
					
					# If neighbor node doesn't already have the node's topics then add
					self.sources[site].neighbors = self.sources[site].neighbors + [topic for topic in node.topics if topic not in self.sources[site].neighbors]

				# Create new SourceNode
				else:
					# Get site title (if site inaccessible then go to next site)
					try:
						title = siteTitle(site)
					except FailedSearchException:
						continue

					# Get metadata (location/medium)
					location = siteLocationAndName(site)
					medium = siteMedium(site)

					# Create node
					neighbor = SourceNode(title, site, self.query, medium, location, node.topics)
					self.sources[site] = neighbor
					neighboringNodes.append(neighbor)
					
					# Recursively get node's neighbors
					neighbor.neighbors = self.findNeighboringNodes(neighbor, currDepth+1)
		
		return neighboringNodes
