import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Tarayıcıyı gizli modda çalıştırma
options = Options()
options.headless = True  # Tarayıcıyı gizli modda çalıştır

# WebDriver'ı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Web sitesinin temel URL'si ve sayfa aralığı
base_url = "https://www.itopya.com/notebook_k14?pg="
pages = range(1, 10)  # 1'den 9'a kadar olan sayfalar

def get_all_links():
    """
    Verilen sayfalarda bulunan tüm ürün linklerini alır.
    """
    all_links = []
    
    for page_num in pages:
        url = f"{base_url}{page_num}"
        response = requests.get(url)  # Sayfayı çek
        soup = BeautifulSoup(response.text, 'html.parser')  # HTML içeriği parse et
        
        # Her sayfadaki tüm ürünleri bul
        product_bodies = soup.find_all('div', class_='product-body')
        
        # Ürün linklerini al
        for product in product_bodies:
            title_link = product.find('a', class_='title')
            if title_link:
                href = title_link.get('href')
                all_links.append(href)
    
    return all_links


def get_product_data(link):
    """
    Verilen linkteki ürün verilerini çeker.
    """
    driver.get(f'https://www.itopya.com{link}')
    time.sleep(3)  # Sayfanın yüklenmesi için bekle

    # Sayfanın kaynak kodunu al
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # "table table-product-detail" class'ına sahip tabloyu seç
    table = soup.find('table', {'class': 'table table-product-detail'})
    
    product_data = {}

    # Eğer tablo varsa, içeriği al
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # İlk satır başlık olduğu için atlıyoruz
            columns = row.find_all('td')
            if len(columns) > 1:
                key = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                product_data[key] = value
    
    return product_data


def save_to_json(data, filename='all_product_data.json'):
    """
    Verilen veriyi JSON formatında dosyaya kaydeder.
    """
    with open(filename, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Tüm ürün verileri '{filename}' dosyasına kaydedildi.")


def main():
    """
    Ana işlev. Ürün linklerini alır, her bir ürünün verisini çeker
    ve JSON dosyasına kaydeder.
    """
    # Tüm ürün linklerini al
    print("Ürün linkleri toplanıyor...")
    all_links = get_all_links()
    
    # Tüm ürün verilerini tutacak liste
    all_products_data = []
    
    # Linkler üzerinden döngü başlat
    print("Ürün verileri toplanıyor...")
    for link in all_links:
        product_data = get_product_data(link)
        if product_data:
            all_products_data.append({
                "product_link": f'https://www.itopya.com{link}',
                "product_data": product_data
            })
            print(f"{link} için veri toplandı.")
        else:
            print(f"'{link}' sayfasında 'table table-product-detail' class'ına sahip tablo bulunamadı.")
    
    # Veriyi JSON dosyasına kaydet
    save_to_json(all_products_data)


if __name__ == "__main__":
    main()

    # WebDriver'ı kapat
    driver.quit()
