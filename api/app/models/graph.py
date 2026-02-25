from typing_extensions import Literal
from abc import abstractmethod

from app.models.nodes import Node, SourceNode, TopicNode


class Graph:
	def __init__(self, query: str, type: Literal['topical', 'medium', 'locational'], depth: int) -> None:
		"""
		Graph Base Class
		"""

		# Set attributes
		self.query: str = query
		self.type: Literal['topical', 'medium', 'locational'] = type
		self.depth: int = depth

		# Define attributes which will be set later
		self.topicNodes: list[TopicNode] = [] # List of all topicnodes (linked to sourceNodes)
		self.sources: dict[str, SourceNode] = {} # List of all sources (str URLs) and their corresponding SourceNode

		# Construct graph
		self.construct()



	@abstractmethod
	def construct(self) -> Node:
		"""
		Construct a graph of this class
		"""
		raise NotImplementedError("construct() method not implemented") # Raise error if not implemented
	

	@abstractmethod
	def findNeighboringNodes(self, node: SourceNode, currDepth: int = 1) -> list[SourceNode]:
		"""
		Find neighboring nodes given a SourceNode
		"""
		raise NotImplementedError("findNeighboringNodes() method not implemented") # Raise error if not implemented



	def parse(self) -> dict:
		"""
		Universal method to parse the graph into a dictionary format to send as a request
		"""

		# Create base graph
		self.graph = {
			'name': self.query,
			'type': self.type,
			'depth': self.depth,
			'topics': [topic for topic in self.topicNodes.keys()], # Get each topic by name as string
			'sources': [],
			'topicLinks': [],
			'sourceLinks': []
		}

		# Go through each topic node and recursively get sources + sourceNode Links
		self.traversed = [] # list of sources traversed (str to keep less memory)

		for topic in self.topicNodes.values():
			for source in topic.sourceNodes:
				# Create link between source and topic nodes
				self.graph['topicLinks'].append({
						'target': topic.name,
						'source': source.source
					})

				# Traverse sourceNode
				self.parseSourceNodes(source)

		self.graph['sourceLinks'] = self.traversed

		return self.graph



	def parseSourceNodes(self, node: SourceNode) -> None:
		"""
		Parse source nodes recursively to get links and sources
		"""

		# Add current node
		self.traversed.append(node.source)

		nodeDict = dict(node)
		nodeDict['id'] = node.source # Set ID
		self.graph['sources'].append(nodeDict)

		# Find links
		links = []

		for neighbor in node.neighbors:
			links.append({
					'target': node.source,
					'source': neighbor.source
				})

			# Recursively traverse neighbor if not yet added
			if neighbor.source not in self.traversed:
				self.parseSourceNodes(neighbor)


		# Add links
		self.graph['sourceLinks'].extend(links)
