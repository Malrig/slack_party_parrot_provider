import unittest
from unittest.mock import MagicMock
from src.parrot_blame import ParrotBlame


class TestParrotBlame(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def test_blame_parrot(self):
        print("test_blame_parrot")

    def test_blame_parrot_without_entry(self):
        print("test_blame_parrot_no_entry")

    def test_create_blame_entry(self):
        print("test_create_blame_entry")

    def test_override_blame_entry(self):
        print("test_override_blame_entry")


class TestInitiationParrotBlame(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def test_initiation_creates_file(self):
        print("test_initiation_creates_file")

    def test_initiation_doesnt_override_existing_file(self):
        print("test_initiation_doesnt_override_existing_file")
