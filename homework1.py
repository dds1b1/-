"""
作业 1：抓 1 页人才数据，存成 CSV

【用法】
    1. 先双击 `启动调试浏览器.bat`，登录 Upwork，打开人才搜索页，窗口保持开着
    2. 运行本脚本：
           python upwork_crawler/爬虫作业1_填空版.py
       或者双击项目根目录的 `做作业1.bat`

【你要做的】
    只有 3 个 TODO。管道部分（连浏览器、找令牌、发请求）我已经写好了，不用改。

    建议节奏：
        改一个 TODO → Ctrl+S 保存 → 跑一次 → 看输出对了没 → 再改下一个

【卡住了怎么问】
    按这个格式发我：
        我改的是：TODO ?
        我写的代码：（贴代码）
        报错/现象：（贴报错）
        我以为是：（你的猜测）
"""

import csv
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BODY_FILE = os.path.join(HERE, "graphql_body_样本.json")
API = "https://www.upwork.com/api/graphql/v1?alias=userFreelancerSearchV2"
CSV_FILE = os.path.join(HERE, "profiles.csv")
TOKEN_RE = re.compile(r"oauth2v2_int_[0-9a-f]{32}")

KEYWORD = "video editor"
ROWS = 50        # 服务端上限就是 50，别改大（改了会返回 0 条，这是坑）
PAGES = 2        # 今天只抓前 2 页，够你练手了

QUERY = json.load(open(BODY_FILE, encoding="utf-8"))["query"]

# CSV 的表头：列名要和 TODO 1 里返回的字典的 key 完全一致
FIELDS = ["person_id", "name", "country", "city", "region",
          "hourly_rate", "job_success", "total_hours",
          "total_earned", "jobs_completed", "description",
          "skills"]

# ==================================================================
#  管道部分（已经写好了，不用改）
# ==================================================================

JS_FETCH = """
async ({url, body, auth, tenant}) => {
  const r = await fetch(url, {method: 'POST',
    headers: {'content-type': 'application/json', 'accept': '*/*', 'authorization': auth,
              'x-upwork-api-tenantid': tenant, 'x-upwork-accept-language': 'en-US'},
    body: JSON.stringify(body), credentials: 'include'});
  return {status: r.status, text: await r.text()};
}
"""


def make_body(start, rows=ROWS):
    return {"query": QUERY, "variables": {"request": {
        "individualEarningsSearch": True, "paging": {"start": start, "rows": rows},
        "facets": ["hourly_rate"], "addGoodSummaries10Rids": True,
        "userQuery": KEYWORD, "clientAccount": False, "addGuidedSpecialties": True}}}


def find_token(page, ctx, tenant):
    """从浏览器 cookie 里找一个能用的令牌（会自动重试）"""
    cands = []
    for c in ctx.cookies():
        for m in TOKEN_RE.findall(c.get("value") or ""):
            if m not in cands:
                cands.append(m)
    for t in cands:
        auth = "bearer " + t
        for attempt in (1, 2):          # 网络抖动时重试一次
            try:
                res = page.evaluate(JS_FETCH, {"url": API, "body": make_body(0, 10),
                                               "auth": auth, "tenant": tenant})
                data = json.loads(res["text"])
                if get_profiles(data):
                    print("  找到可用令牌：...%s" % t[-8:])
                    return auth
            except Exception:
                time.sleep(1)
    return None


def get_profiles(data):
    """从接口返回的 JSON 里，把人才列表挖出来"""
    node = (((data.get("data") or {}).get("search") or {}).get("universalSearchNuxt") or {}).get("userFreelancerSearchV2") or {}
    return node.get("profiles") or []


def fetch_page(page, auth, tenant, start):
    """抓一页，返回 (人才列表, 分页信息)"""
    res = page.evaluate(JS_FETCH, {"url": API, "body": make_body(start),
                                   "auth": auth, "tenant": tenant})
    data = json.loads(res["text"])
    if data.get("errors"):
        print("  接口报错：%s" % json.dumps(data["errors"], ensure_ascii=False)[:150])
        return [], {}
    node = (((data.get("data") or {}).get("search") or {}).get("universalSearchNuxt") or {}).get("userFreelancerSearchV2") or {}
    return node.get("profiles") or [], node.get("pagingInfo") or {}


