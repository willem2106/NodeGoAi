import os, requests, time
from colorama import Fore, Style
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

def save_bearer_token():
    """Menyimpan Bearer Token ke dalam file jika belum ada."""
    file_name = "data.txt"
    print("\033[92m📜 File data.txt tidak ditemukan. Membuat file baru...\033[0m")
    bearer_token = input("\033[96m🔑 Masukkan Bearer Token: \033[0m")
    with open(file_name, "w") as file:
        file.write(bearer_token)
    print("\033[93m✅ Bearer Token berhasil disimpan di data.txt!\033[0m")
    return bearer_token

def load_bearer_token():
    """Memuat Bearer Token dari file atau meminta input jika file tidak ada."""
    file_name = "data.txt"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            bearer_token = file.read().strip()
        print("\033[94m📂 Bearer Token berhasil dimuat dari data.txt!\033[0m")
        return bearer_token
    else:
        return save_bearer_token()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

def print_banner():
    banner = r"""
    _   __          __                 ___    ____
   / | / /___  ____/ /__  ____ _____  /   |  /  _/
  /  |/ / __ \/ __  / _ \/ __ `/ __ \/ /| |  / /  
 / /|  / /_/ / /_/ /  __/ /_/ / /_/ / ___ |_/ /   
/_/ |_/\____/\__,_/\___/\__, /\____/_/  |_/___/   
                       /____/                     
"""
    print(Fore.MAGENTA + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "👨‍💻 Created by: @Python3pip" + Style.RESET_ALL)
    print(Fore.CYAN + f"🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Style.RESET_ALL)
    print("=" * 50)

print_banner()
bearer = load_bearer_token()

session = requests.Session()
retry = Retry(connect=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    response = session.get(
        'https://nodego.ai/api/user/me',
        headers={
            "Authorization": "Bearer " + bearer,
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
    )

    if response.status_code == 200:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            rprint(Panel("❌ [bold red]Gagal membaca data JSON dari server.[/]", title="🔴 Error", expand=False))
            exit()

        total_points = sum(node["totalPoint"] for node in data.get("metadata", {}).get("nodes", []))
        status_msg = "[bold green]✅ SUCCESS[/]" if response.status_code == 200 else "[bold red]❌ ERROR[/]"

        rprint(Panel(f"Status Code: {response.status_code} {status_msg}", title="📢 Server Response", expand=False))

        user_info = Table(title="👤 User Info")
        user_info.add_column("Field", style="bold cyan")
        user_info.add_column("Value", style="bold white")

        metadata = data.get("metadata", {})
        user_info.add_row("🆔 User ID", metadata.get("_id", "N/A"))
        user_info.add_row("📛 Username", metadata.get("username", "N/A"))
        user_info.add_row("📧 Email", metadata.get("email", "N/A"))
        user_info.add_row("🎭 Role", metadata.get("userRole", "N/A"))
        user_info.add_row("🔗 Referral Code", metadata.get("refCode", "N/A"))
        if metadata.get("refBy"):
            user_info.add_row("🔄 Referred By", metadata["refBy"])
        user_info.add_row("✅ Verified", "Yes ✅" if metadata.get("isVerified") else "No ❌")
        user_info.add_row("💰 Total Points", f"{total_points:.6f} 🌟")

        rprint(user_info)

        print("\033[96m🌐 Memulai ping ke server...\033[0m")

        headers = {
            "Authorization": "Bearer " + bearer,
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }

        while True:
            ping = session.post('https://nodego.ai/api/user/nodes/ping', headers=headers, json={"type": "extension"})
            if ping.status_code in (200, 201):
                rprint(Panel("✅ [bold green]Server terhubung! Ping berhasil. 🚀[/]", title="🟢 Connection Status", expand=False))
                time.sleep(180)
            elif ping.status_code == 429:
                rprint(Panel(f"⚠️ [bold yellow]Terlalu banyak permintaan! Menunggu 2 menit sebelum mencoba lagi... ⏳[/]", title="🟠 Rate Limit", expand=False))
                time.sleep(120)
            else:
                rprint(Panel(f"❌ [bold red]Gagal ping ke server! Status: {ping.status_code} ⚠️ Mencoba lagi...[/]", title="🔴 Connection Error", expand=False))
                time.sleep(60)

    else:
        rprint(Panel(f"❌ [bold red]Gagal mendapatkan data user! Status: {response.status_code}[/]", title="🔴 Error", expand=False))

except requests.exceptions.RequestException as e:
    rprint(Panel(f"❌ [bold red]Terjadi kesalahan jaringan: {str(e)}[/]", title="🔴 Network Error", expand=False))
