// Endpoints
const HOST = 'https://localhost:8000'

// Endpoints for search and graph functionality
export const GRAPH = {
	'search': `${HOST}/search`,
	'compare': `${HOST}/search/compare`,
	'nodeAdd': `${HOST}/search/nodeAdd`,
	'nodeDelete': `${HOST}/search/nodeDelete`,
	'path': `${HOST}/search/path`
}

// Endpoints for saved graphs
export const SAVED = {
	'load': `${HOST}`
}