# ==================================================================
#  ★ TODO 1：从一条原始数据里挑出想要的字段
# ==================================================================
def extract(p):
    """
    输入：p = 一条人才数据（就是一个大字典）
    输出：一个字典，key 必须是 FIELDS 里那些列名

    字段路径请查 `upwork_crawler/字段映射与任务清单.md` 那张表，
    例如：
        p["personId"]                                    → person_id
        p["profile"]["personalData"]["firstName"]        → name 的一部分
        p["profile"]["personalData"]["chargeRate"]["rawValue"]  → hourly_rate

    提示：
      - 有些字段可能不存在（是 None），用 .get() 会更安全，比如
            pd.get("title")
      - 技能是个列表，每个元素长这样：{"ontologySkill": {"preferredLabel": "Video Editing"}}
        想一想：怎么把 17 个技能拼成一个字符串？
      - 最难写的就是这个函数，慢慢来

    验证：
      先不要写完整，先写两行试试——
            pd = p["profile"]["personalData"]
            print(p["personId"], pd["firstName"], pd["chargeRate"]["rawValue"])
      跑一下看能不能打印出东西，能就说明路径找对了
    """
    profile = p.get("profile") or {}
    pdata = profile.get("personalData") or {}
    location = pdata.get("location") or {}
    charge_rate = pdata.get("chargeRate") or {}
    aggregates = profile.get("profileAggregates") or {}
    skill = profile.get("skills") or []
    skills = ""
    for s in skill:
        if s.get("ontologySkill"):
            skills += s["ontologySkill"]["preferredLabel"] + ", "
        else:
            continue
    return {
        "person_id": p.get("personId"),
        "name": (pdata.get("firstName") or "") + " " + (pdata.get("lastName") or ""),
        'country': location.get("country"),
        'city': location.get("city"),
        'region': location.get("region"),
        'hourly_rate': charge_rate.get("rawValue"),
        'job_success': aggregates.get("nSS100BwScore"),
        'total_hours': aggregates.get("totalHours"),
        'total_earned': p.get("individualTotalEarnings"),
        "jobs_completed":   p.get("totalCompletedJobs"),
        "description":      pdata.get("description"),
        "skills":           skills.rstrip(", ")
    }
    
    # ← 把这里替换成你的代码


# ==================================================================
#  ★ TODO 2：把一批数据追加写进 CSV
# ==================================================================
def save(rows, path=CSV_FILE):
    """
    输入：rows = 一个列表，里面每个元素都是 TODO 1 返回的字典
    要做的：把这批数据**追加**写入 CSV 文件

    提示（照抄急救包第 5 条）：
        import csv
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()      # 只在文件不存在时写表头
            w.writerow(每一条)

    要想清楚的三件事：
      1. 什么时候写表头？（提示：文件不存在时写，存在时不写）
         判断文件在不在：`if not os.path.exists(path):`
      2. 为什么要用 "a" 而不是 "w"？
         （提示：想想中途崩溃会怎样）
      3. 第一个参数的 rows 是个列表，怎么写进去？（提示：for 循环）

    验证：跑完后打开 profiles.csv，应该能看到表头 + 50 行数据
    """
    pass               # ← 把这里替换成你的代码


# ==================================================================
#  主流程（不用改，但你最好读懂它在干什么）
# ==================================================================
def main():
    print("=" * 66)
    print("作业 1：抓 %d 页，共约 %d 条" % (PAGES, PAGES * ROWS))
    print("=" * 66)

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        except Exception as e:
            print("!! 连不上浏览器：%s" % str(e)[:120])
            print("!! 请先双击 `启动调试浏览器.bat`，登录 Upwork 并打开人才搜索页。")
            return

        ctx = browser.contexts[0]
        pages = [pg for pg in ctx.pages if "upwork.com" in (pg.url or "") and "talent" in (pg.url or "")]
        if not pages:
            print("!! 浏览器里没找到人才搜索页，请先打开它。")
            return
        page = pages[-1]
        print("已接上页面：%s" % page.url[:90])

        tenant = next((c["value"] for c in ctx.cookies() if c["name"] == "current_organization_uid"), None)
        auth = find_token(page, ctx, tenant)
        if not auth:
            print("!! 没找到可用令牌。检查一下：浏览器里是否已登录 Upwork？")
            return

        for i in range(PAGES):
            start = i * ROWS          # 第 0 页 start=0，第 1 页 start=50
            print("\n--- 抓第 %d 页（start=%d）---" % (i + 1, start))
            profiles, pinfo = fetch_page(page, auth, tenant, start)
            print("  拿到 %d 条 | 总人数 total=%s" % (len(profiles), pinfo.get("total")))
            if not profiles:
                print("  0 条！可能是 rows 超上限 / 令牌失效 / 已经抓到底了")
                break

            # 先看一眼原始数据长什么样（帮你写 TODO 1 用）
            if i == 0:
                print("\n  【原始数据速查】第一条的顶层字段：")
                print("   ", list(profiles[0].keys()))
                print("    profile 下面有哪些分组：")
                print("   ", list((profiles[0].get("profile") or {}).keys()))
                print("    personalData 下面有哪些字段：")
                print("   ", list(((profiles[0].get("profile") or {}).get("personalData") or {}).keys()))
                print()

            rows = []
            for p in profiles:
                got = extract(p)
                if got:
                    rows.append(got)
            print("  extract() 转换出 %d 条，示例：%s" % (len(rows), rows[0] if rows else "（空——TODO 1 还没写吧？）"))

            if rows:
                save(rows)
                print("  已写入 %s" % CSV_FILE)
            time.sleep(3)             # 限速：每次请求间隔 3 秒

        print("\n" + "=" * 66)
        print("跑完了。检查一下 %s 里有多少行数据。" % CSV_FILE)
        print("=" * 66)


if __name__ == "__main__":
    main()
