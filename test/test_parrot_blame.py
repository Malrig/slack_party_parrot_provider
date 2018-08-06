import unittest
from unittest.mock import MagicMock
from src.parrot_blame import ParrotBlame, ParrotBlameInfo

parrot_blame_data = [
    {
        "parrot_name": "joy_parrot",
        "username": "TestUser",
        "created_date": "2018-07-24 20:35:43.687369",
        "team_id": "T001"
    },
    {
        "parrot_name": "sweat_smile_parrot",
        "username": "AnotherUser",
        "created_date": "2018-07-10 20:35:43.687369",
        "team_id": "T003"
    }
]


class TestParrotBlameWithFile(unittest.TestCase):
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


class TestParrotBlameWithoutFile(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.parrot_blame = ParrotBlame("file_path")
        self.parrot_blame._get_parrot_blame_information = MagicMock(return_value=parrot_blame_data)
        self.parrot_blame._add_parrot_blame_information = MagicMock()

    def test_initiation_creates_file(self):
        print("test_initiation_creates_file")

    def test_initiation_doesnt_override_existing_file(self):
        print("test_initiation_doesnt_override_existing_file")

    def test_blame_parrot(self):
        blame_parrot = self.parrot_blame.blame_parrot("joy_parrot",
                                                      "T001")

        self.assertEqual(ParrotBlameInfo(parrot_name="joy_parrot",
                                         username="TestUser",
                                         created_date="2018-07-24 20:35:43.687369",
                                         team_id="T001"),
                         blame_parrot)
        self.parrot_blame._get_parrot_blame_information.assert_called()

    def test_blame_parrot_without_entry(self):
        self.assertRaises(ValueError, self.parrot_blame.blame_parrot, "sweat_smile_parrot", "T001")
        self.parrot_blame._get_parrot_blame_information.assert_called()

    def test_create_blame_entry(self):
        print("test_create_blame_entry")

    def test_override_blame_entry(self):
        print("test_override_blame_entry")
