import unittest
from datetime import datetime
from freezegun import freeze_time
from unittest.mock import MagicMock, patch
from src.parrot_blame import ParrotBlame, ParrotBlameInfo

mockdate = datetime(2000, 1, 1, 0, 0, 0)

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

    def test_initiation_creates_file(self):
        print("test_initiation_creates_file")

    def test_initiation_doesnt_override_existing_file(self):
        print("test_initiation_doesnt_override_existing_file")

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
        self.parrot_blame = ParrotBlame("file_path")
        self.parrot_blame._get_parrot_blame_information = MagicMock(return_value=parrot_blame_data)
        self.parrot_blame._save_parrot_blame_information = MagicMock()

    def test_blame_parrot(self):
        blame_parrot = self.parrot_blame.blame_parrot(":joy_parrot:",
                                                      "T001")

        self.parrot_blame._get_parrot_blame_information.assert_called()
        self.assertEqual(ParrotBlameInfo("joy_parrot",
                                         "TestUser",
                                         datetime.strptime("2018-07-24 20:35:43.687369",
                                                           "%Y-%m-%d %H:%M:%S.%f"),
                                         "T001"),
                         blame_parrot)

    def test_blame_parrot_with_colons(self):
        blame_parrot = self.parrot_blame.blame_parrot("sweat_smile_parrot",
                                                      "T003")

        self.parrot_blame._get_parrot_blame_information.assert_called()
        self.assertEqual(ParrotBlameInfo("sweat_smile_parrot",
                                         "AnotherUser",
                                         datetime.strptime("2018-07-10 20:35:43.687369",
                                                           "%Y-%m-%d %H:%M:%S.%f"),
                                         "T003"),
                         blame_parrot)

    def test_blame_parrot_without_entry(self):
        with self.assertRaises(ValueError) as val_err:
            self.parrot_blame.blame_parrot(":not_like_this_parrot:", "T001")

        self.parrot_blame._get_parrot_blame_information.assert_called()
        self.assertEqual("('The parrot :{parrot_name}: was not found in the blame information.', "
                         "'not_like_this_parrot')",
                         str(val_err.exception))

    def test_blame_parrot_without_team(self):
        with self.assertRaises(ValueError) as val_err:
            self.parrot_blame.blame_parrot(":joy_parrot:", "T003")

        self.parrot_blame._get_parrot_blame_information.assert_called()
        self.assertEqual("('The parrot :{parrot_name}: was not found in the blame information.', 'joy_parrot')",
                         str(val_err.exception))

    # @patch('src.parrot_blame.datetime.now')
    @freeze_time("2018-08-03")
    def test_create_blame_entry(self):
        self.parrot_blame.add_parrot_blame_information(":tick_parrot:",
                                                       "YetAnotherUser",
                                                       "T005")

        self.parrot_blame._get_parrot_blame_information.assert_called()
        self.parrot_blame._save_parrot_blame_information.assert_called_with([
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
            },
            {
                "parrot_name": "tick_parrot",
                "username": "YetAnotherUser",
                "created_date": str(datetime(2018, 8, 3)),
                "team_id": "T005"
            }
        ])

    def test_override_blame_entry(self):
        print("test_override_blame_entry")
