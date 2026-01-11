class Node:
	def __init__(self, 
			  	name: str, 
				color: tuple[int], 
				neighbors: tuple['Node']
			) -> None:
		self.name: str = name
		self.color: tuple[int] = color
		self.neighbors: tuple['Node'] = neighbors
