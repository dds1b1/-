import csv, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows 防 GBK
HERE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(HERE, "profiles.csv")
TMP      = os.path.join(HERE, "profiles_新.csv")
BACKUP   = os.path.join(HERE, "profiles_备份.csv")           # 新增:备份文件的路径(跟 CSV 放同一目录)
FIELDS = ["person_id", "name", "country", "city", "region",
          "hourly_rate", "job_success", "total_hours",
          "total_earned", "jobs_completed", "description", "skills"]

if os.path.exists(CSV_FILE):                                 # 新增:先备份 —— 这是"动原文件"之前的保险
    shutil.copy2(CSV_FILE, BACKUP)                           # 新增:复制一份;copy2 会连修改时间一起复制
    print("已备份 ->", BACKUP)                                # 新增:打印出来,确认备份成功再往下走

with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
seen = set()
out = []
tmp = "profilesnew"
def clean(s):
    if not s:
        return ""
    s = s.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')                             # 改:原来第二个参数是空字符串 ''(把双空格删掉),改成 ' '(压成一个空格)
    return s.strip()
for r in rows:
    pid = r.get('person_id')
    if pid in seen:
        continue
    seen.add(pid)
    for k in ('description', 'skills','name'):
        r[k] = clean(r.get(k))
    out.append(r)

try:
    with open(TMP, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)
except Exception as e:
    print("写临时文件失败:", e)
    raise SystemExit(1)      

os.replace(TMP, CSV_FILE)
