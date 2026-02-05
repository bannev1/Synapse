# Run from /app as root
from app import *

app = application()

if __name__ == '__main__':
	# Run app (hupper -m waitress --port=8000 main:app)
	app.run(host="0.0.0.0", port=8000, debug=True)
