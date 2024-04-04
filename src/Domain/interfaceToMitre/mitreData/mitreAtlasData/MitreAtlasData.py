import json
import os
from typing import List
from mitreattack.stix20 import StixObjectFactory
from stix2.v20 import AttackPattern, CourseOfAction, Campaign, Software
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.TechniquesContainer import TechniquesContainer
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.RelationshipsContainer import RelationshipsContainer
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.MitigationsContainer import MitigationsContainer
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.CaseStudiesContainer import CaseStudiesContainer


class MitreAtlasData:

    all_techniques_used_by_all_campaigns = None
    all_techniques_used_by_all_mitigations = None
    all_mitigations_mitigating_all_techniques = None

    def __init__(self, filepath: str = None):
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                self.dict_file = json.load(file)

        # Initialize Containers
        TechniquesContainer(self.dict_file)
        RelationshipsContainer(self.dict_file)
        MitigationsContainer(self.dict_file)
        CaseStudiesContainer(self.dict_file)

    ###################################
    # STIX Objects Section
    ###################################

    def get_techniques(self) -> List[AttackPattern]:
        """Retrieve all technique objects.
        Returns
        -------
        list
            a list of AttackPattern objects
        """
        return TechniquesContainer().get_data()

    def get_mitigations(self) -> List[CourseOfAction]:
        """Retrieve all mitigation objects.
        Returns
        -------
        list
            a list of CourseOfAction objects
        """
        return MitigationsContainer().get_data()

    def get_case_studies(self) -> List[Campaign]:
        """Retrieve all campaign objects.
        Returns
        -------
        list
            a list of Campaign objects
        """
        return CaseStudiesContainer().get_data()

    def get_sofwtware(self) -> List[Software]:
        return []

    ###################################
    # Get STIX Object by Value
    ###################################

    def get_technique_by_id(self, technique_id: str) -> AttackPattern:
        for technique in self.get_techniques():
            if technique_id == technique['id']:
                return technique

    ###################################
    # Relationships Setion
    ###################################

    def get_related(self, source_type: str, target_type: str, reverse: bool = False) -> dict:
        """Build relationship mappings.

        Parameters
        ----------
        source_type : str
            source type for the relationships, e.g. 'intrusion-set'
        target_type : str
            target type for the relationships, e.g. 'attack-pattern'
        reverse : bool
            build reverse mapping of target to source, by default False

        Returns
        -------
        dict
            relationship mapping of source_object_id => [{target_object, relationship[]}];
        """
        # stix_id => [ { relationship, related_object_id } for each related object ]
        id_to_related = {}

        # build the dict
        for relationship in RelationshipsContainer().get_data():
            if source_type in relationship.source_ref and target_type in relationship.target_ref:
                if (relationship.source_ref in id_to_related and not reverse) or (relationship.target_ref in id_to_related and reverse):
                    # append to existing entry
                    if not reverse:
                        id_to_related[relationship.source_ref].append(
                            {"relationship": relationship, "id": relationship.target_ref}
                        )
                    else:
                        id_to_related[relationship.target_ref].append(
                            {"relationship": relationship, "id": relationship.source_ref}
                        )
                else:
                    # create a new entry
                    if not reverse:
                        id_to_related[relationship.source_ref] = [
                            {"relationship": relationship, "id": relationship.target_ref}
                        ]
                    else:
                        id_to_related[relationship.target_ref] = [
                            {"relationship": relationship, "id": relationship.source_ref}
                        ]

        # all objects of relevant type
        if not reverse:
            targets = TechniquesContainer().get_data()
        else:
            targets = MitigationsContainer().get_data()

        # build lookup of stixID to stix object
        id_to_target = {}
        for target in targets:
            id_to_target[target["id"]] = target

        # build final output mappings
        output = {}
        for stix_id in id_to_related: # for every attack pattern
            value = []
            for related in id_to_related[stix_id]:
                value.append(
                    {
                        "object": StixObjectFactory(id_to_target[related['id']]),
                        "relationships": [related["relationship"]],
                    }
                )
            output[stix_id] = value
        return output

    ###################################
    # Technique/Campaign Relationships
    ###################################

    def get_all_techniques_used_by_all_case_studies(self) -> dict:
        """Get all techniques used by all case studies.

        Returns
        -------
        dict
            a mapping of campaign_stix_id => [{"object": AttackPattern, "relationships": Relationship[]}] for each technique used by the case studies
        """
        # return data if it has already been fetched
        if self.all_techniques_used_by_all_campaigns:
            return self.all_techniques_used_by_all_campaigns

        self.all_techniques_used_by_all_campaigns = self.get_related("campaign", "attack-pattern")
        return self.all_techniques_used_by_all_campaigns

    def get_techniques_used_by_case_study(self, case_study_stix_id: str) -> list:
        """Get all techniques used by a case study.

        Parameters
        ----------
        case_study_stix_id : str
            the STIX ID of the case study

        Returns
        -------
        list
            a list of {"object": AttackPattern, "relationships": Relationship[]} for each technique used by the case study
        """
        techniques_used_by_case_studies = self.get_all_techniques_used_by_all_case_studies()
        return (
            techniques_used_by_case_studies[case_study_stix_id] if case_study_stix_id in techniques_used_by_case_studies else []
        )

    ###################################
    # Mitigation/Technique Relationships
    ###################################

    def get_all_techniques_used_by_all_mitigations(self) -> dict:
        """Get all techniques used by all mitigations.

            Returns
            -------
            dict
                a mapping of mitigation_stix_id => [{"object": AttackPattern, "relationships": Relationship[]}] for each technique used by the mitigations
        """
        # return data if it has already been fetched
        if self.all_techniques_used_by_all_mitigations:
            return self.all_techniques_used_by_all_mitigations

        self.all_techniques_used_by_all_mitigations = self.get_related("course-of-action", "attack-pattern")
        return self.all_techniques_used_by_all_mitigations

    def get_techniques_used_by_mitigation(self, mitigation_stix_id: str) -> list:
        """Get all techniques used by a mitigation.

        Parameters
        ----------
        mitigation_stix_id : str
            the STIX ID of the mitigation (course-of-action)

        Returns
        -------
        list
            a list of {"object": AttackPattern, "relationships": Relationship[]} for each technique used by the mitigation
        """
        techniques_used_by_mitigations = self.get_all_techniques_used_by_all_mitigations()
        return (
            techniques_used_by_mitigations[mitigation_stix_id] if mitigation_stix_id in techniques_used_by_mitigations else []
        )

    def get_all_mitigations_mitigating_all_techniques(self) -> dict:
        """Get all mitigations mitigating all techniques.

        Returns
        -------
        dict
            a mapping of technique_stix_id => [{"object": CourseOfAction, "relationships": Relationship[]}] for each mitigation mitigating the technique
        """
        # return data if it has already been fetched
        if self.all_mitigations_mitigating_all_techniques:
            return self.all_mitigations_mitigating_all_techniques

        self.all_mitigations_mitigating_all_techniques = self.get_related("course-of-action", "attack-pattern", reverse=True)
        return self.all_mitigations_mitigating_all_techniques

    def get_mitigations_mitigating_technique(self, technique_stix_id: str) -> list:
        """Get all mitigations mitigating a technique.

        Parameters
        ----------
        technique_stix_id : str
            the STIX ID of the technique

        Returns
        -------
        list
            a list of {"object": CourseOfAction, "relationships": Relationship[]} for each mitigation mitigating the technique
        """
        mitigations_mitigating_techniques = self.get_all_mitigations_mitigating_all_techniques()
        return (
            mitigations_mitigating_techniques[technique_stix_id] if technique_stix_id in mitigations_mitigating_techniques else []
        )

    ###################################
    # Software/Technique Relationships
    ###################################

    def get_all_techniques_used_by_software(self) -> dict:
        return {}

    def get_techniques_used_by_software(self, software_stix_id: str) -> list:
        return []
