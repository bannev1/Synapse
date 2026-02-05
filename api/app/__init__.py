import os
from dotenv import load_dotenv

# Initialize Routes
from app.routes.routes import Routes
Routes()

# Import all routes
from app.routes import *


# Create App function
def application():
	Routes().registerBlueprints()

	# Set up config/dotenv for locally run project
	envPath = os.path.join(os.getcwd(), '', '.env')
	if os.path.isfile(envPath):
		load_dotenv(envPath)

	return Routes().index # Return main route