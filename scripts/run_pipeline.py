# run_pipeline.py (cleaned up to use centralized logger config)

import os
import sys
import argparse
import json
from datetime import datetime, timezone

# Removed sys.path manipulation for clean -m support

from modules.user_profile import load_user_profiles, load_user_profile
from control_plane.orchestrator import run_pipeline_for_user
from utils.logger import log_pipeline_event


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, help="Run pipeline for specific user ID")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate run without making changes"
    )
    args = parser.parse_args()

    if args.user:
        profile = load_user_profile(args.user)
        if not profile:
            print(f"🚫 No profile found for user '{args.user}'")
            sys.exit(1)
        print(f"🔧 Running pipeline for user: {args.user} (dry_run={args.dry_run})")
        if not args.dry_run:
            run_pipeline_for_user(args.user, profile, verbose=args.verbose)
        log_pipeline_event(
            args.user,
            action="pipeline_run",
            mode="dry_run" if args.dry_run else "real",
            status="simulated" if args.dry_run else "executed",
        )
    else:
        user_profiles = load_user_profiles()
        if not user_profiles:
            print("🚫 No user profiles found.")
            sys.exit(1)

        print(f"👥 Running pipeline for {len(user_profiles)} user(s)...")
        for profile in user_profiles:
            user_id = profile["user_id"]
            print(f"\n🔧 Processing user: {user_id} (dry_run={args.dry_run})")
            if not args.dry_run:
                run_pipeline_for_user(user_id, profile, verbose=args.verbose)
            log_pipeline_event(
                user_id,
                action="pipeline_run",
                mode="dry_run" if args.dry_run else "real",
                status="simulated" if args.dry_run else "executed",
            )


if __name__ == "__main__":
    main()
