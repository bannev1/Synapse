from app.routes.routes import Routes

share = Routes().share


@share.get('/')
def get() -> None:
	return
