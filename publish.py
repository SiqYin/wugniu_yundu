# -*- coding: utf-8 -*-
"""把本目錄發布到 GitHub：建倉庫 → 提交 → 推送 → 開 GitHub Pages。

用法（令牌只從環境變數讀，不寫進檔案、不落盤）：

    set GITHUB_TOKEN=ghp_xxx            # Windows cmd
    $env:GITHUB_TOKEN="ghp_xxx"         # PowerShell
    export GITHUB_TOKEN=ghp_xxx         # bash
    python publish.py                   # 預設 SiqYin/wugniu_yundu
    python publish.py --name wugniu_yundu --public

需要的令牌權限：
  classic token      → 勾 repo、workflow
  fine-grained token → Administration: Read and write
                       Contents: Read and write
                       Pages: Read and write
                       （Repository access 選 SiqYin 名下）

推送走既有的 SSH 金鑰（git@github.com），不需要把令牌寫進 remote。
用完請到 https://github.com/settings/tokens 撤銷該令牌。
"""
import argparse, json, os, subprocess, sys, time, urllib.request, urllib.error

API = "https://api.github.com"
HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = "main"
DESC = "吳語蘇滬混合腔現代韻圖：按今音韻基分韻，開合齊撮逐位列出，一位一圖"


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not t:
        print("找不到 GITHUB_TOKEN 環境變數。請先設定後再跑。")
        sys.exit(1)
    return t.strip()


def api(path, tok, method="GET", body=None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "wugniu-yundu-publish")
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=data, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), cwd=HERE, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("git %s 失敗：\n%s%s" % (" ".join(args), r.stdout, r.stderr))
        sys.exit(1)
    return (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default="SiqYin")
    ap.add_argument("--name", default="wugniu_yundu")
    ap.add_argument("--public", action="store_true", default=True)
    ap.add_argument("--private", dest="public", action="store_false")
    ap.add_argument("--no-api", action="store_true",
                    help="倉庫已由使用者手動建好，不呼叫 GitHub API："
                         "只做 git 推送，Pages 交給 .github/workflows/pages.yml 自動開啟")
    a = ap.parse_args()

    repo = "%s/%s" % (a.owner, a.name)
    # 權杖可有可無：--no-api 時只用來當 HTTPS 推送的回退；沒給也能純 SSH 推送。
    tok = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip() or None
    if not a.no_api and not tok:
        print("找不到 GITHUB_TOKEN 環境變數（要建倉庫／開 Pages 必須提供）。")
        sys.exit(1)

    # 1) 建倉庫（已存在就沿用）
    if a.no_api:
        print("· --no-api：跳過建倉庫，假設 %s 已由使用者建好" % repo)
    else:
        status, res = api("/user/repos", tok, "POST", {
            "name": a.name,
            "description": DESC,
            "homepage": "https://%s.github.io/%s/" % (a.owner.lower(), a.name),
            "private": not a.public,
            "has_issues": True, "has_wiki": False, "has_projects": False,
            "auto_init": False,
        })
        if status == 201:
            print("· 已建立倉庫 %s" % repo)
        elif status == 422:
            print("· 倉庫 %s 已存在，沿用" % repo)
        else:
            print("建倉庫失敗（HTTP %s）：%s" % (status, res))
            sys.exit(1)

    # 2) 提交並推送
    if not os.path.isdir(os.path.join(HERE, ".git")):
        git("init", "-b", BRANCH)
    git("config", "user.name", a.owner)
    git("config", "user.email", "%s@users.noreply.github.com" % a.owner)
    git("add", "-A")
    if git("status", "--porcelain"):
        git("commit", "-m", "蘇滬混合腔韻圖：分韻方案、韻圖頁面、三語介面與霞鶩文楷字型")
        print("· 已提交")
    else:
        print("· 沒有新變更")

    ssh_url = "git@github.com:%s.git" % repo
    remotes = git("remote").split()
    if "origin" in remotes:
        git("remote", "set-url", "origin", ssh_url)
    else:
        git("remote", "add", "origin", ssh_url)

    # 先試 SSH；失敗（例如 sandbox 不讓讀 ~/.ssh/known_hosts）就用權杖走 HTTPS。
    # 注意：權杖只出現在這一條指令裡，不會寫進 .git/config —— remote 仍是 ssh_url。
    r = subprocess.run(["git", "push", "-u", "origin", BRANCH],
                       cwd=HERE, capture_output=True, text=True)
    if r.returncode == 0:
        print("· 已推送（SSH）到 %s" % ssh_url)
    else:
        if not tok:
            print("SSH 推送失敗，且沒有可用權杖可回退：\n%s%s" % (r.stdout, r.stderr))
            sys.exit(1)
        print("· SSH 推送不可用，改走 HTTPS 權杖通道……")
        https_url = "https://x-access-token:%s@github.com/%s.git" % (tok, repo)
        r2 = subprocess.run(
            ["git", "-c", "credential.helper=", "push", https_url,
             "%s:%s" % (BRANCH, BRANCH)],
            cwd=HERE, capture_output=True, text=True)
        if r2.returncode != 0:
            print("HTTPS 推送也失敗：\n%s%s"
                  % (r2.stdout.replace(tok, "<TOKEN>"),
                     r2.stderr.replace(tok, "<TOKEN>")))
            sys.exit(1)
        print("· 已推送（HTTPS）到 %s" % repo)
        # 讓本地 main 追蹤乾淨的 SSH remote
        git("branch", "--set-upstream-to=origin/%s" % BRANCH, check=False)

    # 3) 開 GitHub Pages
    if a.no_api:
        print("· --no-api：Pages 交由 .github/workflows/pages.yml 自動開啟")
        url = "https://%s.github.io/%s/" % (a.owner.lower(), a.name)
        print("\n完成。線上網址：%s" % url)
        print("倉庫地址：https://github.com/%s" % repo)
        print("部署進度：https://github.com/%s/actions" % repo)
        return

    status, res = api("/repos/%s/pages" % repo, tok)
    if status == 200 and res:
        print("· Pages 已經開著：%s" % res.get("html_url"))
    else:
        status, res = api("/repos/%s/pages" % repo, tok, "POST", {
            "source": {"branch": BRANCH, "path": "/"},
        })
        if status in (201, 409):
            print("· 已啟用 GitHub Pages")
        else:
            print("開 Pages 失敗（HTTP %s）：%s" % (status, res))
            print("  可手動到 https://github.com/%s/settings/pages 選 %s 分支根目錄"
                  % (repo, BRANCH))

    # 4) 等部署完成
    url = "https://%s.github.io/%s/" % (a.owner.lower(), a.name)
    print("· 等待 Pages 首次部署（最多 5 分鐘）……")
    for i in range(60):
        time.sleep(5)
        st, r = api("/repos/%s/pages/builds/latest" % repo, tok)
        if st == 200 and r:
            if r.get("status") == "built":
                print("· 部署完成")
                break
            if r.get("status") == "errored":
                print("· 部署出錯：%s" % r.get("error", {}).get("message"))
                break
        else:
            # 沒有 builds 端點權限時，直接用 HTTP 探測
            try:
                with urllib.request.urlopen(url, timeout=10) as resp:
                    if resp.status == 200:
                        print("· 網站已經可以訪問")
                        break
            except Exception:
                pass
    print("\n完成。線上網址：%s" % url)
    print("倉庫地址：https://github.com/%s" % repo)


if __name__ == "__main__":
    main()
