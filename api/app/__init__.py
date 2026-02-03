# Initialize Routes
from app.routes.routes import Routes
Routes()

# Import all routes
from app.routes import *


# Create App function
def application():
	Routes().registerBlueprints()

	return Routes().index # Return main route