from app.routes.routes import Routes

share = Routes().share


@share.update('/save/{id}')
def save(id: str) -> None:
	return
