import os
import sys
import argparse

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.user_profile import load_user_profiles, load_user_profile
from control_plane.orchestrator import run_pipeline_for_user

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, help="Run pipeline for specific user ID")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.user:
        profile = load_user_profile(args.user)
        if not profile:
            print(f"🚫 No profile found for user '{args.user}'")
            sys.exit(1)
        print(f"🔧 Running pipeline for user: {args.user}")
        run_pipeline_for_user(args.user, profile, verbose=args.verbose)
    else:
        user_profiles = load_user_profiles()
        if not user_profiles:
            print("🚫 No user profiles found.")
            sys.exit(1)

        print(f"👥 Running pipeline for {len(user_profiles)} user(s)...")
        for profile in user_profiles:
            user_id = profile["user_id"]
            print(f"\n🔧 Processing user: {user_id}")
            run_pipeline_for_user(user_id, profile, verbose=args.verbose)
