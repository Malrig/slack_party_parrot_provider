import json
from datetime import datetime
from collections import namedtuple


class ParrotBlameInfo:
    def __init__(self, parrot_name: str, username: str, created_date: datetime, team_id: str):
        self.parrot_name = parrot_name
        self.username = username
        self.created_date = created_date
        self.team_id = team_id

    @classmethod
    def from_json(cls, json_entry: dict):
        if not all(key in json_entry for key in("parrot_name", "username", "created_date", "team_id")):
            raise ValueError("Dictionary did not contain one of; parrot_name, username, created_date or team_id.")
        return ParrotBlameInfo(json_entry["parrot_name"],
                               json_entry["username"],
                               datetime.strptime(json_entry["created_date"], "%Y-%m-%d %H:%M:%S.%f"),
                               json_entry["team_id"])

    def to_json(self):
        json_dict = {
            "parrot_name": self.parrot_name,
            "username": self.username,
            "created_date": str(self.created_date),
            "team_id": self.team_id
        }

        return json_dict

    def __eq__(self, other):
        return ((isinstance(other, ParrotBlameInfo)) and
                (self.parrot_name == other.parrot_name) and
                (self.username == other.username) and
                (self.created_date == other.created_date) and
                (self.team_id == other.team_id))


class ParrotBlame:
    def __init__(self,
                 parrot_blame_filename: str):
        self.parrot_blame_filename = parrot_blame_filename

    def add_parrot_blame_information(self,
                                     parrot_name: str,
                                     username: str,
                                     team_id: str):
        parrot_name = parrot_name.replace(":", "")

        current_info = self._get_parrot_blame_information()

        current_info.append(ParrotBlameInfo(parrot_name,
                                            username,
                                            datetime.now(),
                                            team_id).to_json())

        self._save_parrot_blame_information(current_info)

    def blame_parrot(self,
                     parrot_name: str,
                     team_id: str):
        parrot_name = parrot_name.replace(":", "")

        blame_info = self._get_parrot_blame_information()

        for blame_entry in blame_info:
            if ((blame_entry["parrot_name"] == parrot_name) and
                    (blame_entry["team_id"] == team_id)):
                return ParrotBlameInfo.from_json(blame_entry)

        raise ValueError("The parrot :{parrot_name}: was not found in the blame information.", parrot_name)

    def _get_parrot_blame_information(self):
        print("_get_parrot_blame_information")

    def _save_parrot_blame_information(self,
                                       parrot_blame_info: list):
        print("_add_parrot_blame_information")
