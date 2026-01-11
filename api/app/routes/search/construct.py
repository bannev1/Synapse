from app.routes.routes import Routes

search = Routes().search


@search.route('/construct')
def construct() -> None:
	return
