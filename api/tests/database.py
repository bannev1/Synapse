# Test for database to ensure configured properly
import unittest

from app.models import Database
from app.routes import Routes


class TestDatabase(unittest.TestCase):
	def test_connection(self):
		"""Test can connect to database with credentials"""

		def connect():
			# Set up routes/Flask config first
			Routes()
			db = Database()

			# Run test connection
			conn = db.get_connection()
			cursor = conn.cursor()
			cursor.close()
			db.release_connection(conn)

		# Assert connect function works
		failed = False
		try:
			connect()
		except:
			failed = True
		
		self.assertFalse(failed, 'Exception raised when connecting to database')