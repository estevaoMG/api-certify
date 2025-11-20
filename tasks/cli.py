import subprocess
import sys


def cli():
    if len(sys.argv) < 2:
        print("Use: task <lint|format|test|run>")
        return

    cmd = sys.argv[1]

    if cmd == "lint":
        subprocess.run(["flake8", "."])
    elif cmd == "format":
        subprocess.run(["black", "."])
    elif cmd == "test":
        subprocess.run(["pytest", "-v"])
    elif cmd == "run":
        subprocess.run(["uvicorn", "main:app", "--reload"])
    else:
        print(f"Unknown task: {cmd}")
