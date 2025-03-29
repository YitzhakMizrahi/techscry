import os
import sys

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.user_profile import load_user_profiles
from control_plane.orchestrator import run_pipeline_for_user

if __name__ == "__main__":
    user_profiles = load_user_profiles()
    if not user_profiles:
        print("🚫 No user profiles found.")
        sys.exit(1)

    print(f"👥 Running pipeline for {len(user_profiles)} user(s)...")
    for profile in user_profiles:
        user_id = profile["user_id"]
        print(f"\n🔧 Processing user: {user_id}")
        run_pipeline_for_user(user_id, profile)
