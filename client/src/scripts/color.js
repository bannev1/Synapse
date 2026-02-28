// Function to aid coloring of nodes


// Assign color to topics
export const assignColorTopics = (topics) => {
	var coloredTopics = new Object() // Dictionary


	topics.forEach((topic) => {
		// Generate color (at upper spectrum of color)
		const randomColor = [
			Math.floor(Math.random() * 156 + 100), // R
			Math.floor(Math.random() * 156 + 100), // G
			Math.floor(Math.random() * 156 + 100) // B
		]

		// Assign topic
		coloredTopics[topic] = randomColor
	})

	return coloredTopics
}


// Convert RGB to Hex
const RGBtoHex = (RGB) => {
	const hex = RGB.map(component => {
		let hexVal = component.toString(16)

		if (hexVal.length == 1) // leading zero
			return '0' + hexVal
		
		return hexVal
	})

	return '#' + hex[0] + hex[1] + hex[2]
}


// Blend multiple colors
const blendRBGColors = (colors) => {
	// Get components of colors
	const Rs = colors.map(color => color[0])
	const Gs = colors.map(color => color[1])
	const Bs = colors.map(color => color[2])

	// Calculate averages
	const finalColor = [
		Rs.reduce((r1, r2) => r1 + r2) / Rs.length,
		Gs.reduce((g1, g2) => g1 + g2) / Gs.length,
		Bs.reduce((b1, b2) => b1 + b2) / Bs.length
	]

	// Convert to int
	return finalColor.map(component => Math.floor(component))
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
					coloredTopics[node.name],
					[100, 100, 100] // Darker color
				])
				
				// Convert color to hex
				node.color = RGBtoHex(color)
				break;

			case 'source':
				// Return grey if no topics associated
				if (node.topics == null || node.topics?.length == 0) {
					node.color = '#7d7d7d'
					break;
				}

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
