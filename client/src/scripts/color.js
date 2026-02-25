// Function to aid coloring of nodes


// Assign color to topics
export const assignColorTopics = (topics) => {
	var coloredTopics = new Object() // Dictionary

	topics.forEach((topic) => {
		// Generate color
		const randomColor = [
			Math.floor(Math.random() * 256), // R
			Math.floor(Math.random() * 256), // G
			Math.floor(Math.random() * 256) // B
		]

		// Assign topic
		coloredTopics[topic] = randomColor
	})

	return coloredTopics
}


// Convert RGB to Hex
const RGBtoHex = (RGB) => {

} 


// Blend multiple colors
const blendRBGColors = (colors) => {

}


// Given the color assignments, color the nodes
export const colorNodes = (coloredTopics, nodes) => {
	const coloredNodes = nodes.map((node) => {
		switch (node.group) {
			case 'title':
				node.color = '#201e1f' // Pre-defined
				break;
			
			case 'topic':
				// Darken
				let color = blendRBGColors([
					coloredTopics[node.id],
					[50, 50, 50] // Darker color
				])
				
				// Convert color to hex
				node.color = RGBtoHex(color)
				break;

			case 'source':
				// Get all associated colors
				let colorList = node.topics.map(topic => coloredTopics[topic]) 

				// Blend and convert color to hex
				node.color = RGBtoHex(blendRBGColors(colorList))
				break;
		}

		return node
	})

	return coloredNodes
}
