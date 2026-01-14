from app.routes.routes import Routes

share = Routes().share


@share.route('/save/{id}', methods=["UPDATE"])
def save(id: str) -> None:
	return
