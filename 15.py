import requests
import json
import time
import base64
import random
import platform
import urllib.parse
import hashlib
from datetime import datetime, timedelta

APP_START_TIME = time.time()
TOTAL_REQUESTS = 0
GLOBAL_DISPLAY_IP = "***.***.***.***"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def log(msg):
    uptime_seconds = int(time.time() - APP_START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    print(f"[{uptime_str} | Tong Req: {TOTAL_REQUESTS}] {msg}")

class TyPhuBauTroi_Auto:
    def __init__(self, init_data, index):
        self.init_data = init_data
        self.index = index
        self.base_url = "https://typhubautroi.vercel.app/api"
        
        os_name = platform.system()
        machine = platform.machine()
        
        if os_name == "Windows":
            ua_os = "Windows NT 10.0; Win64; x64"
            sec_platform = '"Windows"'
        elif os_name == "Darwin":
            ua_os = "Macintosh; Intel Mac OS X 10_15_7"
            sec_platform = '"macOS"'
        elif os_name == "Linux":
            ua_os = "X11; Linux x86_64"
            sec_platform = '"Linux"'
        else:
            ua_os = f"{os_name}; {machine}"
            sec_platform = f'"{os_name}"'

        real_user_agent = f"Mozilla/5.0 ({ua_os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://typhubautroi.vercel.app",
            "Referer": "https://typhubautroi.vercel.app/",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": sec_platform,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": real_user_agent,
            "x-init-data": self.init_data
        }
        self.session.headers.update(self.headers)
        
        self.session_payload = None
        self.user_info = {"fullName": "User", "avatar": ""}
        self.round_requests = 0

    def send_api(self, endpoint, method="POST", body=None):
        global TOTAL_REQUESTS
        self.round_requests += 1
        TOTAL_REQUESTS += 1
        
        log(f"{Colors.BLUE}[API] Gui '{endpoint}' -> Req của ván này: {self.round_requests}{Colors.RESET}")
        
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "POST":
                response = self.session.post(url, json=body, timeout=15)
            else:
                response = self.session.get(url, timeout=15)
            return response
        except Exception as e:
            log(f"{Colors.RED}[LOI] Loi ket noi {endpoint}: {e}{Colors.RESET}")
            return None

    def get_user_info(self):
        try:
            parsed = urllib.parse.parse_qs(self.init_data)
            user_json = parsed.get('user', ['{}'])[0]
            data = json.loads(user_json)
            self.user_info['fullName'] = f"{data.get('first_name','')} {data.get('last_name','')}".strip()
            self.user_info['avatar'] = data.get('photo_url', "https://t.me/i/userpic/320/placeholder.svg")
            return data.get('username', 'Unknown')
        except:
            return "Unknown"

    def decode_jwt(self, token):
        try:
            payload_part = token.split('.')[1]
            payload_part += '=' * (-len(payload_part) % 4)
            decoded_bytes = base64.urlsafe_b64decode(payload_part)
            return json.loads(decoded_bytes)
        except Exception as e:
            log(f"{Colors.RED}[LOI] Khong the giai ma Token: {e}{Colors.RESET}")
            return {}

    def start(self):
        req_start_time = time.time()
        response = self.send_api("start", method="POST", body=None)
        
        if response and response.status_code in [200, 201]:
            try:
                data = response.json()
                if data.get('ok'):
                    self.session_payload = data.get('payload')
                    balance = data.get('balance', 0)
                    energy = data.get('energy', 0)
                    
                    jwt_data = self.decode_jwt(self.session_payload)
                    crash_ts = jwt_data.get('crashTime', 0)
                    iat_ts = jwt_data.get('iat', 0)
                    energy_lost = jwt_data.get('energyLost', 0)
                    
                    total_flight_duration = (crash_ts - (iat_ts * 1000)) / 1000.0
                    elapsed_time = time.time() - req_start_time
                    remaining_sec = total_flight_duration - elapsed_time
                    
                    log(f"{Colors.CYAN}[START] Thông tin cất cánh:{Colors.RESET}")
                    log(f"{Colors.CYAN} Ví hiện tạ : {balance}{Colors.RESET}")
                    log(f"{Colors.CYAN} Năng lượng  : {energy}{Colors.RESET}")
                    log(f"{Colors.CYAN} T.gian bay  : {total_flight_duration:.2f}s{Colors.RESET}")
                    log(f"{Colors.CYAN} Đặt cọc  : {energy_lost}{Colors.RESET}")
                    
                    if remaining_sec > 0:
                        safe_margin = random.uniform(1.5, 3.0)
                        wait_sec = remaining_sec - safe_margin
                        
                        if wait_sec > 0:
                            log(f"{Colors.YELLOW}[CHO] Tính toán delay nhảy dù:{Colors.RESET}")
                            log(f"{Colors.YELLOW} Mạng delay  : {elapsed_time:.2f}s{Colors.RESET}")
                            log(f"{Colors.YELLOW} Còn thực tế : {remaining_sec:.2f}s{Colors.RESET}")
                            log(f"{Colors.YELLOW} Trừ hao     : {safe_margin:.2f}s{Colors.RESET}")
                            log(f"{Colors.YELLOW} Đang chờ    : {wait_sec:.2f} giây...{Colors.RESET}")
                            time.sleep(wait_sec)
                        else:
                            log(f"{Colors.YELLOW}[CHO] Thời gian quá ngắn ({remaining_sec:.2f}s), ngảy dù ngay!{Colors.RESET}")
                            time.sleep(0.2)
                    else:
                        log(f"{Colors.YELLOW}[CHO] Tau da no do mang cham, nhay vot vat ngay!{Colors.RESET}")
                        
                    return True
                else:
                    log(f"{Colors.RED}[START] Server tu choi: {data}{Colors.RESET}")
            except Exception as e:
                log(f"{Colors.RED}[START] Loi phan tich phan hoi: {e}{Colors.RESET}")
        else:
            log(f"{Colors.RED}[START] Yeu cau that bai (Het nang luong hoac Loi HTTP).{Colors.RESET}")
        return False

    def jump(self):
        if not self.session_payload:
            return
            
        body = {
            "payload": self.session_payload,
            "fullName": self.user_info['fullName'],
            "avatar": self.user_info['avatar']
        }
        
        response = self.send_api("jump", method="POST", body=body)
        if response and response.status_code == 200:
            try:
                data = response.json()
                if data.get('ok'):
                    earned = data.get('earned', 0)
                    energy_lost = data.get('energyLost', 0)
                    refunded = data.get('refundedEnergy', 0)
                    
                    log(f"{Colors.GREEN}[JUMP] Nhảy dù THÀNH CÔNG:{Colors.RESET}")
                    log(f"{Colors.GREEN} Lợi nhuận   : +{earned}{Colors.RESET}")
                    log(f"{Colors.GREEN} bị trừ    : {energy_lost}{Colors.RESET}")
                    log(f"{Colors.GREEN} được hoàn : {refunded}{Colors.RESET}")
                else:
                    log(f"{Colors.RED}[JUMP] Nhay hut (Crashed): {data}{Colors.RESET}")
            except Exception as e:
                log(f"{Colors.RED}[JUMP] Loi du lieu nhay: {e}{Colors.RESET}")

    def run_cycle(self):
        user_name = self.get_user_info()
        print(f"\n{Colors.CYAN}======================================================{Colors.RESET}")
        log(f"{Colors.CYAN}[ACC] Tai khoan: {user_name}{Colors.RESET}")
        log(f"{Colors.CYAN}[THIET BI] IP: {GLOBAL_DISPLAY_IP}{Colors.RESET}")
        log(f"{Colors.CYAN}[THIET BI] Platform: {self.headers['Sec-Ch-Ua-Platform']}{Colors.RESET}")
        log(f"{Colors.CYAN}[THIET BI] U-Agent: {self.headers['User-Agent'][:45]}...{Colors.RESET}")
        print(f"{Colors.CYAN}------------------------------------------------------{Colors.RESET}")
        
        self.round_requests = 0 
        
        if self.start():
            self.jump()
            log(f"{Colors.GREEN}[HOAN THANH] Tổng req đã sử dụng ván này: {self.round_requests}{Colors.RESET}")
        else:
            log(f"{Colors.YELLOW}[DUNG] Bỏ qua ván này.{Colors.RESET}")

