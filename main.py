import os,requests,time
from colorama import Fore, Style
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
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
    # Untuk Windows
    if os.name == 'nt':
        os.system('cls')
    # Untuk Linux / macOS
    else:
        os.system('clear')

# Contoh pemanggilan fungsi
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
    print(Fore.YELLOW + f"👨‍💻 Created by: @Python3pip" + Style.RESET_ALL)
    print(Fore.CYAN + f"🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Style.RESET_ALL)
    print("="*50)
print_banner()
barier = load_bearer_token()
session = requests.Session()
retry = Retry(connect=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
info = session.get('https://nodego.ai/api/user/me',headers={
    "Host": "nodego.ai",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": "\"Windows\"",
    "Authorization": "Bearer "+barier,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua-mobile": "?0",
    "Origin": "https://app.nodego.ai",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://app.nodego.ai/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "If-None-Match": "W/\"385-Ed7sjmewlLtFmWf+Hf4zIb2L1E0\""
})
if info.status_code == 200:
    data = info.json()
    def format_time(timestamp):
        return datetime.fromisoformat(timestamp.replace("Z", "")).strftime("%Y-%m-%d %H:%M:%S")

    # Header Status
    total_points = sum(node["totalPoint"] for node in data["metadata"]["nodes"])

    # Status Response
    status = data["statusCode"]
    status_msg = "[bold green]✅ SUCCESS[/]" if status == 200 else "[bold red]❌ ERROR[/]"
    rprint(Panel(f"Status Code: {status} {status_msg}", title="📢 [bold cyan]Server Response[/]", expand=False))

    # Info User
    user_info = Table(title="👤 User Info")
    user_info.add_column("Field", style="bold cyan")
    user_info.add_column("Value", style="bold white")
    user_info.add_row("🆔 User ID", data["metadata"]["_id"])
    user_info.add_row("📛 Username", data["metadata"]["username"])
    user_info.add_row("📧 Email", data["metadata"]["email"])
    user_info.add_row("🎭 Role", data["metadata"]["userRole"])
    user_info.add_row("🔗 Referral Code", data["metadata"]["refCode"])
    user_info.add_row("🔄 Referred By", data["metadata"]["refBy"])
    user_info.add_row("✅ Verified", "Yes ✅" if data["metadata"]["isVerified"] else "No ❌")
    user_info.add_row("🕒 Account Created", format_time(data["metadata"]["createdAt"]))
    user_info.add_row("💰 Total Points", f"{total_points:.6f} 🌟")  # Tambahkan total point

    rprint(user_info)

    # Info Node
    for node in data["metadata"]["nodes"]:
        node_info = Table(title="🖥️ Node Info")
        node_info.add_column("Field", style="bold cyan")
        node_info.add_column("Value", style="bold white")
        node_info.add_row("🌍 IP Address", node["id"])
        node_info.add_row("🔋 Active", "Yes ✅" if node["isActive"] else "No ❌")
        node_info.add_row("📊 Total Points", f"{node['totalPoint']:.6f} 🌟")
        node_info.add_row("📅 Today's Points", f"{node['todayPoint']:.6f} ⭐")
        node_info.add_row("🕒 Last Connected", format_time(node["lastConnectedAt"]))
        node_info.add_row("⏳ Uptime (sec)", f"{node['totalUptime']:.2f} ⏲️")
        node_info.add_row("🌎 Country", node["countryCode"])
        rprint(node_info)
    print("\033[96m🌐 Memulai ping ke server...\033[0m")
    headers = {
        "Host": "nodego.ai",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Authorization": "Bearer "+barier,
        "Accept": "*/*",
        "Origin": "chrome-extension://jbmdcnidiaknboflpljihfnbonjgegah",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Storage-Access": "active",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9"
    }
    while True:
        ping = session.post('https://nodego.ai/api/user/nodes/ping',headers=headers,json={"type":"extension"})
        if ping.status_code in (200, 201):
            rprint(Panel("✅ [bold green]Server terhubung! Ping berhasil. 🚀[/]", title="🟢 Connection Status", expand=False))
            time.sleep(3 * 60)
        elif ping.status_code == 429:
            wait_time = 2 * 60
            rprint(Panel(f"⚠️ [bold yellow]Terlalu banyak permintaan! Menunggu {wait_time} detik sebelum mencoba lagi... ⏳[/]", title="🟠 Rate Limit", expand=False))
            time.sleep(wait_time)
        else:
            rprint(Panel("❌ [bold red]Gagal terhubung ke server. ⚠️ Mencoba lagi...[/]", title="🔴 Connection Error", expand=False))

