from abc import ABC
from typing import List


class AbstractAtlasContainer(ABC):

    def __init__(self, objects: List):
        if not isinstance(objects, list):
            self._objects = list(objects)
        else:
            self._objects = objects

    def get_data(self):
        return self._objects

    def get_object_from_data_by_id(self, target_id: str):
        return next((obj for obj in self._objects if obj.id == target_id), None)

    def get_object_from_data_by_name(self, target_name: str):
        return [obj for obj in self._objects if target_name.lower() in obj.name.lower()]

    def _get_external_refs(self, obj_dict: dict, url_dir: str) -> List[dict]:
        external_refs = []
        """
        if "ATT&CK-reference" in obj_dict.keys():
            attack_ref = obj_dict["ATT&CK-reference"]
            external_refs.append({
                "source_name": "mitre_attack",
                "url": attack_ref['url'],
                "external_id": attack_ref['id']
            })
        else:
        """
        external_refs.append({
            "source_name": "mitre-atlas",
            "url": f"https://atlas.mitre.org/{url_dir}/{obj_dict['id']}",
            "external_id": obj_dict['id']
        })
        return external_refs
