# run_pipeline.py (patched with --dry-run, structured logging)

import os
import sys
import argparse
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.user_profile import load_user_profiles, load_user_profile
from control_plane.orchestrator import run_pipeline_for_user

PIPELINE_LOG_PATH = "logs/pipeline_log.jsonl"


def log_pipeline_run(user_id, dry_run):
    os.makedirs(os.path.dirname(PIPELINE_LOG_PATH), exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user_id,
        "action": "pipeline_run",
        "mode": "dry_run" if dry_run else "real",
        "status": "executed" if not dry_run else "simulated",
    }
    with open(PIPELINE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


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
        log_pipeline_run(args.user, args.dry_run)
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
            log_pipeline_run(user_id, args.dry_run)


if __name__ == "__main__":
    main()
