# Day 1 教材：环境检查 + 第一个爬虫

> 日期：2026-10-01 晚
> 目标：① 确认环境齐全 ② 在 books.toscrape.com 上写出你的第一个爬虫
> 预计用时：1.5 ~ 2 小时

---

## 上篇：环境检查（约 20 分钟）

### 为什么要先检查环境

写代码最怕的不是逻辑错，是"环境少了一块"——你代码写得全对，
但 `import requests` 报 `ModuleNotFoundError`，白白折腾一小时。
所以先花 20 分钟把地基打好。

### 怎么检查

**方法一（推荐）**：双击 `check_env.py` 同目录的运行方式——
在终端里跑：

```
cd C:\Users\35759\mycode2
python check_env.py
```

脚本会自动检查并打印 ✓ / ✗。

**方法二**：手动逐条敲（帮你理解每条在检查什么）：

```bash
python --version                    # 应该显示 Python 3.14.x
python -c "import requests"          # 不报错 = ✓
python -c "import bs4"               # 不报错 = ✓
git config --global user.name        # 应该显示 dds1b1
```

### 检查清单

| 项 | 怎么查 | 期望结果 | 你的状态 |
|---|---|---|---|
| Python | `python --version` | 3.14.x | ✓ 已确认 |
| requests | `python -c "import requests"` | 不报错 | ✓ 已装好 |
| BeautifulSoup | `python -c "import bs4"` | 不报错 | ✓ 已装好 |
| Git 身份 | `git config --global user.name` | dds1b1 | ✓ 已确认 |
| playwright | `python -c "import playwright"` | 不报错 | ⏳ Day 2 再装，今天不用 |
| 代理（v2rayN） | 看 v2rayN 是否开着 | 端口 10808 在听 | 你自己确认 |

> playwright 今天不用——Day 1 的练习站（books.toscrape）不需要真浏览器，
> 用 requests 就够了。playwright 留到 Day 2 用 Upwork 时再装。

---

## 下篇：写出你的第一个爬虫（约 1 小时）

### 靶场：books.toscrape.com

这是一个**专门给人练习爬虫**的网站：

- 不设防（没有 Cloudflare、没有验证码）
- 结构经典（商品列表 + 分页 + 详情页）
- 数据公开（书名、价格、评分、库存）

**网址**：https://books.toscrape.com/

### 三段式理解爬虫

爬虫的本质就三步，记住这个框架后面什么都能套：

```
吃什么：一个网址
   ↓
怎么处理：requests.get(网址) → 拿到 HTML 文本 → BeautifulSoup 挑数据
   ↓
吐什么：你要的数据（书名、价格……）
```

### 你要弄懂的几个概念

**1. 状态码**

服务器收到你的请求后，会回一个数字告诉你"怎么样了"：

| 码 | 含义 | 你该怎么想 |
|---|---|---|
| **200** | 成功 | 数据到手了 |
| 403 | 被拒绝 | 服务器不让你看（Cloudflare 之类） |
| 404 | 没找到 | 网址写错了 |
| 500 | 服务器出错了 | 不是你的问题 |

> books.toscrape 会给你 200。Upwork 会给你 403——这就是 Day 2 要换工具的原因。

**2. HTML 是什么**

网页的"源代码"，用尖括号标签写成的一棵树：

```html
<article class="product_pod">        ← 一本书的容器
    <h3>
        <a href="..." title="书名">书名</a>   ← 书名在 a 标签的 title 属性里
    </h3>
    <p class="price_color">£51.77</p>        ← 价格在 p 标签的文本里
</article>
```

> 爬虫的核心技能：**在这棵树里找到你要的标签**。
> 怎么找？右键网页 → 检查（F12）→ Elements 面板里看结构。

**3. BeautifulSoup（bs4）是什么**

一个帮你从 HTML 里挑数据的库。你不用手写正则、不用手找尖括号，
告诉它"我要所有 `class="product_pod"` 的 `article` 标签"，它帮你找出来。

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html文本, "html.parser")
books = soup.find_all("article", class_="product_pod")  # 找出所有书的容器
```

### 动手任务

打开同目录的 `day1_books.py`，里面有 **3 个 TODO** 要你填。

**管道部分**（发请求、建 soup）我已经写好了，你只需要填解析部分。

| TODO | 要做什么 | 提示 |
|---|---|---|
| TODO 1 | 找出页面上所有书 | `soup.find_all("article", class_="product_pod")` |
| TODO 2 | 从一本书里取出书名和价格 | 书名在 `h3 > a` 的 `title` 属性里；价格在 `p.price_color` 的文本里 |
| TODO 3 | 打印结果 | `print(f"{书名} - {价格}")` |

**做完后的验收标准**：

- [ ] 屏幕上打印出 **20 本书**的名字和价格（books.toscrape 首页正好 20 本）
- [ ] 你能回答：为什么是 20 本？（提示：看网页结构）
- [ ] 你能回答：如果要抓第 2 页，网址要怎么改？（提示：看分页链接）

**加分题**（做完基础题再试）：

- [ ] 把 20 本书存成一个 CSV 文件（用 `csv.DictWriter`，参考路线里的急救包第 5 条）
- [ ] 抓前 5 页（共 100 本），存 CSV

### 卡住了怎么问我

按这个格式发我：

```
我改的是：TODO ?
我写的代码：（贴代码）
报错/现象：（贴报错）
我以为是：（你的猜测）
```

### 最重要的：改一处跑一次

**不要一次写完 3 个 TODO 再跑**。每填一个就存盘、跑一次、看输出。
- 填完 TODO 1 → 跑 → 看看是不是打印了 20 个 `<article>` 对象
- 填完 TODO 2 → 跑 → 看看是不是打印了 20 个书名
- 填完 TODO 3 → 跑 → 看看格式对不对

这是爬虫工程师的日常节奏，也是你以后独立工作时最重要的习惯。

---

## 今天结束时要完成的事

- [ ] `check_env.py` 跑通，环境全 ✓（playwright 除外）
- [ ] `day1_books.py` 3 个 TODO 全填完，打印出 20 本书
- [ ] git commit 一次："Day 1: 爬虫练手 books.toscrape 完成"
- [ ] 在 `C:\Users\35759\WorkBuddy\2026-09-23-15-43-40\upwork_crawler\踩坑记录.md`
      里写一条今天的踩坑（哪怕只是"第一次跑就报错，后来发现是少装了 bs4"）
