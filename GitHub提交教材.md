# 提交到 GitHub 教材（发网址给验收人）

> 写于 2026-10-06
> 用途：把 `mycode2` 里的作业推上 GitHub，生成网址发给验收人

---

## 一、先搞清三个概念

这三样不是一回事，验收人看的是第3 个。

| | 是什么 | 在哪 |
|---|---|---|
| **工作区/本地仓库** | 你硬盘上的文件夹 + `.git` 目录 | `C:\Users\35759\mycode2` |
| **远程仓库** | GitHub 上的一个仓库（网址） | `github.com/你的用户名/仓库名` |
| **GitHub 网址** | 远程仓库的公开地址 | 验收人点这个链接就能看 |

**一句话**：git commit 是**存在本地**，git push 才是**传到 GitHub**。

**我查过你的现状**：

```
gh 命令      没装
git remote   没配（还没连 GitHub）
你的 git 身份  dds1b1 / 3575938055@qq.com  ✅ 已配好
```

---

## 二、先确认一件事：GitHub 仓库必须是公开的

**验收人曹喆含要看你���仓库，必须是 Public（公开），不能是 Private（私有）。**

GitHub 私有仓库别人打不开（要登录 + 被加 collaborators）。**上传前一定确认仓库是 Public。**

---

## 三、方法 A：网页上传（最简单，适合第一次）

**适合**：文件不多、想快速搞定。

### 步骤 1：注册/登录 GitHub

打开 `https://github.com/signup`，用邮箱注册。

> ⚠️ **不要用 QQ 邮箱**。GitHub 国内邮箱验证经常失败，推荐用：
> - Gmail（`@gmail.com`）
> - 163 / 126 邮箱（QQ 邮箱偶发失败）
>
> 你现在 git 配的是 `3575938055@qq.com`。**建议去 GitHub 设置里加一个备用邮箱**，或者直接用别的邮箱注册 GitHub（git 提交作者和 GitHub 账号可以是两个邮箱，不影响）。

### 步骤 2：新建一个仓库

1. 登录后点右上角 **`+`** → **New repository**
2. 填：

| 字段 | 填什么 |
|---|---|
| Repository name | `upwork-crawler`（或 `crawler-homework`） |
| Description | `Upwork 人才数据爬虫 + books.toscrape 练习` |
| Public / Private | **选 Public** ← 关键 |
| Add README | **不勾**（我们本地已有仓库，勾了会冲突） |
| .gitignore | **不选**（我们本地有） |
| License | **不选** |

3. 点 **Create repository**

### 步骤 3：上传文件

在仓库页面点 **uploading an existing file** 的链接，然后：

- **把关键文件拖进浏览器**（不要拖整个文件夹，GitHub 网页版不支持）
- 或者点 **choose your files** 逐个选

**该传哪些文件**（`mycode2` 里的）：

```
✅ 必须传
   homework1.py              作业1主程序
   清洗去重.py                清洗脚本
   profiles.csv              数据成果（2179条）
   graphql_body_样本.json     作业依赖，不传跑不了
   清洗去重教材.md            ← 新写的这份
   Day1教材.md

✅ 建议传
   day1_books.py / day2 / day3.py / test    books 练习
   对照表                                    字段映射表
   books.csv / book_json

❌ 不要传
   profiles_备份.csv     3.9MB，太大
   progress.txt / data.txt     断点临时文件
   诊断500.py / 诊断令牌.py     排查用，乱
   __pycache__/                缓存
   upwork_edge_profile/        浏览器数据（含登录凭证！！）
```

> ⚠️⚠️ **绝对不能传 `upwork_edge_profile/`** —— 里面有你的 **cookie、cf_clearance、登录令牌**。传上去等于把账号交出去了。

**⚠️ 还要传一个 `.gitignore`**（新建仓库时没勾自动生成的，要手动传）：

```
progress.txt
data.txt
profiles_备份.csv
__pycache__/
upwork_edge_profile/
upwork_profile/
```

### 步骤 4：拿到网址

