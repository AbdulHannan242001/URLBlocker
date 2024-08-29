import os
import sys
import platform
import ctypes


def is_admin():
    """Checks if the script is running with administrator privileges (Windows only)."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def toggle_block_urls(urls):
    """Blocks or unblocks the specified URLs using the hosts file."""

    log_file = "block_urls_log.txt"

    def log_message(message):
        """Writes a message to the log file and prints it to the console."""
        with open(log_file, 'a') as log:
            log.write(message + "\n")
        print(message)

    log_message("Blocking/Unblocking URLs...")

    hosts_file = {
        'Windows': r'C:\Windows\System32\drivers\etc\hosts',
        'Linux': '/etc/hosts',
        'Darwin': '/etc/hosts'  # macOS
    }[platform.system()]

    redirect_ip = "127.0.0.1"

    with open(hosts_file, 'r') as file:
        content = file.readlines()

    # Combine base URL and www prefix checking
    urls_to_check = [url for url in urls] + [f"www.{url}" for url in urls]

    urls_blocked = all(any(redirect_ip in line and url in line for line in content) for url in urls_to_check)

    if urls_blocked:
        # Unblock URLs
        with open(hosts_file, 'w') as file:
            for line in content:
                if not any(redirect_ip in line and url in line for url in urls_to_check):
                    file.write(line)
        log_message("URLs unblocked successfully!")
    else:
        # Block URLs
        with open(hosts_file, 'a') as file:
            for url in urls_to_check:
                file.write(f"{redirect_ip} {url}\n")
        log_message("URLs blocked successfully!")

    # Clear DNS cache (Windows only)
    if platform.system() == 'Windows':
        os.system('ipconfig /flushdns')


if platform.system() == 'Windows' and not is_admin():
    # Re-run the script as admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
else:
    # List of URLs to block/unblock
    urls_to_toggle = [
        "youtube.com",
        "facebook.com",
        "instagram.com"
    ]
    toggle_block_urls(urls_to_toggle)