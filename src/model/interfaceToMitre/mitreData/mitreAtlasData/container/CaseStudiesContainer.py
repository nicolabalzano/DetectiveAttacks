import datetime
from typing import List
from stix2.v20 import Campaign
from src.model.Singleton import singleton
from src.model.interfaceToMitre.mitreData.mitreAtlasData.container.AbstractAtlasContainer import AbstractAtlasContainer
from src.model.interfaceToMitre.mitreData.mitreAtlasData.utils.MitreAtlasUtils import get_uuid_from_string


@singleton
class CaseStudiesContainer(AbstractAtlasContainer):

    def __init__(self, dict_file: dict):
        self.dict_file = dict_file
        super().__init__(self.__get_all_case_studies())

    def __get_all_case_studies(self) -> List[Campaign]:
        list_case_studies = []
        for cs in self.dict_file['case-studies']:
            date_data = str(cs['incident-date']).split("-")
            case_study = Campaign(
                type='campaign',
                id="campaign--" + f"{get_uuid_from_string(cs['id'])}",
                name=cs['name'],
                description=cs['summary'],
                created=datetime.date(int(date_data[0]), int(date_data[1]), int(date_data[2])),
                external_references=super()._get_external_refs(cs, 'studies')
            )
            list_case_studies.append(case_study)

        return list_case_studies
