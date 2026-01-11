from app.routes.routes import Routes

share = Routes().share


@share.post('/')
def post() -> None:
	return
