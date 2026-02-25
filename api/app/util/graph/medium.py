from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import google
from app.util.search.siteMetadata import siteMedium, siteLocationAndName, siteTitle
from app.util.search import subsites
from config import Config


class MediumGraph(Graph):
	def __init__(self, query: str, depth: int) -> None:
		# Save attributes of inherited function
		super().__init__(query, 'medium', depth)

		# Custom attribute for this class
		self.mediums = {} # Store all main mediums with corresponding topic node



	def construct(self) -> None:
		"""
		Construct a medium-type graph
		"""
		
		# Get base SourceNodes (only sites)
		sourceSites = google(self.query)

		# Create SourceNodes
		for site in sourceSites:
			# Get metadata
			info = siteLocationAndName(site['Link'])
			location = info['location']
			sourceName = info['sourceName']
			
			medium = siteMedium(site['Link'])

			# Create new SourceNode
			node = SourceNode(site['Title'], site['Link'], sourceName, self.query, medium, location)
			
			# Check if topicnode for medium exists
			if medium in list(self.mediums.keys()):
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
		neighborSites = subsites(node.source, Config.MAX_SUBSITES)
		neighborNodes = []
		
		for site in neighborSites:
			# Check if source already exists
			if site in list(self.sources.keys()):
				neighborNodes.append(self.sources[site])
			
			# Create new source
			else:
				# Get metadata
				info = siteLocationAndName(site)
				location = info['location']
				sourceName = info['sourceName']

				medium = siteMedium(site)
				title = siteTitle(site)

				# Create node
				newNode = SourceNode(title, site, sourceName, self.query, medium, location)

				self.sources[site] = newNode

				# Determine if can link to TopicNode
				if medium in list(self.mediums.keys()):
					self.mediums[medium].sourceNodes.append(newNode)

				# Get neighboring nodes
				newNode.neighbors = self.findNeighboringNodes(newNode, currDepth+1)


	def parse(self):
		return super().parse()
