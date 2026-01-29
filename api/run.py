import os
from dotenv import load_dotenv

# Run from /app as root
from app import application

app = application()

if __name__ == '__main__':
	# Set up config/dotenv for locally run project
	envPath = os.path.join(os.getcwd(), '.env')
	if os.path.isfile(envPath):
		load_dotenv(envPath)

	# Run app
	app.run(host="0.0.0.0", port=8080, debug=True)
