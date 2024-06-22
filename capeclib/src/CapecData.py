from src.utils.Singleton import singleton
from src.utils.FileUtils import read_from_json
from src.utils.Path import default_path, CAPEC

@singleton
class CapecData:
    def __init__(self):
        self.capec_data = read_from_json(default_path , CAPEC)['objects']

    def get_capec_data(self):
        return self.capec_data
    
    def get_capec_by_capec_id(self, capec_id):
        for object in self.capec_data:
            if 'external_references' in object:
                for er in object['external_references']:
                    if er['source_name'] == 'capec' and er['external_id'] == capec_id:
                        return object
    
    def get_attack_patterns_mitre_ids_by_CAPEC(self, CAPEC_id):
        
        related_attack_pattern_mitre_ids = []
        
        for er_for_at in self.get_capec_by_capec_id(CAPEC_id)['external_references']:
            if er_for_at['source_name'] == 'ATTACK':
                related_attack_pattern_mitre_ids.append(er_for_at['external_id'])

        return related_attack_pattern_mitre_ids