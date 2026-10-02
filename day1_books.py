"""
Day 1 练习：爬 books.toscrape.com

你的第一个爬虫。管道部分（发请求、建 soup）已经写好了，
你只需要填 3 个 TODO。

节奏：填一个 TODO → 存盘 → 跑一次 → 看输出 → 再填下一个
"""
import json
import sys
import requests
from bs4 import BeautifulSoup
import csv
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = "https://books.toscrape.com/"

# ==================================================================
#  管道部分（已写好，不用改）
# ==================================================================

print("正在请求 %s ..." % URL)
resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
print("状态码：%d（200 = 成功）" % resp.status_code)

if resp.status_code != 200:
    print("!! 状态码不是 200，没法继续。检查网络。")
    sys.exit(1)
resp.encoding = "utf-8"
# 把 HTML 文本交给 BeautifulSoup，建一棵可搜索的"树"
soup = BeautifulSoup(resp.text, "html.parser")
books = soup.find_all('article',class_="product_pod")
print("HTML 已加载，长度 %d 字符" % len(resp.text))
print(books)
result = []
def find(bs):
    title = bs.h3.a.get("title")
    if bs.find("p", class_="price_color") is not None:
        price = bs.find("p", class_="price_color").get_text()
    else :
        price = ('notfound:price')
    return{'title':title,'price':price}
for book in books:
    inform = find(book)
    result.append(inform)
print(result)
with open('book_json',"w", encoding="utf-8-sig") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["title", "price"])
    w.writeheader()
    for book in books:
        w.writerow(find(book))

# ==================================================================
#  ★ TODO 1：找出页面上所有的"书"
# ==================================================================
# 提示：
#   每本书包在一个 <article class="product_pod"> 标签里
#   用 soup.find_all() 找出所有这样的标签
#
#   参考写法（自己抄了改）：
#       books = soup.find_all("article", class_="product_pod")
#
#   注意：class 在 Python 里是关键字，所以 BeautifulSoup 用 class_ 加下划线
#
#   填完后跑一下，应该打印出 20 本书。


 # ← 把这行改成你的代码


# ==================================================================
#  ★ TODO 2：从一本书里取出书名和价格
# ==================================================================
# 提示：
#   书名在 <h3> 里的 <a> 标签的 title 属性里：
#       book.find("h3").find("a")["title"]
#   或者：
#       book.h3.a.get("title")
#
#   价格在 <p class="price_color"> 的文本里：
#       book.find("p", class_="price_color").get_text()
#   或者：
#       book.select_one(".price_color").text
#
#   .get_text() 会取出标签里的文字（去掉尖括号那层包装）
#
#   想想：如果某本书没有价格，上面的代码会不会报错？
#   要更安全的话用 .get_text(strip=True) 或者先判断 None



# ==================================================================
#  ★ TODO 3：打印结果
# ==================================================================
# 提示：
#   用 for 循环遍历 books，每本调用 extract_book()，然后打印
#
#   参考写法：
#       for book in books:
#           info = extract_book(book)
#           print(f"{info['title']}  -  {info['price']}")
#
#   f"..." 是格式化字符串，{变量名} 会被替换成变量的值

# ↓ 在这里写你的循环（删掉 pass，换成你的代码）
pass


# ==================================================================
#  加分题（做完上面的再试）
# ==================================================================
# 把 20 本书存成 CSV：
#
#   import csv
#   with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
#       w = csv.DictWriter(f, fieldnames=["title", "price"])
#       w.writeheader()
#       for book in books:
#           w.writerow(extract_book(book))
#   print("已存到 books.csv")
#
# 想想：
#   1. 为什么用 "w" 而不是 "a"？（提示：第一次创建文件）
#   2. 为什么用 utf-8-sig？（提示：Excel 打开不乱码）
#   3. 如果要抓 5 页怎么办？（提示：看网页底部分页链接的 URL 规律）
