'use client';

// Get autocomplete options
export default async ( query, maxOptions = 5 ) => {
	const url = `https://en.wikipedia.org/w/api.php?action=query&format=json&assert=anon&list=prefixsearch&formatversion=2&pssearch=${query}&pslimit=${maxOptions}}`

	const response = await fetch(url,
		{
			mode: 'cors',
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Accept': '*/*',
				'User-Agent': 'PostmanRuntime/7.44.1'
			}
		}
	);

	const data = await response.json();

	let pages = [];
	
	data['query']['prefixsearch'].forEach(page => {
		pages.push(page.title);
	});

	return pages;
}