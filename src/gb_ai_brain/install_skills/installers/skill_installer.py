from typing import Protocol

from gb_ai_brain.install_skills.models.skill_def import SkillDef


class SkillInstaller(Protocol):
    def install(self, skill: SkillDef) -> bool: ...
