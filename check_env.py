"""
环境自检脚本 —— Day 1 开始前先跑这个

用法：
    cd C:\\Users\\35759\\mycode2
    python check_env.py

全部 ✓ 就可以开始写爬虫了。
"""

import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

checks = []


def ok(label, detail=""):
    checks.append((label, True, detail))
    print("  [✓] %-30s %s" % (label, detail))


def fail(label, detail=""):
    checks.append((label, False, detail))
    print("  [x] %-30s %s" % (label, detail))


def info(label, detail=""):
    print("  [i] %-30s %s" % (label, detail))


print("=" * 60)
print("  环境自检  Day 1")
print("=" * 60)

# 1. Python
try:
    ver = "%d.%d.%d" % sys.version_info[:3]
    ok("Python", ver)
except Exception:
    fail("Python", "读不到版本")

# 2. requests
try:
    import requests
    ok("requests", requests.__version__)
except ImportError:
    fail("requests", "没装。运行: pip install requests")

# 3. BeautifulSoup
try:
    import bs4
    ok("BeautifulSoup (bs4)", bs4.__version__)
except ImportError:
    fail("bs4", "没装。运行: pip install beautifulsoup4")

# 4. csv（标准库，肯定有）
try:
    import csv
    ok("csv (标准库)", "内置")
except Exception:
    fail("csv", "不应该失败")

# 5. Git 身份
try:
    result = subprocess.run(["git", "config", "--global", "user.name"],
                            capture_output=True, text=True, timeout=5)
    name = result.stdout.strip()
    if name:
        ok("Git user.name", name)
    else:
        fail("Git user.name", "没配。运行: git config --global user.name \"你的名字\"")
except Exception:
    fail("Git", "git 命令不可用")

# 6. playwright（Day 2 才需要）
try:
    import playwright
    ok("playwright", "已装（Day 2 用）")
except ImportError:
    info("playwright", "今天不用，Day 2 再装")

# 7. 能不能连上练习站
print()
print("--- 测试连接 books.toscrape.com ---")
try:
    import requests
    r = requests.get("https://books.toscrape.com/", timeout=10,
                     headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code == 200:
        ok("books.toscrape.com", "HTTP 200  能连")
    else:
        fail("books.toscrape.com", "HTTP %d" % r.status_code)
except Exception as e:
    fail("books.toscrape.com", "连不上：%s" % str(e)[:60])

# 汇总
print()
print("=" * 60)
fails = [c for c in checks if not c[1]]
if not fails:
    print("  全部通过！可以开始写爬虫了。")
else:
    print("  有 %d 项没通过，按上面的提示修一下：" % len(fails))
    for label, _, detail in fails:
        print("    - %s : %s" % (label, detail))
print("=" * 60)
