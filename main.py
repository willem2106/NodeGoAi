import os, requests, time
from colorama import Fore, Style
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

def save_bearer_token():
    file_name = "data.txt"
    print("\033[92m📜 File data.txt tidak ditemukan. Membuat file baru...\033[0m")
    bearer_token = input("\033[96m🔑 Masukkan Bearer Token: \033[0m").strip()
    
    if not bearer_token:
        print("\033[91m❌ Bearer Token tidak boleh kosong!\033[0m")
        return save_bearer_token()
    
    with open(file_name, "w") as file:
        file.write(bearer_token)
    print("\033[93m✅ Bearer Token berhasil disimpan di data.txt!\033[0m")
    return bearer_token

def load_bearer_token():
    file_name = "data.txt"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            bearer_token = file.read().strip()
        if not bearer_token:
            return save_bearer_token()
        print("\033[94m📂 Bearer Token berhasil dimuat dari data.txt!\033[0m")
        return bearer_token
    else:
        return save_bearer_token()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = r"""
    _   __          __                 ___    ____
   / | / /___  ____/ /__  ____ _____  /   |  /  _/
  /  |/ / __ \/ __  / _ \/ __ `/ __ \/ /| |  / /  
 / /|  / /_/ / /_/ /  __/ /_/ / /_/ / ___ |_/ /   
/_/ |_\____/\__,_/\___/\__, /\____/_/  |_/___/   
                       /____/                     
"""
    print(Fore.MAGENTA + banner + Style.RESET_ALL)
    print(Fore.YELLOW + f"👨‍💻 Created by: @Python3pip" + Style.RESET_ALL)
    print(Fore.CYAN + f"🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Style.RESET_ALL)
    print("="*50)

clear_screen()
print_banner()
bearer_token = load_bearer_token()

session = requests.Session()
retry = Retry(connect=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    info = session.get(
        'https://nodego.ai/api/user/me',
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )
    if info.status_code == 200:
        try:
            data = info.json()
        except requests.exceptions.JSONDecodeError:
            rprint(Panel("❌ [bold red]Gagal mengurai JSON! Mungkin server tidak merespons dengan benar.[/]", title="🔴 JSON Error"))
            exit()
    else:
        rprint(Panel(f"⚠️ [bold yellow]Request gagal dengan status {info.status_code}: {info.text}[/]", title="🟠 HTTP Error"))
        exit()
except requests.RequestException as e:
    rprint(Panel(f"❌ [bold red]Terjadi kesalahan koneksi: {str(e)}[/]", title="🔴 Connection Error"))
    exit()
