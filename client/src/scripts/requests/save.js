import { SAVED } from "./endpoints";

// Methods to save/share graphs

// Function to upload (post) a graph and return its ID
export const uploadGraph = async (graph) => {
	const url = SAVED['post'];

	const body = {
		'graph': graph
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
		console.log(`Failed to upload graph, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['id'];
};

// Function to update an existing graph at a given ID
export const updateGraph = async (id, graph) => {
	const url = `${SAVED['update']}/${id}`;

	const body = {
		'graph': graph
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
		console.log(`Failed to update graph at ${id}, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return 'success';
};

// Function to load a graph by its ID
export const loadGraph = async (id) => {
	const url = `${SAVED['load']}/${id}`;

	// Make request to server
	const response = await fetch(url, {
		method: 'GET'
	});

	const result = await response.json();

	// Check if error
	if (result['status'] === 'error') {
		console.log(`Failed to load graph at ${id}, server returned:\n${JSON.stringify(result)}`);
		
		return 'error';
	}

	return result['graph'];
};
