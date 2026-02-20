// Endpoints
const HOST = 'https://localhost:8000'

// Endpoints for search and graph functionality
export const GRAPH = {
	'search': `${HOST}/search`,
	'compare': `${HOST}/search/compare`,
	'nodeAdd': `${HOST}/search/nodeAdd`,
	'nodeDelete': `${HOST}/search/nodeDelete`,
	'path': `${HOST}/search/nodePath`
}

// Endpoints for saved graphs
export const SAVED = {
	'load': `${HOST}/share`,
	'post': `${HOST}/share`,
	'update': `${HOST}/share/save`
}
