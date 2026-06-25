from gb_ai_brain.install_skills.shell import run_command


def update_skills() -> bool:
    print("Checking for skill updates...")
    return run_command(["npx", "skills", "update"])
