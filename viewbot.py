# Original code wasn't made by me, I just added title shit

import requests, random, ssl, ctypes, time
from threading import active_count, Thread
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

count = 0
views = []

def calculate_cpm():
    cpm = 0
    for i in views:
        if i + 60 > int(time.time()):
            cpm += 1
    return cpm

def calculate_cpm_s():
    cpm = 0
    for i in views:
        if i + 1 > int(time.time()):
            cpm += 1
    return cpm

def title_daemon():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW("Tiktok View Bot | Views: " + str(count) + " | VPM: " + str(calculate_cpm()) + " | VPS: " + str(calculate_cpm_s()))

def stats(item_id):
    global count
    while True:
        try:
            with r.post(f"https://api.toutiao50.com/aweme/v1/aweme/stats/?channel=googleplay&device_type=SM-G9250&device_id={random.randint(1000000000000000000, 9999999999999999999)}&os_version=10&version_code=220400&app_name=musically_go&device_platform=android&aid=1340", headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8", "user-agent": "com.zhiliaoapp.musically.go/220400 (Linux; U; Android 10; en_US; SM-G9250; Build/MMB25K.G9250ZTU5DPC5; Cronet/TTNetVersion:5f9540e5 2021-05-20 QuicVersion:47555d5a 2020-10-15)"}, data=f"item_id={item_id}&play_delta=1", stream=True, verify=False, timeout=10) as response:
                if (response.json()["status_code"] == 0):
                    count += 1
                    views.append(int(time.time()))
                    break
                else:
                    continue
        except:
            continue
    

item_id = str(input("Video Link: "))
if ("vm.tiktok.com" in item_id or "vt.tiktok.com" in item_id):
    item_id = r.head(item_id, stream=True, verify=False, allow_redirects=True).url.split("/")[5].split("?", 1)[0]
else:
    item_id = item_id.split("/")[5].split("?", 1)[0]
threads = int(input("Threads: "))
print("")
print("Sending views")

# Title
Thread(target=title_daemon, daemon=True).start()

for _ in iter(int, 1):
    while True:
        if (active_count() <= threads):
            Thread(target=(stats), args=(item_id,)).start()
            break
