# techscry/loop_runner.py

import time
import subprocess
import argparse
import sys


def loop_runner(script_path, script_args, interval):
    args_display = " ".join(script_args) if script_args else ""
    print(f"🔁 Starting loop: {script_path} {args_display} (every {interval}s)")
    try:
        while True:
            print("\n⏱️ Running script at:", time.strftime("%Y-%m-%d %H:%M:%S"))
            try:
                subprocess.run([sys.executable, script_path] + script_args, check=False)
            except Exception as e:
                print("⚠️ Script execution failed:", e)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Loop interrupted. Exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True, help="Path to script to run in loop")
    parser.add_argument(
        "--args", nargs=argparse.REMAINDER, help="Args to pass to the script"
    )
    parser.add_argument("--interval", type=int, default=900, help="Interval in seconds")
    args = parser.parse_args()

    loop_runner(args.script, args.args or [], args.interval)
