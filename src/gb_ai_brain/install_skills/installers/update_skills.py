from gb_ai_brain.shared_kernel.shell import run_command


def update_skills() -> bool:
    print("Checking for skill updates...")
    return run_command(["npx", "skills", "update"])
