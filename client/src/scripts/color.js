// Function to aid coloring of nodes


// Assign color to topics
export const assignColorTopics = (topics) => {
	var coloredTopics = new Object() // Dictionary

	topics.forEach((topic) => {
		// Generate color
		const randomHexInt = Math.floor(Math.random() * 16777215)
		const hexcolor = '#' + randomHexInt.toString(16).padStart(6, '0')

		// Assign topic
		coloredTopics[topic] = hexcolor
	})

	return coloredTopics
}


// Given the color assignments, color the nodes
export const colorNodes = (coloredTopics, nodes) => {

}
