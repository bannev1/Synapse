from app.routes.routes import Routes

search = Routes().search


@search.route('/nodeDelete')
def nodeDelete() -> None:
	return
