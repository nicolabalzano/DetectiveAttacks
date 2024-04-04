import datetime
from typing import List
from stix2.v20 import Relationship
from src.domain.Singleton import singleton
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.AbstractAtlasContainer import AbstractAtlasContainer
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.utils.MitreAtlasUtils import get_uuid_from_string


@singleton
class RelationshipsContainer(AbstractAtlasContainer):

    def __init__(self, dict_file: dict):
        self.dict_file = dict_file
        super().__init__(self.__define_all_relationships())

    def __define_all_relationships(self) -> List[Relationship]:
        complete_relationship_list = self.__define_case_studies_to_techniques_relationships()
        complete_relationship_list.extend(self.__define_mitigations_to_techniques_relationships())
        return complete_relationship_list

    def __define_case_studies_to_techniques_relationships(self) -> List[Relationship]:
        case_study_to_techniques_relationships_list = []
        for cs in self.dict_file["case-studies"]:
            date_data = str(cs['incident-date']).split("-")
            for tec in cs['procedure']:
                case_study_to_techniques_relationships_list.append(Relationship(
                    type='relationship',
                    relationship_type='uses',
                    id=f'relationship--{get_uuid_from_string(cs["id"]+"-"+tec["technique"])}',
                    source_ref=f"campaign--{get_uuid_from_string(cs['id'])}",
                    target_ref=f"attack-pattern--{get_uuid_from_string(tec['technique'])}",
                    description=tec['description'],
                    created=datetime.date(int(date_data[0]), int(date_data[1]), int(date_data[2]))
                ))
        return case_study_to_techniques_relationships_list

    def __define_mitigations_to_techniques_relationships(self) -> List[Relationship]:
        mitigation_to_techniques_relationships_list = []
        for mit in (self.dict_file['matrices'][0])['mitigations']:
            for tec in mit['techniques']:
                mitigation_to_techniques_relationships_list.append(Relationship(
                    type='relationship',
                    relationship_type='uses',
                    id=f'relationship--{get_uuid_from_string(mit["id"]+"-"+tec["id"])}',
                    source_ref=f"course-of-action--{get_uuid_from_string(mit['id'])}",
                    target_ref=f"attack-pattern--{get_uuid_from_string(tec['id'])}",
                    description=mit['description']
                ))
        return mitigation_to_techniques_relationships_list
