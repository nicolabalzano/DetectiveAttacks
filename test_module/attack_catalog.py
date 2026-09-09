import json
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENTERPRISE_ATTACK = (
    REPO_ROOT / "stix&vulnerability" / "src" / "dataProvider" / "interfaceToCTI" / "files" / "enterprise-attack.json"
)


ATTACK_ID_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")


@dataclass(frozen=True)
class AttackPattern:
    attack_id: str
    name: str
    description: str
    tactics: tuple
    domains: tuple
    is_subtechnique: bool
    parent_id: str
    parent_name: str

    def as_candidate_text(self, description_chars=None):
        description = compact_text(self.description)
        if description_chars is not None:
            if description_chars <= 0:
                description = ""
            elif len(description) > description_chars:
                description = description[:description_chars].rsplit(" ", 1)[0] + "..."
        tactics = ", ".join(self.tactics)
        parent = f", parent:{self.parent_id} {self.parent_name}" if self.parent_id else ""
        if description:
            return f"ID:{self.attack_id}, name:{self.name}{parent}, tactics:{tactics}, description:{description};"
        return f"ID:{self.attack_id}, name:{self.name}{parent}, tactics:{tactics};"

    def as_dict(self):
        return {
            "attack_id": self.attack_id,
            "name": self.name,
            "description": self.description,
            "tactics": list(self.tactics),
            "domains": list(self.domains),
            "is_subtechnique": self.is_subtechnique,
            "parent_id": self.parent_id,
            "parent_name": self.parent_name,
        }


def compact_text(text):
    text = re.sub(r"<.*?>", " ", text or "", flags=re.DOTALL)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _external_attack_id(stix_object):
    for reference in stix_object.get("external_references", []):
        external_id = reference.get("external_id", "")
        if reference.get("source_name") == "mitre-attack" and ATTACK_ID_RE.match(external_id):
            return external_id
    return None


def load_enterprise_attack_patterns(path=DEFAULT_ENTERPRISE_ATTACK, include_subtechniques=True):
    with Path(path).open(encoding="utf-8") as handle:
        bundle = json.load(handle)

    raw_patterns = []
    id_to_name = {}
    for obj in bundle.get("objects", []):
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        attack_id = _external_attack_id(obj)
        if not attack_id:
            continue
        raw_patterns.append((attack_id, obj))
        id_to_name[attack_id] = obj.get("name", "")

    patterns = []
    for attack_id, obj in raw_patterns:
        is_subtechnique = bool(obj.get("x_mitre_is_subtechnique")) or "." in attack_id
        if is_subtechnique and not include_subtechniques:
            continue
        parent_id = attack_id.split(".", 1)[0] if is_subtechnique else ""
        tactics = tuple(
            phase.get("phase_name", "")
            for phase in obj.get("kill_chain_phases", [])
            if phase.get("kill_chain_name") == "mitre-attack" and phase.get("phase_name")
        )
        patterns.append(
            AttackPattern(
                attack_id=attack_id,
                name=obj.get("name", ""),
                description=obj.get("description", ""),
                tactics=tactics,
                domains=tuple(obj.get("x_mitre_domains", [])),
                is_subtechnique=is_subtechnique,
                parent_id=parent_id,
                parent_name=id_to_name.get(parent_id, "") if parent_id else "",
            )
        )

    return sorted(patterns, key=lambda pattern: pattern.attack_id)


def attack_pattern_index(patterns):
    return {pattern.attack_id: pattern for pattern in patterns}


def valid_attack_ids(patterns):
    return set(attack_pattern_index(patterns))
