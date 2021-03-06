import json
import os
import logging
from datetime import datetime

logger = logging.getLogger()


class ParrotBlameInfo:
    def __init__(self, parrot_name: str, username: str, created_date: datetime, team_id: str) -> None:
        self.parrot_name = parrot_name
        self.username = username
        self.created_date = created_date
        self.team_id = team_id

    @classmethod
    def from_json(cls, json_entry: dict):
        if not all(key in json_entry for key in("parrot_name", "username", "created_date", "team_id")):
            logger.error("Failed to create ParrotBlameInfo from dictionary: %s.", json_entry)
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
                 data_dir_path: str) -> None:
        self._prepare_blame_file(data_dir_path)
        self.parrot_file_path = os.path.join(data_dir_path, "parrot_blame.json")

    @staticmethod
    def _prepare_blame_file(data_dir_path: str):
        logger.debug("Preparing blame data file at %s.", data_dir_path)
        parrot_file_path = os.path.join(data_dir_path, "parrot_blame.json")

        os.makedirs(os.path.dirname(parrot_file_path), exist_ok=True)

        if os.path.isfile(parrot_file_path):
            logger.debug("Existing blame file found, do not recreate.")
            return

        with open(parrot_file_path, 'w+') as new_json_file:
            logger.debug("No existing blame file found, create a new one.")
            json.dump([], new_json_file)

    def add_parrot_blame_information(self,
                                     parrot_name: str,
                                     username: str,
                                     team_id: str):
        parrot_name = parrot_name.replace(":", "")
        logger.debug("Adding blame information for parrot %s.", parrot_name)

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
        logger.debug("Getting blame information for parrot %s.", parrot_name)

        blame_info = self._get_parrot_blame_information()

        for blame_entry in blame_info:
            if ((blame_entry["parrot_name"] == parrot_name) and
                    (blame_entry["team_id"] == team_id)):
                logger.debug("Found blame entry for parrot %s: %s.", parrot_name, blame_entry)
                return ParrotBlameInfo.from_json(blame_entry)

        raise ValueError("No blame information for :%s: was found.", parrot_name)

    def _get_parrot_blame_information(self):
        with open(self.parrot_file_path, 'r') as blame_data:
            data = json.load(blame_data)

        return data

    def _save_parrot_blame_information(self,
                                       parrot_blame_info: list):
        with open(self.parrot_file_path, 'w') as blame_data:
            json.dump(parrot_blame_info, blame_data)
