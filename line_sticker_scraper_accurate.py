import re, requests, time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

Path("line_stickers").mkdir(exist_ok=True)

options = Options()
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions")
    time.sleep(5)
    
    # Click all "Show all" buttons
    show_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Show all')]")
    for btn in show_buttons:
        try:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
        except: pass
    
    time.sleep(3)
    
    # Define exact package mappings from the provided data
    def get_package_id(sticker_id):
        sid = int(sticker_id)
        if 1988 <= sid <= 2027:
            return "446"
        elif 10855 <= sid <= 10894:
            return "789"
        elif 17839 <= sid <= 17878:
            return "1070"
        elif 10551376 <= sid <= 10551399:
            return "6136"
        elif 10979904 <= sid <= 10979927:
            return "6325"
        elif 11069848 <= sid <= 11069871:
            return "6359"
        elif 11087920 <= sid <= 11087943:
            return "6362"
        elif 11088016 <= sid <= 11088039:
            return "6370"
        elif 11825374 <= sid <= 11825397:
            return "6632"
        elif 16581242 <= sid <= 16581265:
            return "8515"
        elif 16581266 <= sid <= 16581289:
            return "8522"
        elif 16581290 <= sid <= 16581313:
            return "8525"
        elif 52002734 <= sid <= 52002773:
            return "11537"
        elif 51626494 <= sid <= 51626533:
            return "11538"
        elif 52114110 <= sid <= 52114149:
            return "11539"
        else:
            return "unknown"
    
    page_source = driver.page_source
    sticker_data = []
    
    # Find all sticker URLs
    sticker_urls = re.findall(r'https://[^"\'>\s]*sticker[^"\'>\s]*\.(?:png|jpg)', page_source)
    
    for url in sticker_urls:
        sticker_match = re.search(r'/(\d+)/', url)
        if sticker_match:
            sticker_id = sticker_match.group(1)
            package_id = get_package_id(sticker_id)
            
            if package_id != "unknown":
                sticker_data.append({
                    "package_id": package_id,
                    "sticker_id": sticker_id,
                    "image_url": url,
                    "filename": f"{package_id}_{sticker_id}.png"
                })
    
    # Remove duplicates
    seen = set()
    unique_stickers = []
    for s in sticker_data:
        key = (s['package_id'], s['sticker_id'])
        if key not in seen:
            seen.add(key)
            unique_stickers.append(s)
    
    print(f"Found {len(unique_stickers)} unique stickers. Downloading...")
    
    def download(s):
        try:
            r = requests.get(s['image_url'], timeout=10)
            if r.status_code == 200:
                with open(f"line_stickers/{s['filename']}", 'wb') as f: 
                    f.write(r.content)
                return s['filename']
        except: pass
        return None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(download, unique_stickers))
        
    downloaded = [r for r in results if r]
    print(f"Done! Downloaded {len(downloaded)}/{len(unique_stickers)} stickers")
    
    # Show package distribution
    packages = {}
    for s in unique_stickers:
        packages[s['package_id']] = packages.get(s['package_id'], 0) + 1
    print(f"Package distribution: {packages}")

finally:
    driver.quit()