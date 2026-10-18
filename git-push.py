import subprocess
import sys
import datetime

def run_command(command):
    """Executes a shell command and prints the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.stdout.strip():
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute: {command}\nError: {e.stderr.strip()}")
        sys.exit(1)

def main():
    # If a message is passed as an argument, use it. Otherwise, use a timestamp.
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-update from WSL: {now}"

    print("🚀 Staging files...")
    run_command("git add .")

    print(f"📝 Committing changes: '{commit_message}'")
    # Using a separate try-except here because 'git commit' throws an error if there's nothing to commit
    try:
        subprocess.run(f'git commit -m "{commit_message}"', shell=True, check=True, text=True, capture_output=True)
        print("Commit successful.")
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.stdout.lower() or "nothing to commit" in getattr(e, 'stderr', '').lower():
            print("No changes detected. Working tree is clean.")
            sys.exit(0)
        else:
            print(f"Error during commit: {getattr(e, 'stderr', e)}")
            sys.exit(1)

    print("☁️ Pushing to https://github.com/martinmat13/ML4MaterialScience.git...")
    # Explicitly defining the URL ensures it goes to the right place even if origin isn't perfectly configured
    run_command("git push https://github.com/martinmat13/ML4MaterialScience.git main")
    
    print("✅ Push complete!")

if __name__ == "__main__":
    main()