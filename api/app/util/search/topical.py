# Code for getting topics and whatnot using the wikipedia API

import requests



# Get topics
def getTopics(query: str, amt: int = -1)-> list[str]:
	"""
	Get a list of topics given the topic/query
	
	:param query: Topic/query to get topics of
	:param amt: Amount of topics of query (max) to give, -1 for all
	:return: List of topics (string format)
	:rtype: list[str]
	"""