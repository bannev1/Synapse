from app.routes.routes import Routes

search = Routes().search


@search.route('/compare')
def compare() -> None:
	return
