from app.routes.routes import Routes

search = Routes().search


"""
Route Request Structure:
{
	'query': 'My Query/Topic',
	'sites': [
		'https://www.website1.com',
		'https://www.website2.com',
		...
	],
	'type': 'topical' | 'medium' | 'locational',
	'depth': 5
}
"""


@search.route('/construct')
def construct() -> None:
	return
