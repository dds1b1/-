"""
Day 3 练习：抓全站 50 页 + 去重 + 断点续抓 + 错误兜底

Day1 学了：发请求、解析单页、提取字段、存文件
Day2 学了：for 循环翻页、拼 URL、累加结果
Day3 学了：抓 50 页（1000 本），外加爬虫三大reality——

    ① 去重      同一本书可能出现在多页，不去重数据会重复
    ② 断点续抓  50 页抓到第 30 页断了，不该从头再来
    ③ 错误兜底  某页失败/超时，不该整个脚本崩掉

节奏：填一个 TODO → 存盘 → 跑一次 → 看输出 → 再填下一个
"""
import json
import csv
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ==================================================================
#  配置区（已写好，不用改）
# ==================================================================

BASE = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 50          # 全站 50 页
PROGRESS_FILE = "progress.txt"      # 断点文件：记抓到第几页了
RESULT_JSON = "day3_result.json"   # 结果：json
RESULT_CSV = "day3_result.csv"     # 结果：csv
HEADERS = {"User-Agent": "Mozilla/5.0"}


# ==================================================================
#  管道部分（已写好，不用改）
# ==================================================================

def fetch_page(n):
    """
    抓第 n 页，返回这一页的书列表（列表套字典）。失败返回空列表。

    这里已经写好了「重试 3 次 + 失败不崩」，你不用改。
    """
    url = BASE.format(n)
    for attempt in range(1, 4):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.encoding = "utf-8"

            if resp.status_code != 200:
                print(f"    第{attempt}次：状态码 {resp.status_code}，重试")
                time.sleep(1)
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            out = []
            for b in soup.find_all("article", class_="product_pod"):
                price_tag = b.find("p", class_="price_color")
                out.append({
                    "title": b.h3.a.get("title", "") if b.h3 and b.h3.a else "",
                    "price": price_tag.get_text(strip=True) if price_tag else "",
                    "page": n,          # 顺手记来源页，出了问题好回头查
                })
            return out

        except Exception as e:
            print(f"    第{attempt}次失败：{type(e).__name__}，重试")
            time.sleep(2)

    print(f"    !! 第 {n} 页 3 次都失败，跳过")
    return []


# ==================================================================
#  ★ TODO 1：断点续抓 —— 上次抓到第几页了？
# ==================================================================
#  问题：50 页抓到第 30 页时电脑睡了/网络断了，重跑时要不要从第 1 页重来？
#        不用。记一个 progress.txt，下次跑从断的地方接着抓。
#
#  思路：
#    第一次运行 → progress.txt 不存在 → 从第 1 页开始
#    跑到第 30 页 → 把"30"写进 progress.txt
#    下次运行   → 读到 30 → 从第 31 页继续
#
#  提示：
#   os.path.exists(PROGRESS_FILE)  判断文件在不在
#   open(PROGRESS_FILE, "r").read().strip()  读内容
#   open(PROGRESS_FILE, "w").write(str(n))    写内容
#
#  边界：如果上次抓到第 30 页但没存结果，续抓时要从 30 还是 31？
#        想清楚再写，选错会导致第 30 页重复或丢失。

def load_progress():
    """
    返回上次抓到的页码。首次运行（文件不存在）返回 1。

    返回值 = "从第几页开始抓"
    """
    # ↓ 在这里写你的代码
    pass


# ==================================================================
#  ★ TODO 2：去重 —— 同一本书只能留一条
# ==================================================================
#  问题：翻页时某本书可能在第 5 页和第 20 页各出现一次。
#        不去重，CSV 里就有重复行，验收时会被看出来。
#
#  思路：用一个集合(set)记住见过的书名。
#       set 的特性：加进去两次还是一条，天生适合去重。
#
#  提示：
#    seen = set()                # 空集合
#    if title not in seen:       # 没见过
#        seen.add(title)         # 记下来
#        保留这条数据
#    else:                       # 见过，跳过
#        continue
#
#  想想：
#    1. 为什么不直接用 list + if title not in list？
#       （提示：list 查找是逐个比，集合是哈希直查。1000 条以内差别不大，
#         10 万条以上差 100 倍。爬虫数据量大会用到。）
#    2. 如果两本书同名但价格不同，算重复吗？（提示：Upwork 上真有这种情况）

def dedup(books):
    """
    输入：书列表（列表套字典）
    输出：去重后的书列表

    每条数据里有 'title' 和 'page' 两个字段可用
    """
    # ↓ 在这里写你的代码
    pass


# ==================================================================
#  ★ TODO 3：主流程 —— 把上面三块串起来
# ==================================================================
#  要做的事，按顺序：
#
#   1. start = load_progress()          从第几页开始
#   2. all_books = []                    存所有书
#   3. for n in range(start, TOTAL_PAGES + 1):   循环每一页
#         books = fetch_page(n)         抓这一页（管道已写好）
#         all_books.extend(books)       累加进大列表
#         存进度：把 n 写进 progress.txt
#         print(f"第{n}页: 本页{len(books)}本，累计{len(all_books)}本")
#         time.sleep(1)                 别抓太快
#   4. final = dedup(all_books)         去重
#   5. 存 json 和 csv
#   6. print 汇总
#
#  提示：
#    list.extend(列表)   把另一个列表的所有元素加进来（对比 append 只加一个）
#    json.dump(数据, f, ensure_ascii=False, indent=2)
#    csv.DictWriter 用法跟 Day 2 一样

# ↓ 在这里写你的代码
pass


# ==================================================================
#  验收标准（跑完对照一下）
# ==================================================================
#  □ 50 页全部抓到，原始数据 1000 本左右
#  □ 去重后条数 <= 原始条数（说明去重起了作用）
#  □ progress.txt 里记着最后抓的页码
#  □ 手动测试断点：跑到一半 Ctrl+C 停掉，再重跑，看它是不是从断的地方继续
#  □ 三个 TODO 分别单独 commit（细粒度 commit）
#
#  想加分：
#  □ 把去重前后的条数都 print 出来，让人看见去掉了多少
#  □ 抓的时候实时存盘（每页存一次），而不是最后一次性存
#    —— 这样就算第 50 页崩了，前面 49 页的数据也在
#