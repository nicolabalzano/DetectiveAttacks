import json
from pprint import pprint

from src.controller.app import DICT_OF_FILTER_TYPES, get_attack_patterns_grouped_by_CKCP, get_report_groups
from src.controller.objectsController.stixController.AttackPatternController import \
    get_all_attack_patterns_grouped_by_CKCP
from src.controller.objectsController.stixController.IntrusionSetController import \
    __get_intrusion_set_probability_from_attack_patterns, fetch_report_of_intrusion_set_probability_from_attack_patterns
from src.controller.objectsController.util import download_file
from src.model.container import AttackPatternsContainer, MitreToCVEContainer, IntrusionSetsContainer
from src.model.container.vulnerabilityContainer.AbstractMitreToVulnerabilityContainer import \
    AbstractMitreToVulnerabilityContainer
from src.model.gptAPI.gptAPI import GPT_API
from src.model.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ENTERPRISE_DATA
from src.model.pdfGeneration.pdf import generate_pdf_from_html

vuln_desc = """

TensorFlow is an Open Source Machine Learning Framework. In versions prior to 2.11.1 a malicious invalid input crashes a tensorflow model (Check Failed) and can be used to trigger a denial of service attack. A proof of concept can be constructed with the `Convolution3DTranspose` function. This Convolution3DTranspose layer is a very common API in modern neural networks. The ML models containing such vulnerable components could be deployed in ML applications or as cloud services. This failure could be potentially used to trigger a denial of service attack on ML cloud services. An attacker must have privilege to provide input to a `Convolution3DTranspose` call. This issue has been patched and users are advised to upgrade to version 2.11.1. There are no known workarounds for this vulnerability.

"""
# MitreToCVEContainer().get_attack_pattern_by_vuln_id('CVE-2023-25661')
"""
print([obj[0].name + ' ' + str(obj[1]) for obj in
       get_intrusion_set_probability_from_attack_patterns(
           'Command%26Control__T1205.002,Action_on_Objectives__T1561.002,Action_on_Objectives__T1498.001,Command%26Control__T1113')])
"""

# Dizionario di esempio
data = __get_intrusion_set_probability_from_attack_patterns(
    'Command%26Control__T1205.002,Action_on_Objectives__T1561.002,Action_on_Objectives__T1498.001,Command%26Control__T1113')
print(type(data[0]))


def get_report_groups2():
    id_list = 'Command%26Control__T1205.002,Action_on_Objectives__T1561.002,Action_on_Objectives__T1498.001,Command%26Control__T1113'
    return download_file(fetch_report_of_intrusion_set_probability_from_attack_patterns(id_list))


get_report_groups2()

"""
print(set([g.name for g in IntrusionSetsContainer().get_tuple_data() if
           len(g.attack_patterns_and_relationship.keys()) > 0]))
"""
