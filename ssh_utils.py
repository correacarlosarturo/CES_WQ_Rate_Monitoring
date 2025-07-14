import paramiko
from paramiko import RSAKey
from pathlib import Path

def open_proxy_tunnel(proxy_host, proxy_user, proxy_key_path, proxy_key_pass, ces_host, ces_user, ces_pass):
    """
    Opens a double-layered SSH connection using Paramiko only.
    Connects to proxy, opens tunnel to CES, connects to CES.
    Returns an active Paramiko SSHClient to CES device.
    """

    # Load private key
    key_path = Path(proxy_key_path).expanduser()
    if not key_path.exists():
        raise FileNotFoundError(f"Private key not found at: {key_path}")
    key = RSAKey.from_private_key_file(str(key_path), password=proxy_key_pass or None)

    print(f"[+] Connecting to SSH proxy {proxy_host} as {proxy_user}")
    proxy_transport = paramiko.Transport((proxy_host, 22))
    proxy_transport.connect(username=proxy_user, pkey=key)

    # Create channel from proxy to CES
    print(f"[+] Opening channel from proxy to CES host: {ces_host}")
    channel = proxy_transport.open_channel(
        "direct-tcpip",
        (ces_host, 22),          # destination
        ("127.0.0.1", 0)         # origin (us)
    )

    # Connect to CES using channel as socket
    print(f"[+] Connecting to CES via forwarded channel as {ces_user}")
    ces_client = paramiko.SSHClient()
    ces_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ces_client.connect(
        hostname=ces_host,
        username=ces_user,
        password=ces_pass,
        sock=channel
    )

    print("[✓] Connected to CES device.")
    return ces_client
