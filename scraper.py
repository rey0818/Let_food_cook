import requests
from bs4 import BeautifulSoup
import re
def search(keyword,limit=10,timeout=10):
    try:
        url = "https://online.carrefour.com.tw/zh/search"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, params={'q':keyword},timeout=timeout)
        response.raise_for_status()
        pattern = r'[\d,]+'
        soup = BeautifulSoup(response.content, 'html.parser')
        productdiv = soup.find_all('div', class_='hot-recommend-item')
        if not productdiv:
            print(f"未找到{keyword}的搜尋結果。")
            return []
        products = []
        for item_div in productdiv[:limit]:
            try:
                commodity_div = item_div.find('div', class_='commodity-desc')
                name = commodity_div.find('a').get_text(strip=True) if commodity_div else ""
                links = item_div.find('a')
                link = links.get('href', '') if links else ""
                if link and not link.startswith('http'):
                    link = f"https://online.carrefour.com.tw{link}"
                cur_div = item_div.find('div', class_='current-price')
                ori_div = item_div.find('div', class_='original-price')
                discount = bool(cur_div and ori_div)
                ori_price = ori_div.get_text(strip=True).replace(',','') if ori_div else 0
                match = re.search(pattern, ori_price)
                if match:
                    try:
                        original = int(match.group())
                    except ValueError:
                        print("無法分析原價,設其為0,可能網站有變動")
                        original = 0
                else:
                    original = 0
                cur_price = cur_div.get_text(strip=True).replace(',','') if cur_div else 0
                price_match = re.search(pattern, cur_price)
                if price_match:
                    try:
                        cur_price = int(price_match.group())
                    except ValueError:
                        print("無法分析價格,設其為0,可能網站有變動")
                        cur_price = 0
                else:
                    cur_price = 0
                if name and cur_price > 0:
                    info = {
                        "title": name,
                        "price": cur_price,
                        "link": link
                    }
                    if discount and original > cur_price:
                        info["is_on_sale"] = True
                        info["original_price"] = original
                        info["discount"] = original - cur_price
                    else:
                        info["is_on_sale"] = False
                    products.append(info)
            except Exception as e:
                print(f"錯誤: 無法分析食材:{e}")
                continue
        if not products:
            print(f"{keyword}沒有有效的食材資料。")
        return products
    except requests.exceptions.RequestException as x:
        print(f"網路錯誤:{x}")
        return []
    except Exception as x:
        print(f"發生未預期的錯誤 : {x}")
        return []