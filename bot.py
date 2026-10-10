mport os
import time
import random
import requests

# استدعاء الكوكي والمعلومات من المتغيرات البيئية بأمان
ROBLOSECURITY_COOKIE = os.getenv("ROBLOSECURITY", "")
PLACE_ID = int(os.getenv("PLACE_ID", "109983668079237
"))  # ضع Place ID اللعبة هنا أو من إعدادات المنصة
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://discord.com/api/webhooks/1558449981155967121/MR8Kd79GkVf5jminIXlKAV0LNZlyPqrxG8JVQyty_e4QkJ_rAF75AU7woPwUIj7gu3GO")

# إعداد الجلسة والهيدرز الخاصة بروبلوكس لتجاوز الحماية
session = requests.Session()
if ROBLOSECURITY_COOKIE:
    session.cookies.set(".ROBLOSECURITY", ROBLOSECURITY_COOKIE, domain=".roblox.com")

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.roblox.com/"
})

def send_to_discord(job_id, players_count):
    """إرسال تنبيه السيرفر إلى ديسكورد"""
    payload = {
        "content": "🚨 **تم رصد سيرفر جديد عبر السحابة 24/7!**",
        "embeds": [
            {
                "title": "🌍 معلومات السيرفر المتاح",
                "color": 65280, # أخضر
                "fields": [
                    {"name": "👥 عدد اللاعبين", "value": str(players_count), "inline": True},
                    {"name": "Server JobId", "value": f"`{job_id}`", "inline": False},
                    {"name": "⚡ طريقة الدخول", "value": "انسخ الـ JobId وادخل مباشرة للحساب!", "inline": False}
                ]
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("[+] تم إرسال الـ JobId بنجاح إلى ديسكورد!")
    except Exception as e:
        print(f"[-] خطأ في إرسال الـ Webhook: {e}")

def main():
    print("🤖 بدأ تشغيل بوت البايثون السحابي لفحص السيرفرات...")
    
    if not ROBLOSECURITY_COOKIE:
        print("[-] تحذير: لم يتم العثور على كوكي الحساب! سيتم الفحص بدون صلاحيات كاملة.")

    while True:
        try:
            # جلب قائمة السيرفرات العامة للعبة
            url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?sortOrder=Asc&limit=100"
            response = session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                servers = [s for s in data.get("data", []) if s.get("playing", 0) < s.get("maxPlayers", 0)]
                
                if servers:
                    target_server = random.choice(servers)
                    job_id = target_server.get("id")
                    players_count = target_server.get("playing")
                    
                    print(f"[*] تم فحص سيرفر فيه {players_count} لاعبين... (ID: {job_id[:8]}...)")
                    
                    # إرسال السيرفر للديسكورد
                    send_to_discord(job_id, players_count)
                    
                    time.sleep(60) # الانتظار دقيقة قبل الفحص التالي
                else:
                    print("[-] لا توجد سيرفرات متاحة حالياً...")
            else:
                print(f"[-] خطأ في الاتصال بروبلوكس، الرمز: {response.status_code} (تأكد من صلاحية الكوكي)")
                
        except Exception as e:
            print(f"[-] حدث خطأ غير متوقع: {e}")
            
        time.sleep(15)

if __name__ == "__main__":
    main()
