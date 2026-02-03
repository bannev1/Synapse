from app.routes.routes import Routes

search = Routes().search


@search.route('/nodePath')
def nodePath() -> None:
	return
