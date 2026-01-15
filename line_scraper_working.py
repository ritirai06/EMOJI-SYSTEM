import json, os, re, requests, time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By

Path("line_emojis").mkdir(exist_ok=True)
driver = webdriver.Chrome()
driver.get("https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions")
time.sleep(3)

# Click all Show all buttons
for btn in driver.find_elements(By.TAG_NAME, 'button'):
    if 'Show all' in btn.text:
        try: driver.execute_script("arguments[0].click();", btn); time.sleep(0.1)
        except: pass

time.sleep(1)
emoji_data = []

# Extract data
for section in driver.find_elements(By.CSS_SELECTOR, 'div[data-v-537568e6]'):
    try:
        product_id = section.find_element(By.CSS_SELECTOR, 'code[id^="product-"]').text.strip()
        for item in section.find_elements(By.CSS_SELECTOR, 'div.emoji-grid-item'):
            emoji_id = item.find_element(By.CSS_SELECTOR, 'code[id^="emoji-"]').text.strip()
            style = item.find_element(By.CSS_SELECTOR, 'div[style*="background: url"]').get_attribute('style')
            match = re.search(r'url\(["\']?(https://[^"\')\s]+)', style)
            if match:
                emoji_data.append({
                    "product_id": product_id,
                    "emoji_id": emoji_id,
                    "image_url": match.group(1).replace('&quot;', ''),
                    "filename": f"{product_id}_{emoji_id}.png"
                })
    except: pass

driver.quit()
print(f"Found {len(emoji_data)} emojis. Downloading...")

# Download with threading
from concurrent.futures import ThreadPoolExecutor

def download(e):
    try:
        r = requests.get(e['image_url'], timeout=5)
        if r.status_code == 200:
            with open(f"line_emojis/{e['filename']}", 'wb') as f: f.write(r.content)
            return e['filename']
    except: pass
    return None

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(download, emoji_data))
    
downloaded = [r for r in results if r]
print(f"\nDone! Downloaded {len(downloaded)}/{len(emoji_data)} emojis to 'line_emojis' folder")
