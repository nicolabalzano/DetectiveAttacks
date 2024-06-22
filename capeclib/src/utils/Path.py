import os

current_directory = os.path.dirname(os.path.abspath(__file__))
directories_up = os.path.dirname(current_directory)

default_path = directories_up+"/_data/"
CAPEC = "stix-capec"
default_repo = "https://github.com/mitre/cti.git",
