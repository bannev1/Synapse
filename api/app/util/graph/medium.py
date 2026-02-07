from app.models import Graph
from app.models.nodes import SourceNode, TopicNode
from app.util.search.google import google
from app.util.search.siteMetadata import siteMedium, siteLocation, siteTitle
from app.util.search import subsites


class MediumGraph(Graph):
	def __init__(self, query: str, depth: int, sites: list[str]) -> None:
		# Save attributes of inherited function
		super().__init__(query, 'medium', depth, sites)

		# Custom attribute for this class
		self.mediums = {} # Store all main mediums with corresponding topic node



	def construct(self) -> None:
		"""
		Construct a medium-type graph
		"""
		
		# Get base SourceNodes (only sites)
		sourceSites = google(self.query, self.sites).values()

		# Create SourceNodes
		for site in sourceSites:
			# Get metadata
			medium = siteMedium(site['Link'])
			location = siteLocation(site['Link'])

			# Create new SourceNode
			node = SourceNode(site['Title'], site['Link'], site['Source'], self.query, medium, location)
			
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
