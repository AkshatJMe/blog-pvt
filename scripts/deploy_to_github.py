import subprocess
from datetime import datetime
from pathlib import Path

def deploy_to_github():
    # ========= Configuration =========
    SOURCE_REPO = "git@github.com:AkshatJMe/AkshatJMe.github.io.git"
    PUBLIC_REPO = "git@github.com::AkshatJMe/Blogs.git"
    BRANCH = "main"
    NAME = "Akshat Jain"
    EMAIL = "realakshatjain@gmail.com"
    
    # Resolve paths relative to THIS script's directory
    SCRIPT_DIR = Path(__file__).resolve().parent
    SITE_ROOT = SCRIPT_DIR.parent  # Assuming project root is one level up from script file
    PUBLIC_DIR = SITE_ROOT / "public"
    # =================================

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    source_commit_msg = f"Update source: {timestamp}"
    public_commit_msg = f"Build: {timestamp}"

    def run(cmd, cwd=None):
        print(f"👉 Running: {cmd} (cwd={cwd})")
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)

    def git_config(cwd=None):
        run(f'git config user.name "{NAME}"', cwd=cwd)
        run(f'git config user.email "{EMAIL}"', cwd=cwd)

    def has_changes_to_commit(cwd=None):
        result = subprocess.run(
            "git status --porcelain", shell=True,
            capture_output=True, text=True, cwd=cwd
        )
        return bool(result.stdout.strip())

    # Build Hugo site
    print("🔨 Building Hugo site...")
    run("hugo", cwd=SITE_ROOT)

    # Push source code to source repo
    print(f"📦 Pushing source code to {SOURCE_REPO}...")
    git_config(cwd=SITE_ROOT)
    run("git add .", cwd=SITE_ROOT)

    if has_changes_to_commit(cwd=SITE_ROOT):
        run(f'git commit -m "{source_commit_msg}"', cwd=SITE_ROOT)
        run(f"git push origin {BRANCH}", cwd=SITE_ROOT)
    else:
        print("ℹ️ No changes to commit in source repository.")

    # Deploy public site
    print(f"🚀 Deploying to {PUBLIC_REPO}...")

    if not PUBLIC_DIR.exists():
        raise FileNotFoundError(f"Public directory does not exist: {PUBLIC_DIR}")

    if not (PUBLIC_DIR / ".git").exists():
        print("🔧 Initializing git in public/ directory...")
        run("git init", cwd=PUBLIC_DIR)
        run(f"git remote add origin {PUBLIC_REPO}", cwd=PUBLIC_DIR)

    git_config(cwd=PUBLIC_DIR)
    run(f"git checkout -B {BRANCH}", cwd=PUBLIC_DIR)
    run("git add .", cwd=PUBLIC_DIR)

    if has_changes_to_commit(cwd=PUBLIC_DIR):
        run(f'git commit -m "{public_commit_msg}"', cwd=PUBLIC_DIR)
        run(f"git push -f origin {BRANCH}", cwd=PUBLIC_DIR)
    else:
        print("ℹ️ No changes to commit in public directory.")

    print("\n✅ Done. Source and public folders pushed.")
    print(f"📌 Source commit message: {source_commit_msg}")
    print(f"📌 Public commit message: {public_commit_msg}")

# deploy_to_github()