// Methods to manage searches and graphs
import { GRAPH } from "./endpoints";


// Function to search and construct a graph
export const search = async (query, depth, graphType) => {
	const url = GRAPH['search'];

	const body = {
		'query': query,
		'depth': depth,
		'type': graphType
	};

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed construction of graph, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['graph'];
};

// Function to create a compare graph
export const compare = async (graph1, graph2) => {
	const url = GRAPH['compare'];

	const body = {
		'graph1': graph1,
		'graph2': graph2
	};

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed to compare graphs, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['graph'];
};

// Function to add a node
export const addNode = async (graph, source) => {
	const url = GRAPH['nodeAdd'];

	const body = {
		'graph': graph,
		'source': source
	};

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed to add node, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['graph'];
};

// Function to delete a node
export const deleteNode = async (graph, source) => {
	const url = GRAPH['nodeDelete'];

	const body = {
		'graph': graph,
		'source': source
	};

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed to delete node, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['graph'];
};

// Function to find node path
export const findPath = async (graph, source) => {
	const url = GRAPH['path'];

	const body = {
		'graph': graph,
		'source': source
	};

	// Make request to server
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed to find path, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['path'];
};
