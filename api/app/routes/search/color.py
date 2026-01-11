from app.routes.routes import Routes

search = Routes().search


@search.route('/color')
def color() -> None:
	return