def get_short_link():
    base_url = "https://taixuongmienphi.click/s/key-tpbtz1u1fhcmlxym55y"
    unique_url = f"{base_url}?req={random.randint(1000000, 9999999)}"
    try:
        res = requests.get(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(unique_url)}", timeout=5)
        if res.status_code == 200:
            return res.text.strip()
    except:
        pass
    return unique_url

def verify_key(user_key, ip):
    secret = "TDK_TPBT_855678ALI"
    now = datetime.now()
    for i in range(25):
        t = now - timedelta(hours=i)
        raw_str = f"{t.strftime('%d/%m/%Y-%H')}-{secret}-{ip}"
        expected = hashlib.md5(raw_str.encode()).hexdigest()[:10]
        if user_key == expected:
            return True
    return False

def main():
    global GLOBAL_DISPLAY_IP
    print(f"{Colors.GREEN}=== TOOL TỈ PHÚ BẦU TRỜI ; ADMIN: DUONG PHUNG; ( TDK-TOOL ) ==={Colors.RESET}")
    print("------------------------------------------------------")

    current_ip = "127.0.0.1"
    try:
        current_ip = requests.get("https://api.ipify.org?format=json", timeout=5).json().get("ip")
    except:
        pass
        
    link_key = get_short_link()
    print(f"{Colors.YELLOW}Vui long lay key tai link sau:{Colors.RESET}")
    print(f"{Colors.CYAN}{link_key}{Colors.RESET}")
    
    user_key = input(f"{Colors.GREEN}Nhap key xac nhan (Hoat dong 24h): {Colors.RESET}").strip()
    
    if not verify_key(user_key, current_ip):
        print(f"{Colors.RED}Key khong hop le hoac da het han!{Colors.RESET}")
        return
        
    print(f"{Colors.GREEN}Xac thuc thanh cong! Key se het han sau 24h.{Colors.RESET}")
    print("------------------------------------------------------")

    ask_ip = input("Ban co muon hien thi IP thuc tren thong bao khong? (y/n): ").strip().lower()
    GLOBAL_DISPLAY_IP = current_ip if ask_ip == 'y' else "***.***.***.***"
    print(f"{Colors.GREEN}[+] Da xac nhan cau hinh IP.{Colors.RESET}\n")

    try:
        with open('data.txt', 'r') as f:
            accounts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}[LOI] Khong tim thay file data.txt{Colors.RESET}")
        return

    if not accounts:
        print(f"{Colors.RED}[LOI] File data.txt trong!{Colors.RESET}")
        return

    while True:
        for idx, init_data in enumerate(accounts):
            bot = TyPhuBauTroi_Auto(init_data, idx + 1)
            bot.run_cycle()
            
            delay = random.randint(100, 200)
            print(f"{Colors.CYAN}------------------------------------------------------{Colors.RESET}")
            log(f"{Colors.YELLOW}[SLEEP] Đang nghỉ ngơi {delay} giây chống spam...{Colors.RESET}")
            time.sleep(delay)

if __name__ == "__main__":
    main()
