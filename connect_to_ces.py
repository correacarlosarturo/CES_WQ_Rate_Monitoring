import os
import argparse
from dotenv import load_dotenv
from ssh_utils import open_proxy_tunnel
from work_queue_monitoring import monitor_work_queue
from analyzer import analyze_samples

# Load .env values
load_dotenv()

def parse_args():
    """Parse CLI arguments for overriding .env values."""
    parser = argparse.ArgumentParser(description="Connect to CES via SSH proxy and monitor queue stats.")
    parser.add_argument("--proxy-host")
    parser.add_argument("--proxy-user")
    parser.add_argument("--proxy-key")
    parser.add_argument("--proxy-key-pass")
    parser.add_argument("--ces-host")
    parser.add_argument("--ces-user")
    parser.add_argument("--ces-pass")
    parser.add_argument("--command", default="workqueue rate 10")
    parser.add_argument("--duration", type=int, default=180)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    proxy_host = args.proxy_host or os.getenv("SSH_PROXY_HOST")
    proxy_user = args.proxy_user or os.getenv("SSH_PROXY_USER")
    proxy_key  = args.proxy_key  or os.getenv("SSH_PROXY_KEY_PATH")
    proxy_pass = args.proxy_key_pass or os.getenv("SSH_PROXY_KEY_PASSPHRASE")
    ces_host   = args.ces_host   or os.getenv("SSH_CES_HOSTNAME")
    ces_user   = args.ces_user   or os.getenv("SSH_CES_USER")
    ces_pass   = args.ces_pass   or os.getenv("SSH_CES_PASS")
    command    = args.command
    duration   = args.duration

    if not all([proxy_host, proxy_user, proxy_key, ces_host, ces_user]):
        raise ValueError("Missing required connection info. Check CLI args or .env file.")

    client = open_proxy_tunnel(proxy_host, proxy_user, proxy_key, proxy_pass, ces_host, ces_user, ces_pass)
    samples = monitor_work_queue(client, command=command, duration=duration)
    verdict = analyze_samples(samples)

    client.close()
    print(f"[+] SSH session closed. Verdict: {verdict}")
