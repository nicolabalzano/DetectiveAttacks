from pprint import pprint

from src.controller.app import DICT_OF_FILTER_TYPES, get_attack_patterns_grouped_by_CKCP
from src.controller.objectsController.stixController.AttackPatternController import \
    get_all_attack_patterns_grouped_by_CKCP
from src.model.container import AttackPatternsContainer, MitreToCVEContainer, IntrusionSetsContainer
from src.model.container.vulnerabilityContainer.AbstractMitreToVulnerabilityContainer import \
    AbstractMitreToVulnerabilityContainer
from src.model.gptAPI.gptAPI import GPT_API
from src.model.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ENTERPRISE_DATA

vuln_desc = """

TensorFlow is an Open Source Machine Learning Framework. In versions prior to 2.11.1 a malicious invalid input crashes a tensorflow model (Check Failed) and can be used to trigger a denial of service attack. A proof of concept can be constructed with the `Convolution3DTranspose` function. This Convolution3DTranspose layer is a very common API in modern neural networks. The ML models containing such vulnerable components could be deployed in ML applications or as cloud services. This failure could be potentially used to trigger a denial of service attack on ML cloud services. An attacker must have privilege to provide input to a `Convolution3DTranspose` call. This issue has been patched and users are advised to upgrade to version 2.11.1. There are no known workarounds for this vulnerability.

"""
# MitreToCVEContainer().get_attack_pattern_by_vuln_id('CVE-2023-25661')

print([at.x_mitre_platforms for at in AttackPatternsContainer().get_tuple_data() if 'atlas' in at.x_mitre_domains])