上传成功后，页面上方会显示仓库地址：

```
https://github.com/你的用户名/upwork-crawler
```

**这就是发给验收人的网址。**

---

## 四、方法 B：git push（更正规，推荐）

**适合**：文件多、要频繁更新。**而且这才是"用 Git 提交"的完整流程。**

### 步骤 1：在 GitHub 上先建一个空仓库

同方法 A 的步骤 2。**注意不要勾任何自动生成的文件。**

假设你的用户名是 `dds1b1`，仓库名是 `upwork-crawler`：

```
仓库地址：https://github.com/dds1b1/upwork-crawler
```

### 步骤 2：本地连上远程

```bash
cd C:\Users\35759\mycode2

# 加一个叫 origin 的远程地址（origin 是约定俗成的名字）
git remote add origin https://github.com/dds1b1/upwork-crawler.git

# 看看连上了没
git remote -v
```

**正常输出**：

```
origin  https://github.com/dds1b1/upwork-crawler.git (fetch)
origin  https://github.com/dds1b1/upwork-crawler.git (push)
```

**如果报 `remote origin already exists`**：先删再加

```bash
git remote remove origin
git remote add origin https://github.com/dds1b1/upwork-crawler.git
```

### 步骤 3：推上去

```bash
git push -u origin master
```

**第一次推送会要求登录**：

```
Username for 'https://github.com': dds1b1          ← 你的 GitHub 用户名
Password for 'https://github.com':                  ← 这里要粘 Personal Access Token
```

> ⚠️ **2021 年后 GitHub 不再用账号密码认证了**，直接输密码会报 `remote: Support for password authentication was removed`。
>
> **要先生成 Token**：`https://github.com/settings/tokens` → Generate new token (classic) →
> 勾 `repo` → 生成 → **立刻复制**（关掉就看不到了）→ 粘到 Password 位置。
>
> 认证方式是：**用户名随便填 GitHub 用户名，密码位置填 Token。**

### 步骤 4：以后更新只推增量

```bash
git add 文件名
git commit -m "说明"
git push
```

**`git push` 单独用就行**，不需要再写 `-u origin master`（`-u` 只第一次要）。

### 步骤 5：确认成功

打开 `https://github.com/你的用户名/upwork-crawler`，应该能看到：

- 你所有文件
- **右边 "N commits"** — 点进去能看到每条 commit 和改了哪些文件
- 这是验收人重点看的东西

---

## 五、方法 C：装 gh 命令（最省事，可选）

GitHub 官方命令行工具，登录一次以后 push 都不用输账号。

**装**（PowerShell 里）：

```powershell
winget install --id GitHub.cli
```

**装完重开一个终端**，然后：

```bash
gh auth login
```

按提示选：

```
? What account do you want to log into?  → GitHub.com
? What is your preferred protocol?      → HTTPS
? Authenticate Git with your credentials? → Yes
? How authenticate?                     → Login with a web browser
```

**最后一步会给个网址**，复制到浏览器打开，粘贴那个验证码回来就行。

**登录后**：

```bash
# 推送当前仓库到 GitHub（会自动建仓库）
gh repo create upwork-crawler --public --source=. --push
```

**一条命令搞定建仓库 + 上传 + 设为公开。**

---

## 六、GitHub 上传前后对照

| | 本地 | GitHub |
|---|---|---|
| 存 commit 历史 | ✅ 已经有了（11 条） | 推上去才有 |
| 能被别人看到 | ❌ 只有你能看 | ✅ Public 后谁都能看 |
| 验收人能不能验收 | ❌ 他访问不到你硬盘 | ✅ 点网址就能看 |

**所以"本地 commit 做了 100 分"但"没 push"= 验收人看到 0 分。**

---

## 七、发网址时该说什么

**别只甩一个链接**，告诉对方怎么走：

