from app.routes.routes import Routes

search = Routes().search


@search.route('/list')
def list() -> None:
	return
