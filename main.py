import re
import time
import threading
import tkinter as tk
import vlc
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

MAPS_URL = "http://maps.ufanet.ru/nizhnij-novgorod#1712127689UPE47"
RESOLUTION = "1024x768"


if '#' in MAPS_URL:
    ID = MAPS_URL.split('#')[1]
else:
    raise ValueError("В URL отсутствует символ '#' с ID камеры")

FILE_NAME = "index.m3u8"
IP_REGEX = r"http://([\d\.]+)"
TOKEN_REGEX = r"token=([a-f0-9]{32})"
TOKEN_REFRESH_INTERVAL = 60

class CamStreamWindow:
    def __init__(self):
        self.token = None
        self.ip = None
        self.driver = None
        self.root = tk.Tk()
        self.root.title("Камера")
        self.root.geometry(RESOLUTION)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.embed = tk.Frame(self.root, bg="black")
        self.embed.pack(fill=tk.BOTH, expand=1)
        self.root.update()
        self._set_window_handle()
        self.token_thread = threading.Thread(target=self.token_update_loop, daemon=True)
        self.token_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def start_browser(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(30)

    def get_ip_and_token_from_iframe(self):
        try:
            self.driver.delete_all_cookies()
            self.driver.get(MAPS_URL)
            time.sleep(7)

            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                src = iframe.get_attribute("src")
                if src and "embed.html?token=" in src:
                    ip_match = re.search(IP_REGEX, src)
                    token_match = re.search(TOKEN_REGEX, src)
                    if ip_match and token_match:
                        ip_found = ip_match.group(1)
                        token_found = token_match.group(1)
                        print(f"[INFO] Найден IP: {ip_found}, токен: {token_found}")
                        return ip_found, token_found
            print("[WARN] Iframe со ссылкой не найден, src не содержит embed.html?token=")
        except Exception as e:
            print(f"[ERROR] Ошибка поиска IP/токена через iframe: {e}")
        return None, None

    def _set_window_handle(self):
        wid = self.embed.winfo_id()
        if sys.platform.startswith('linux'):
            self.player.set_xwindow(wid)
        elif sys.platform == "win32":
            self.player.set_hwnd(wid)
        elif sys.platform == "darwin":
            self.player.set_nsobject(wid)

    def play_stream(self, ip, token):
        stream_url = f"http://{ip}/{ID}/{FILE_NAME}?token={token}"
        print(f"[INFO] Запуск потока: {stream_url}")
        media = self.instance.media_new(stream_url)
        self.player.set_media(media)
        self._set_window_handle()
        self.player.play()

    def token_update_loop(self):
        self.start_browser()
        while True:
            ip, token = self.get_ip_and_token_from_iframe()
            if ip and token:
                if (ip != self.ip) or (token != self.token):
                    self.ip = ip
                    self.token = token
                    self.play_stream(ip, token)
                else:
                    print("[INFO] IP и токен не изменились, перезапуск не нужен.")
            else:
                print("[WARN] Не удалось получить IP или токен, повтор через время.")
            time.sleep(TOKEN_REFRESH_INTERVAL)

    def on_close(self):
        print("[INFO] Завершение работы")
        if self.player:
            self.player.stop()
        if self.driver:
            self.driver.quit()
        self.root.destroy()

if __name__ == "__main__":
    CamStreamWindow()
