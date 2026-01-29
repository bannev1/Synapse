from flask import Flask
from flask_cors import CORS
from app.models.database import Database

# Initialize Routes
from app.routes.routes import Routes
Routes()

# Import all routes
from app.routes import *


# Create App function
def application():
	Routes().registerBlueprints()

	return Routes().index # Return main route