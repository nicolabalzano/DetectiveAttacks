from typing import List
from stix2.v20 import CourseOfAction
from src.model.interfaceToMitre.mitreData.mitreAtlasData.container.AbstractAtlasContainer import AbstractAtlasContainer
from src.model.interfaceToMitre.mitreData.mitreAtlasData.utils.MitreAtlasUtils import get_uuid_from_string
from src.model.Singleton import singleton


@singleton
class MitigationsContainer(AbstractAtlasContainer):

    def __init__(self, dict_file: dict):
        self.dict_file = dict_file
        super().__init__(self.__define_all_mitigations())

    def __define_all_mitigations(self) -> List[CourseOfAction]:
        list_mitigations = []
        for mit in (self.dict_file['matrices'][0])['mitigations']:
            mitigation = CourseOfAction(
                type='course-of-action',
                id=f'course-of-action--{get_uuid_from_string(mit["id"])}',
                name=mit['name'],
                description=mit['description'],
                external_references=super()._get_external_refs(mit, 'mitigations')
            )
            list_mitigations.append(mitigation)

        return list_mitigations