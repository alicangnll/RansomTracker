import requests
import sqlite3
import json
import hashlib
import re
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

# Veritabanı bağlantısı ve tablo oluşturma
conn = sqlite3.connect("instance/data.db")
cur = conn.cursor()

# 2. POST verilerini çekme ve veritabanına ekleme
def discord_send_message(content, screenshot_path=None):
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1360155723081715792/hhJkkp6yFF5iCLp_ggSzmD6EHXiKi6uSTP5Pf0TcyFNeXPhHCzBz1Qz_MFqB5XZ0qGPH"
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    
    files = {}
    if screenshot_path:
        try:
            # Ekran görüntüsünü dosya olarak ekle
            with open(screenshot_path, "rb") as screenshot_file:
                files = {"file": screenshot_file}
        except FileNotFoundError:
            print(f"Ekran görüntüsü dosyası bulunamadı: {screenshot_path}")
            files = {}

    try:
        # Webhook'a veri gönder
        response = requests.post(DISCORD_WEBHOOK_URL, data=data, headers=headers, files=files)
        
        if response.status_code == 200:
            print("Discord mesajı ve ekran görüntüsü gönderildi.")
        else:
            print("Discord mesajı gönderilemedi:", response.status_code)
    except Exception as e:
        print("Discord mesaj hatası:", e)

# playwright install-deps and playwright install komutunu girmeyi unutma!
def capture_screenshot(url, output_filename):
    if url and url != "None" and len(url.strip()) > 0:
        try:
            with sync_playwright() as p:
                print(str(url) + " sitesine bağlanıyor...")
                browser = p.chromium.launch(proxy={"server": "socks5://127.0.0.1:9055"}, args=[''])
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                page.goto(url, wait_until='load', timeout=15000)
                page.bring_to_front()
                page.wait_for_timeout(15000)
                page.mouse.move(x=500, y=400)
                page.wait_for_load_state('networkidle')
                page.mouse.wheel(delta_y=2000, delta_x=0)
                page.wait_for_load_state('networkidle')
                if not os.path.exists("screenshot"):
                    os.makedirs("screenshot")
                page.screenshot(path=output_filename, full_page=True)
                return output_filename
        except:
            return "ConnectionError"
    else:
        return "None"

def generate_md5_from_string(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))  # Veriyi encode edip hash'e ekliyoruz
    return str(md5_hash.hexdigest())  # Hash'i hexadecimal (hex) formatında döndürür

# 1. GRUP verilerini çekme ve veritabanına ekleme
def fetch_and_store_groups():
    print("Gruplar alınıyor...")
    response = requests.get("https://api.ransomware.live/v2/groups")
    if response.status_code == 200:
        groups = response.json()
        for group in groups:
            name = group.get("name", "None")
            url = group.get("url", "None")

            # Aynı name ve url varsa kaydı atla
            cur.execute("""
                SELECT * FROM groups WHERE name = ? AND url = ?
            """, (name, url))

            if cur.fetchone():
                print(f"Zaten mevcut: {name}, atlanıyor.")
            else:
                discord_msg = f"SyberCTI Bot\n🇹🇷 Yeni bir tehdit aktörü keşfedildi.\nAdı : {name}\nWebsitesi : {url}"
                discord_send_message(discord_msg, screenshot_path=None)
                cur.execute("""
                            INSERT OR REPLACE INTO groups (locations, meta, name, profile, tools, ttps, url)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                json.dumps(group.get("locations")),
                                group.get("meta", "None"),
                                name,
                                json.dumps(group.get("profile")),
                                json.dumps(group.get("tools")),
                                json.dumps(group.get("ttps")),
                                url
                                ))
                print(str(group.get("name", "None")) + " başarıyla kaydedildi")
                conn.commit()
                print(f"{name} başarıyla kaydedildi")
            print(f"{len(groups)} grup işlendi.")
    else:
        print("Gruplar alınamadı:", response.status_code)
    
def fetch_and_store_posts():
    print("Postlar alınıyor...")
    response = requests.get("https://data.ransomware.live/posts.json")
    if response.status_code == 200:
        posts = response.json()
        for post in posts:
            # Gerekli alanları al
            group_name = post.get("group_name", "None")
            post_url = post.get('post_url', 'None')
            post_title = post.get("post_title", "None")
            discovered = post.get("discovered", "None")
            published = post.get("published", "None")
            website = post.get("website", "None")
            country = post.get("country", "None")
            if post_url == "" or post_url is None:
                post_url = "Herhangi bir onion link bulunamadı ve/veya onion link üzerinde paylaşılmadı"
            # Veritabanında bu kayıt zaten var mı?
            cur.execute("""
                SELECT * FROM posts
                WHERE title = ? AND discovered = ? AND published = ? AND website = ? AND country = ?
            """, (post_title, discovered, published, website, country))

            if cur.fetchone():
                print(f"Zaten mevcut: {post_title}, atlanıyor.")
                continue  # Bu kayıt zaten varsa, atla
            else:
                get_screenshot = capture_screenshot(
                    str(post.get("post_url", "None")),
                    "screenshots/" + generate_md5_from_string(post_title) + ".png"
                    )
                # Yeni kayıt ekle
                if country == "TR":
                    discord_msg = f"SyberCTI Bot\n🇹🇷 Yeni yetkisiz erişim saldırısına uğrayan alan: {post_title}\nTehdit Aktörü Adı :\n{group_name}🔗\nWebsitesi : {website}\nTarih : {published}\nSızıntı URL : {post_url}"
                    discord_send_message(discord_msg, screenshot_path="screenshots/" + generate_md5_from_string(post_title) + ".png")
                elif country == "None" or country == "":
                    if website != "None" or website != "":
                        pattern = r'https?://(?:[\w.-]+\.)?[\w-]+\.(?:com|ct)\.tr(?:/[^\s]*)?|(?:[\w-]+\.)?[\w-]+\.(?:com|ct)\.tr'
                        matches = re.findall(pattern, website)
                        for match in matches:
                            discord_msg = f"SyberCTI Bot\n🇹🇷 Yeni yetkisiz erişim saldırısına uğrayan alan: {match}\nTehdit Aktörü Adı :\n{group_name}🔗\nTarih : {published}\nSızıntı URL : {post_url}"
                            discord_send_message(discord_msg, screenshot_path="screenshots/" + generate_md5_from_string(post_title) + ".png")
                cur.execute("""
                            INSERT OR REPLACE INTO posts (title, name, description, discovered, published, post_url, country, activity, website, duplicates, screenshot)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                post_title,
                                post.get("group_name", "None"),
                                post.get("description", "None"),
                                discovered,
                                published,
                                post.get("post_url", "None"),
                                country,
                                post.get("activity", "None"),
                                website,
                                json.dumps(post.get("duplicates")),
                                get_screenshot
                                ))
                print(f"{post_title} başarıyla kaydedildi")
                conn.commit()
        print(f"{len(posts)} post işlendi.")
    else:
        return "None"


if __name__ == "__main__":
    while(True):
        fetch_and_store_groups()
        fetch_and_store_posts()
        print("İşlem tamamlandı.")
