#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JobpowercraftAI - Universal Job Application Automation
=======================================================
Single entry point. Run this file to get started.

Usage:
    python run.py
    python run.py --setup      Force re-run the setup wizard
    python run.py --help       Show help
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.absolute()
DATA_DIR = ROOT / 'data_folder'
RESUME_FILE = DATA_DIR / 'plain_text_resume.yaml'
RESUME_EXAMPLE = DATA_DIR / 'plain_text_resume.example.yaml'
PREFS_FILE = DATA_DIR / 'work_preferences.yaml'
PREFS_EXAMPLE = DATA_DIR / 'work_preferences.example.yaml'
ENV_FILE = ROOT / '.env'
ENV_EXAMPLE = ROOT / '.env.example'


# ── Colours (work on any terminal that supports ANSI) ─────────────────────────
class C:
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'

def ok(msg):   print(f"{C.GREEN}✅ {msg}{C.RESET}")
def warn(msg): print(f"{C.YELLOW}⚠️  {msg}{C.RESET}")
def err(msg):  print(f"{C.RED}❌ {msg}{C.RESET}")
def info(msg): print(f"{C.CYAN}ℹ️  {msg}{C.RESET}")
def header(msg):
    print(f"\n{C.BOLD}{C.CYAN}{'='*60}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {msg}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'='*60}{C.RESET}\n")


# ── Setup wizard ──────────────────────────────────────────────────────────────

def setup_env():
    """Interactive setup for .env (API key)."""
    header("Step 1 / 3 — API Key Setup")

    if ENV_FILE.exists():
        from dotenv import dotenv_values
        existing = dotenv_values(ENV_FILE)
        if existing.get('OPENAI_API_KEY', '').startswith('sk-'):
            ok(".env already configured with a valid OpenAI API key.")
            return

    print("  You need an OpenAI API key to generate tailored CVs and cover letters.")
    print("  Get one at: https://platform.openai.com/api-keys\n")

    api_key = input("  Paste your OpenAI API key (starts with sk-): ").strip()
    if not api_key.startswith('sk-'):
        warn("That doesn't look like a valid key (should start with 'sk-').")
        warn("You can edit .env manually later.")

    content = f'OPENAI_API_KEY={api_key}\n'
    if ENV_EXAMPLE.exists():
        from dotenv import dotenv_values
        example_vals = dotenv_values(ENV_EXAMPLE)
        lines = ENV_EXAMPLE.read_text(encoding='utf-8').splitlines()
        new_lines = []
        for line in lines:
            if line.startswith('OPENAI_API_KEY='):
                new_lines.append(f'OPENAI_API_KEY={api_key}')
            elif line.startswith('JOBCRAFT_API_KEY='):
                new_lines.append(f'OPENAI_API_KEY={api_key}')
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines) + '\n'

    ENV_FILE.write_text(content, encoding='utf-8')
    ok(".env file created.")


def setup_resume():
    """Guide user to fill in their resume YAML."""
    header("Step 2 / 3 — Your Resume")

    if RESUME_FILE.exists():
        # Check it's not still the example (name field still placeholder)
        text = RESUME_FILE.read_text(encoding='utf-8')
        if 'Your First Name' not in text:
            ok("plain_text_resume.yaml already exists.")
            return

    if not RESUME_EXAMPLE.exists():
        err("plain_text_resume.example.yaml not found.")
        return

    shutil.copy(RESUME_EXAMPLE, RESUME_FILE)
    print(f"  A template has been copied to:\n  {RESUME_FILE}\n")
    print("  Please open that file and replace all placeholder values with")
    print("  your real name, contact info, experience, education, etc.\n")

    input("  Press ENTER once you have filled in the file... ")

    # Quick sanity check
    text = RESUME_FILE.read_text(encoding='utf-8')
    if 'Your First Name' in text:
        warn("The file still contains placeholder text. Please edit it before running.")
    else:
        ok("Resume file looks good.")


def setup_preferences():
    """Guide user to configure job search preferences."""
    header("Step 3 / 3 — Job Search Preferences")

    if PREFS_FILE.exists():
        ok("work_preferences.yaml already exists.")
        return

    if not PREFS_EXAMPLE.exists():
        err("work_preferences.example.yaml not found.")
        return

    shutil.copy(PREFS_EXAMPLE, PREFS_FILE)
    print(f"  A template has been copied to:\n  {PREFS_FILE}\n")
    print("  Open that file and adjust:")
    print("  • Positions (job titles to search for)")
    print("  • Locations (cities / countries)")
    print("  • Experience level, job type, remote/onsite\n")

    ans = input("  Would you like to edit it now? [Y/n]: ").strip().lower()
    if ans in ('', 'y', 'yes'):
        editor = os.environ.get('EDITOR', 'notepad' if sys.platform == 'win32' else 'nano')
        os.system(f'{editor} "{PREFS_FILE}"')

    ok("work_preferences.yaml ready.")


def run_setup(force=False):
    """Run the full first-time setup wizard."""
    header("JobpowercraftAI — First-Time Setup")
    print("  This wizard will guide you through the one-time configuration.\n")
    setup_env()
    setup_resume()
    setup_preferences()
    header("Setup Complete!")
    print("  You can now run  python run.py  to start searching for jobs.\n")


def is_setup_complete():
    """Return True if all required files exist and look populated."""
    if not ENV_FILE.exists():
        return False
    if not RESUME_FILE.exists():
        return False
    if not PREFS_FILE.exists():
        return False
    text = RESUME_FILE.read_text(encoding='utf-8')
    if 'Your First Name' in text:
        return False
    return True


# ── Main menu ─────────────────────────────────────────────────────────────────

def show_menu():
    header("JobpowercraftAI — Main Menu")
    print("  1. Search jobs and generate tailored CVs + cover letters")
    print("  2. Regenerate documents for already-found jobs")
    print("  3. Re-run setup wizard")
    print("  0. Exit\n")
    return input("  Choose an option: ").strip()


def launch_job_master():
    """Import and run job_master directly."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)
        import importlib.util
        spec = importlib.util.spec_from_file_location("job_master", ROOT / "job_master.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        master = mod.JobMaster()
        master.run()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        err(f"Error running job master: {e}")
        raise


def launch_regenerate():
    """Run the regenerate_all_jobs script."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)
        import importlib.util
        regen_script = ROOT / "regenerate_all_jobs.py"
        if not regen_script.exists():
            err("regenerate_all_jobs.py not found.")
            return
        spec = importlib.util.spec_from_file_location("regen", regen_script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        err(f"Error running regenerate: {e}")
        raise


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="JobpowercraftAI — AI-powered job application automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py              Start the application (auto-setup on first run)
  python run.py --setup      Re-run the setup wizard
        """
    )
    parser.add_argument('--setup', action='store_true', help='Force re-run the setup wizard')
    args = parser.parse_args()

    if args.setup or not is_setup_complete():
        run_setup(force=args.setup)

    if not is_setup_complete():
        err("Setup incomplete. Please complete the setup before continuing.")
        sys.exit(1)

    # Main interaction loop
    while True:
        choice = show_menu()
        if choice == '1':
            launch_job_master()
        elif choice == '2':
            launch_regenerate()
        elif choice == '3':
            run_setup(force=True)
        elif choice == '0':
            print("\nGoodbye!\n")
            break
        else:
            warn("Invalid option, try again.")


if __name__ == '__main__':
    main()
