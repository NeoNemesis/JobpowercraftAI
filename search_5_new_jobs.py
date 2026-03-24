#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 SÖK 5 NYA JOBB AUTOMATISKT
==============================
✅ Söker på Indeed (Uppsala + Södra Stockholm)
✅ Genererar CV och personliga brev automatiskt
✅ Använder nya språkfixen (svenska för svenska företag)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

# Import från job_master
from job_master import JobMaster

def main():
    print("\n" + "="*80)
    print("🔍 SÖKER 5 NYA JOBB AUTOMATISKT")
    print("="*80)
    print("📍 Uppsala + Södra Stockholm (50km)")
    print("💼 Indeed")
    print("🎯 Max 5 nya jobb")
    print("="*80)

    try:
        # Skapa JobMaster instans
        job_master = JobMaster()

        # Starta systemet
        job_master.initialize()

        print("\n🔍 Söker jobb på Indeed...")

        # Sök endast på Indeed (snabbast)
        jobs = job_master.search_indeed_jobs(max_jobs=5)

        if not jobs:
            print("❌ Inga nya jobb hittades")
            return

        print(f"\n✅ Hittade {len(jobs)} nya jobb!")
        print("\n📝 Genererar CV och personliga brev...")

        # Processa jobben automatiskt
        successful = job_master.process_jobs_automatic(jobs)

        print("\n" + "="*80)
        print("✅ KLART!")
        print("="*80)
        print(f"📊 Resultat: {successful}/{len(jobs)} jobb processade")
        print(f"📂 Dokument: {job_master.base_output_dir.absolute()}")

    except Exception as e:
        print(f"\n❌ Fel: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\n🧹 Stänger browser...")
        if hasattr(job_master, 'driver'):
            from src.utils.browser_pool import cleanup_browser
            cleanup_browser()
        print("✅ Klart!")

if __name__ == "__main__":
    main()
