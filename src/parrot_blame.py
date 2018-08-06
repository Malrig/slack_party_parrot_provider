import json
from datetime import datetime
from collections import namedtuple

ParrotBlameInfo = namedtuple('ParrotBlameObj', [
    "parrot_name",
    "username",
    "created_date",
    "team_id"
])


class ParrotBlame:
    def __init__(self,
                 parrot_blame_filename: str):
        self.parrot_blame_filename = parrot_blame_filename

    def add_parrot_blame_information(self,
                                     parrot_name: str,
                                     username: str,
                                     team_id: str):
        current_info = self._get_parrot_blame_information()

        current_info.append(ParrotBlameInfo(parrot_name,
                                            username,
                                            team_id,
                                            datetime.now()))

        self._save_parrot_blame_information(current_info)

    def blame_parrot(self,
                     parrot_name: str,
                     team_id: str):
        blame_info = self._get_parrot_blame_information()

        for blame_entry in blame_info:
            if ((blame_entry["parrot_name"] == parrot_name) and
                    (blame_entry["team_id"] == team_id)):
                return blame_entry

        raise ValueError("The parrot :{parrot_name}: was not found in the blame information."
                            .format(parrot_name=parrot_name))

    def _get_parrot_blame_information(self):
        print("_get_parrot_blame_information")

    def _add_parrot_blame_information(self,
                                      parrot_blame_info: list):
        print("_add_parrot_blame_information")