```
验收人：曹喆含（QQ 1873911236）

老师好，作业已提交，仓库地址：

    https://github.com/你的用户名/upwork-crawler

主要文件说明：
- upwork_crawler/homework1.py   作业1主程序（抓取+清洗+存CSV）
- upwork_crawler/profiles.csv   数据成果：2179 条，12 字段，零空值零重复
- upwork_crawler/踩坑记录.md    踩坑记录 #001~#019（Cloudflare 三道关 + 编码/去重等）
- 练习_day1_day4/              books.toscrape 练习稿（Day1~Day3）
- git log 可以看到 15 条提交记录，每条对应一个功能

数据量说明：题面要求 2500 条起步，实际抓到 2179 条（接口 total 显示 10000，
即该关键词下有 1 万人可选，抓了 50 页 × 50 条上限 = 2500 条位置，
其中 321 条因跨页重复被去重剔除）。

麻烦老师验收。
```

---

## 八、发之前的自查清单

**逐条打勾，别漏**：

```
□ 仓库是 Public（不是 Private）—— 私有别人打不开
□ 所有代码和数据都 push 上去了（GitHub 网页上能翻到）
□ git log 有 15 条以上，每条 message 能看懂
□ 没有 upwork_edge_profile/（含登录凭证！！！）
□ 没有 profiles_备份.csv（3.9MB）
□ 踩坑记录.md 写完了（#001~#019）
□ README.md 写了（怎么跑：先双击哪个 bat，再跑哪个脚本）
□ data.csv / profiles.csv 用 Excel 打开不乱码、不弹框
□ 敏感信息检查：整个仓库搜一遍 "bearer"、"master_access_token"、"oauth2v2"
   —— 有的话必须删掉再推
```

**第 9 条最重要**。快速查：

```bash
# 搜敏感字符串
grep -r "oauth2v2\|master_access_token\|bearer " --include="*.py" --include="*.json" --include="*.md" .
```

搜到的话，确认那是**正则表达式字符串**（如 `TOKEN_RE = re.compile(r"oauth2v2_int_...")`，安全）还是**真实令牌**（危险）。

---

## ⚠️ 我的安全提醒

你的 `upwork_edge_profile/` 里有**真实登录态**：cookie、`cf_clearance`、`master_access_token`。

**这个东西一旦推到公开 GitHub，等于把 Upwork 账号交出去。**

**你已经有 `.gitignore` 保护它了**（工作区那份），但要确认：

```bash
git ls-files | grep -E "edge_profile|upwork_profile"   # 应该什么都不输出
```

**输出为空 = 安全。** 有输出 = 立刻处理（`git rm --cached` 那个文件 + 改历史）。

---

## 九、常见问题

**Q: 提示 `Permission denied (publickey)`**
用 HTTPS 地址 + Token 认证，不要用 SSH。

**Q: 提示 `rejected ... non-fast-forward`**
远程有你没有的 commit（或反过来）。新手最简解法：

```bash
git pull origin master --allow-unrelated-histories
# 处理完冲突再
git push -u origin master
```

**Q: 推上去了但看不到文件**
检查是不是传到了 `.gitignore` 排除的目录。用网页版看：

```
https://github.com/你的用户名/仓库名/tree/main
```

**Q: 一个文件 3MB 推不动（GitHub 单文件限制 100MB，浏览器上传限制 25MB）**
`profiles.csv` 有 3.6MB，网页上传一般没问题。`profiles_备份.csv` 更大，**别传**。

**Q: 提交时间 10.8 截止，什么时候推**
**建议 10.7 当天晚上就推完**。万一出意外还有一天补救。**不要卡着 10.8 下午推。**

---

## 十、一页速查

```bash
# 一次性设置（改 GitHub 用户名和仓库名）
cd C:\Users\35759\mycode2
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin master

# 以后每次更新（3 条）
git add 改的文件
git commit -m "这次改了啥"
git push
```

**检查清单**：
1. 仓库 Public ✅
2. 没有敏感文件 ✅
3. git log 条数够、message 能看懂 ✅
4. README 有写怎么跑 ✅
5. **10.7 晚上推完，不卡 10.8** ✅
