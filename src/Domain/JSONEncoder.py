import dataclasses
import json
from dataclasses import asdict

from stix2.utils import STIXdatetime
from stix2.v20 import ExternalReference


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, STIXdatetime):
            return obj.isoformat()
        elif isinstance(obj, ExternalReference):
            return obj.__dict__

        return super().default(obj)