# CES_WQ_Rate_Monitoring# CES SSH Monitoring Tool (Cross-Platform Version)

## 🌍 Overview

This Python tool connects to a Cisco CES device through a secure proxy SSH tunnel, runs live queue monitoring commands,
parses the results, and returns a verdict (STUCK, SLOW, HEALTHY) based on output behavior — all in a fully cross-platform way.

## 📁 Project Structure

```
ces_monitor/
├── connect_to_ces.py         # Main entry point
├── ssh_utils.py              # Sets up tunnel and session using Paramiko only
├── work_queue_monitoring.py  # Runs 'workqueue rate 10' interactively
├── analyzer.py               # Analyzes collected data for verdict
├── config.py                 # Optional: global thresholds or constants
├── .env                      # Secure credentials and config
└── README.md                 # This file
```

## 🔐 .env Configuration

Example:

```
SSH_PROXY_HOST=f4-ssh.iphmx.com
SSH_PROXY_USER=dh-user
SSH_PROXY_KEY_PATH=C:/Users/you/.ssh/id_rsa
SSH_PROXY_KEY_PASSPHRASE=yourPassphraseIfAny
SSH_CES_HOSTNAME=esa1.test.iphmx.com
SSH_CES_USER=yourCESuser
SSH_CES_PASS=yourCESpassword
```

## 🧠 How It Works

1. `connect_to_ces.py` loads credentials from `.env` or CLI args.
2. Calls `open_proxy_tunnel()` in `ssh_utils.py` to:
   - Use Paramiko to connect to proxy server
   - Open a direct TCP channel to the CES device
   - Pipe that channel into a second Paramiko SSHClient (to CES)
3. Passes that session to `monitor_work_queue()` in `work_queue_monitoring.py`
   - Sends `workqueue rate 10`
   - Collects live output for 3 minutes
   - Sends `Ctrl+C` gracefully
4. Passes results to `analyze_samples()` in `analyzer.py`
   - Returns verdict: STUCK / SLOW / HEALTHY
5. Closes all channels and sessions safely

## 🚦 Verdict Logic

- **STUCK** → No output, In keeps growing
- **SLOW** → In >> Out, queue is flooding
- **HEALTHY** → In and Out are balanced

## 🚀 Future Ideas

- Webhook/email notifier on bad verdicts

---
