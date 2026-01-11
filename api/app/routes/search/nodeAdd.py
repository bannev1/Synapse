from app.routes.routes import Routes

search = Routes().search


@search.route('/nodeAdd')
def nodeAdd() -> None:
	return
