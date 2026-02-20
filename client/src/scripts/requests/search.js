// Methods to manage searches and graphs
import { GRAPH } from "./endpoints";


// Function to search and construct a graph
export const search = async (query, depth, graphType) => {
	const url = GRAPH['search']

	const body = {
		'query': query,
		'depth': depth,
		'type': graphType
	}

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		body: JSON.stringify(body)
	})

	const result = await response.json()

	// Check if error
	if (!response.ok) {
		console.log(`Failed construction of graph, server returned:\n${JSON.stringify(result)}`)
		
		return {
					'status': 'failed',
					'message': JSON.stringify(result)
				}
	}

	// Otherwise return result as graph (with status)
	result['status'] = 'success'
	return result
}


// Function to add a node
export const add = async (graph) => {
	const url = GRAPH['nodeAdd']

	const body = {
		'query': query,
		'depth': depth,
		'type': graphType
	}

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		body: JSON.stringify(body)
	})

	const result = await response.json()

	// Check if error
	if (!response.ok) {
		console.log(`Failed construction of graph, server returned:\n${JSON.stringify(result)}`)
		
		return {
					'status': 'failed',
					'message': JSON.stringify(result)
				}
	}

	// Otherwise return result as graph (with status)
	result['status'] = 'success'
	return result
}