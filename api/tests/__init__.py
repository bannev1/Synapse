# Run tests
import unittest

 
# UnitTest module config
unittest.TestLoader.sortTestMethodsUsing = None

# Import files
from tests.database import TestDatabase
from tests.graph import TestGraph
from tests.cache import TestCache
from tests.save import TestSave
