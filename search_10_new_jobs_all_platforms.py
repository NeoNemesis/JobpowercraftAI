#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 SÖK 10 NYA JOBB (ALLA PLATTFORMAR + SIDA 2)
==============================================
✅ Indeed (sida 1 OCH sida 2)
✅ LinkedIn
✅ Arbetsförmedlingen
✅ Totalt 10 nya jobb (skippar redan processade)
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
    print("🔍 SÖKER 10 NYA JOBB (ALLA PLATTFORMAR + SIDA 2)")
    print("="*80)
    print("📍 Uppsala + Södra Stockholm + Enköping")
    print("💼 Indeed (sida 1+2) + LinkedIn + Arbetsförmedlingen")
    print("🎯 Max 10 nya unika jobb")
    print("="*80)

    try:
        # Skapa JobMaster instans
        job_master = JobMaster()

        # Starta systemet
        job_master.initialize()

        print(f"\n✅ Har redan {len(job_master.processed_urls)} processade jobb-URL:er")
        print("🔎 Söker på alla plattformar inkl. sida 2 på Indeed...")

        all_jobs = []

        # 1. SÖK PÅ INDEED (inkl. sida 2)
        print("\n" + "="*80)
        print("🔍 SÖKER PÅ INDEED (sida 1 + sida 2)")
        print("="*80)
        indeed_jobs = job_master.search_indeed_jobs_multipage(max_jobs=10)
        all_jobs.extend(indeed_jobs)
        print(f"✅ Indeed: {len(indeed_jobs)} nya jobb hittade")

        # 2. SÖK PÅ LINKEDIN (om vi inte har 10 jobb än)
        if len(all_jobs) < 10:
            print("\n" + "="*80)
            print("🔍 SÖKER PÅ LINKEDIN")
            print("="*80)
            remaining = 10 - len(all_jobs)
            linkedin_jobs = job_master.search_linkedin_jobs(max_jobs=remaining)
            all_jobs.extend(linkedin_jobs)
            print(f"✅ LinkedIn: {len(linkedin_jobs)} nya jobb hittade")

        # 3. SÖK PÅ ARBETSFÖRMEDLINGEN (om vi inte har 10 jobb än)
        if len(all_jobs) < 10:
            print("\n" + "="*80)
            print("🔍 SÖKER PÅ ARBETSFÖRMEDLINGEN")
            print("="*80)
            remaining = 10 - len(all_jobs)
            af_jobs = job_master.search_arbetsformedlingen_jobs(max_jobs=remaining)
            all_jobs.extend(af_jobs)
            print(f"✅ Arbetsförmedlingen: {len(af_jobs)} nya jobb hittade")

        # Ta endast de första 10
        all_jobs = all_jobs[:10]

        if not all_jobs:
            print("\n❌ Inga nya jobb hittades")
            return

        print("\n" + "="*80)
        print(f"✅ TOTALT: {len(all_jobs)} nya unika jobb hittade!")
        print("="*80)
        for i, job in enumerate(all_jobs, 1):
            print(f"{i}. {job['title']} @ {job['company']} ({job['source']})")

        print("\n📝 Genererar CV och personliga brev...")

        # KRITISK FIX: Återställ browser OCH uppdatera referenser
        # Efter lång sökning kan browser-sessionen bli invalid
        print("🔄 Återställer browser för stabil PDF-generering...")
        from src.utils.browser_pool import reset_browser, get_browser
        reset_browser()

        # Uppdatera driver-referenser i job_master och modern_facade
        job_master.driver = get_browser()
        if job_master.modern_facade:
            job_master.modern_facade.driver = job_master.driver
        print("✅ Browser återställd och referenser uppdaterade")

        # Processa jobben automatiskt
        successful = job_master.process_jobs_automatic(all_jobs)

        print("\n" + "="*80)
        print("✅ KLART!")
        print("="*80)
        print(f"📊 Resultat: {successful}/{len(all_jobs)} jobb processade")
        print(f"📂 Dokument: {job_master.base_output_dir.absolute()}")

    except Exception as e:
        print(f"\n❌ Fel: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\n🧹 Stänger browser...")
        if hasattr(job_master, 'driver') and job_master.driver:
            from src.utils.browser_pool import cleanup_browser
            cleanup_browser()
        print("✅ Klart!")

if __name__ == "__main__":
    main()
