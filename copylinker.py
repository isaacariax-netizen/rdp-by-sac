#coded by @chyoo_eyes
#do not edit it!!!
import os
import requests
import time
import secrets
import binascii
import uuid
import random
import SignerPy
import subprocess
from concurrent.futures import ThreadPoolExecutor
import threading

print(r'''
░█████╗░██╗░░██╗██╗░░░██╗░█████╗░
██╔══██╗██║░░██║╚██╗░██╔╝██╔══██╗
██║░░╚═╝███████║░╚████╔╝░██║░░██║
██║░░██╗██╔══██║░░╚██╔╝░░██║░░██║
╚█████╔╝██║░░██║░░░██║░░░╚█████╔╝
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  TikTok CopyLink
- By CHYØ
- Telegram: t.me/chyoo_eyes
''')


def get_device_info():
    try:    m = subprocess.getoutput("getprop ro.product.model").strip()
    except: m = "SM-A127F"
    try:    b = subprocess.getoutput("getprop ro.product.brand").strip()
    except: b = "samsung"
    try:    c = subprocess.getoutput("getprop ro.build.display.id").strip()
    except: c = "RP1A.200720.011"
    return m, b, c

MODEL, BRAND, BUILD = get_device_info()


def build_common_params():
    return {
        "device_id": str(random.randint(10**17,10**19)),
        "iid":       str(random.randint(10**17,10**19)),
        "openudid":  binascii.hexlify(os.urandom(8)).decode(),
        "cdid":      str(uuid.uuid4()),
        "app_name":           "musical_ly",
        "version_code":       "390603",
        "version_name":       "39.6.3",
        "app_version":        "39.6.3",
        "manifest_version_code": "2023906030",
        "update_version_code":   "2023906030",
        "ab_version":            "39.6.3",
        "resolution":            "1080*2220",
        "dpi":                   "440",
        "device_platform":       "android",
        "device_type":           MODEL,
        "device_brand":          BRAND,
        "os_api":                "30",
        "os_version":            "11",
        "os":                    "android",
        "host_abi":              "arm64-v8a",
        "language":              "ar",
        "locale":                "ar",
        "region":                "EG",
        "current_region":        "YE",
        "sys_region":            "EG",
        "carrier_region":        "YE",
        "residence":             "YE",
        "app_language":          "ar",
        "app_type":              "normal",
        "channel":               "googleplay",
        "aid":                   "1233",
        "ts":                    str(int(time.time())),
        "_rticket":              str(int(time.time()*1000))
    }


class ChyooCopy:
    def __init__(self, sessionid, video_id):
        self.sessionid = sessionid
        self.video_id = video_id
        self.csrf = secrets.token_hex(16)
        # prepare cookies
        self.cookies = {
            'sessionid': sessionid,
            'sid_tt': sessionid,
            'passport_csrf_token': self.csrf,
            'passport_csrf_token_default': self.csrf
        }
        
        self.headers = {
            'User-Agent': f'com.tiktok.lite.go/390054 (Linux; U; Android 13; en_GB; {MODEL}; Build/{BUILD};tt-ok/3.12.13.34-ul)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def copy_link(self):
        params = build_common_params()
        params.update({
            'share_delta': '1',
            'stats_channel': 'copy',
            'item_id': self.video_id
        })
        sig = SignerPy.sign(params=params, cookie=self.cookies)

        hdr = self.headers.copy()
        hdr['x-tt-passport-csrf-token'] = self.csrf
        hdr.update(sig)
        hdr['Cookie'] = '; '.join(f'{k}={v}' for k,v in self.cookies.items())

        url = 'https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/'
        try:
            r = requests.post(url, params=params, headers=hdr, cookies=self.cookies)
            j = r.json()
            if j.get('status_code') == 0:
                link = f"https://www.tiktok.com/@/video/{self.video_id}"
                print(f"\033[92m[{self.sessionid}] By CHYO\033[0m")
            else:
                print(f"\033[91m[{self.sessionid}] Failed: {j}\033[0m")
        except Exception as e:
            print(f"\033[91m[{self.sessionid}] Exception: {e}\033[0m")

if __name__ == '__main__':
    path = input('Enter session IDs file path: ').strip()
    video_id = input('Enter TikTok Video ID: ').strip()
    if not os.path.isfile(path):
        print('\033[91mFile not found\033[0m')
        exit()
    sessions = open(path, 'r').read().splitlines()
   
    with ThreadPoolExecutor(max_workers=150) as exe:
        for sess in sessions:
            exe.submit(ChyooCopy(sess.strip(), video_id).copy_link)
        #    Coded By CHYO Xoshnaw
        
  #      Script developed by
    #    chyoo_eyes
