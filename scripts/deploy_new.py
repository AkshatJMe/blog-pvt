import subprocess
from datetime import datetime
from pathlib import Path
import shutil
import os
import stat

def deploy_public_to_gh_pages():
    # ========= Configuration =========
    GITHUB_REPO = "git@github.com:AkshatJMe/AkshatJMe.github.io.git"  
    BRANCH = "gh-pages"
    MAIN_BRANCH = "main"
    NAME = "Akshat Jain"
    EMAIL = "realakshatjain@gmail.com"
    
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    PUBLIC_DIR = PROJECT_ROOT / "public"
    DEPLOY_DIR = PROJECT_ROOT / ".gh-pages-temp"
    # =================================

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    deploy_message = f"Deploy site from public/ at {timestamp}"

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

    # 🔧 Handle read-only files (no admin needed)
    def handle_remove_readonly(func, path, exc_info):
        print(f"⚠️ Forcing deletion of read-only file: {path}")
        os.chmod(path, stat.S_IWRITE)  # Remove read-only flag
        func(path)

    # ==== Step 1: Validate ====
    if not PUBLIC_DIR.exists():
        raise FileNotFoundError(f"Public directory not found: {PUBLIC_DIR}")

    # ==== Step 2: Clean deploy dir ====
    if DEPLOY_DIR.exists():
        shutil.rmtree(DEPLOY_DIR, onerror=handle_remove_readonly)
    DEPLOY_DIR.mkdir()

    # ==== Step 3: Copy public/ to .gh-pages-temp ====
    print("📁 Copying public/ to temporary gh-pages directory...")
    for item in PUBLIC_DIR.iterdir():
        dest = DEPLOY_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # ==== Step 4: Initialize git in deploy folder ====
    print("🔧 Initializing Git in deploy directory...")
    run("git init", cwd=DEPLOY_DIR)
    run(f"git remote add origin {GITHUB_REPO}", cwd=DEPLOY_DIR)
    run(f"git checkout -b {BRANCH}", cwd=DEPLOY_DIR)
    git_config(cwd=DEPLOY_DIR)

    # ==== Step 5: Commit and push ====
    run("git add .", cwd=DEPLOY_DIR)
    if has_changes_to_commit(cwd=DEPLOY_DIR):
        run(f'git commit -m "{deploy_message}"', cwd=DEPLOY_DIR)
        run(f"git push -f origin {BRANCH}", cwd=DEPLOY_DIR)
    else:
        print("ℹ️ No changes to deploy.")

    # ==== Step 6: Switch back to main branch in source repo ====
    print(f"\n🔁 Switching back to '{MAIN_BRANCH}' in your main repo...")
    run(f"git checkout {MAIN_BRANCH}", cwd=PROJECT_ROOT)

    # ==== Done ====
    print("\n✅ Deployed to GitHub Pages branch!")
    print(f"🌐 Branch: {BRANCH}")
    print(f"📌 Commit message: {deploy_message}")
    print(f"🔙 Returned to '{MAIN_BRANCH}' in your repo.")

# Run the function
deploy_public_to_gh_pages()
