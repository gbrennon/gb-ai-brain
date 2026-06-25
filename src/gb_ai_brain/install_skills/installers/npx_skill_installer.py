from gb_ai_brain.install_skills.models.skill_def import SkillDef
from gb_ai_brain.install_skills.installers.skill_installer import SkillInstaller
from gb_ai_brain.install_skills.shell import run_command


class NpxSkillInstaller:
    def __init__(self, npx_command: str | None = None) -> None:
        self._npx_command = npx_command or "npx"

    def install(self, skill: SkillDef) -> bool:
        print(f"Installing {skill.name} from {skill.source}")
        return run_command(
            [self._npx_command, "skills", "add", skill.source, "--skill", skill.name, "-g", "-y"]
        )
