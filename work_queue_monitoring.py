import time
import re

def monitor_work_queue(client, command="workqueue rate 10", duration=180):
    """
    Runs a live CES monitoring command in an interactive shell over SSH.
    Collects output for the given duration, then sends Ctrl+C to stop the command.

    Returns:
        samples (list of dict): parsed queue metrics from each sample line.
    """
    print(f"[+] Executing '{command}' for {duration} seconds...")

    channel = client.invoke_shell()
    channel.settimeout(2)
    channel.send(command + "\n")
    time.sleep(2)

    samples = []
    start = time.time()

    try:
        while time.time() - start < duration:
            if channel.recv_ready():
                output = channel.recv(4096).decode("utf-8", errors="ignore")
                lines = output.strip().splitlines()

                for line in lines:
                    match = re.search(r"\d{2}:\d{2}:\d{2}\s+(\d+)\s+(\d+)\s+(\d+)", line)
                    if match:
                        pending, in_count, out_count = map(int, match.groups())
                        delta = in_count - out_count
                        samples.append({"in": in_count, "out": out_count, "delta": delta})
                        print(f"[Sample] In: {in_count}, Out: {out_count}, Δ: {delta}")
            time.sleep(1)

    finally:
        # Gracefully stop the interactive command
        print("[*] Sending Ctrl+C to stop CES monitoring command...")
        channel.send("\x03")  # Ctrl+C
        time.sleep(1)
        channel.close()

    return samples
