# -*- coding: utf-8 -*-
"""把霞鹜文楷（LXGW WenKai Regular）子集化为自托管的 woff2，分三级：

  1. fonts/wk-ui.woff2    ——「首屏字集」：不展開任何韻圖、不點任何彈窗時頁面會用到的全部字
                             （介面文字、三語詞表、音系總覽、分韻總表、註釋）。約 0.16 MB。
                             訪客的第一個字型請求只需要這一個檔案。
  2. fonts/wk-dict.woff2  ——「字典字集」：展開韻圖、打開彈窗之後才會出現的字。約 1.9 MB，
                             只有使用者真的展開某個韻時才會下載。
  3. fonts/wk-ext.woff2   ——「完整字集」：霞鹜文楷收的全部 CJK 字形，作為最後一道回退。
                             平時不會下載。

命名與分工：第 1、2 級共用同一個 font-family「LXGW WenKai」，靠互不重疊的精確
unicode-range 決定誰出場；第 3 級叫「LXGW WenKai Fallback」，排在字型棧的後面。

「精確 unicode-range」是關鍵：每個檔案宣告的 unicode-range 不是整塊 CJK 區段，而是由它
自己 cmap 裡真實存在的碼位壓縮而成。這樣瀏覽器一遇到霞鹜文楷根本沒有的字（本頁有 104 個
擴展 B 區生僻字、2 個上游字典的 PUA 佔位字、以及 ᵝᶽ 兩個 IPA 修飾字母），立刻就知道回退
字型也幫不上忙，直接交給系統字型，不會白白下載 5 MB 的完整字集。

重跑：python make_font.py
"""
import os, sys, json, glob, time, re, hashlib, urllib.request

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"D:\Wu\NetDisk Download\lxgw-wenkai-v1.522\lxgw-wenkai-v1.522\LXGWWenKai-Regular.ttf"
LIVE_DB = "https://siqyin.github.io/wugniu_zyinzozin/data/DB_suhu.json"
OUT = os.path.join(HERE, "fonts")

BASE_ARGS = [
    "--flavor=woff2", "--no-hinting", "--desubroutinize", "--layout-features=",
    "--drop-tables+=GSUB,GPOS,GDEF,BASE,JSTF,vhea,vmtx,VORG,DSIG,mort,kerx,ankr,trak,kern,opbd,prop",
    "--notdef-outline", "--recalc-bounds",
]

# 完整字集只取 CJK 及其相關區段（拉丁／音標已經全部在首屏字集裡了）
EXT_MIN_CP = 0x2E80

# 同步狀態條會出現的四種狀態：載入中／同步成功／抓到舊版／連不上。
# 實測腳本跑的時候只會看到其中一種（通常是「同步成功」），但另外幾種一出現
# 也是首屏可見的字，漏掉就會去拉 2 MB 的字典片，所以固定把它們算進首屏。
SYNC_KEYS = ("sync_loading", "sync_ok", "sync_ok_stamp", "sync_fail", "sync_stale")


# ---------------------------------------------------------------- 工具
def cmap_codepoints(path):
    f = TTFont(path, lazy=True)
    cps = set()
    for t in f["cmap"].tables:
        cps |= set(t.cmap.keys())
    f.close()
    return cps


def compact_ranges(cps):
    """把碼位集合壓縮成 CSS unicode-range 用的區間字串清單。"""
    cps = sorted(cps)
    out, i = [], 0
    while i < len(cps):
        j = i
        while j + 1 < len(cps) and cps[j + 1] == cps[j] + 1:
            j += 1
        out.append("U+%04X" % cps[i] if cps[i] == cps[j]
                   else "U+%04X-%04X" % (cps[i], cps[j]))
        i = j + 1
    return out


def walk_strings(obj, sink, skip_keys=()):
    """遞迴收集 JSON 裡所有字串的字元，可跳過指定欄位。"""
    if isinstance(obj, str):
        sink.update(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in skip_keys:
                continue
            walk_strings(v, sink, skip_keys)
    elif isinstance(obj, list):
        for v in obj:
            walk_strings(v, sink, skip_keys)


# ---------------------------------------------------------------- 字集
def _read(name):
    p = os.path.join(HERE, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def collect_online_dict():
    """抓線上字典（抓不到就用本機副本），回傳 DB 資料。

    網址帶一個時間戳，是為了繞過 GitHub Pages 的 CDN 快取：字典那邊剛 push
    上去時，CDN 還可能端出十來分鐘前的舊檔，會把本機剛同步好的新資料覆蓋掉。
    另外加了保險——若線上抓回來的比本機副本還少，就保留本機副本並出聲提醒。
    """
    local_path = os.path.join(HERE, "DB_suhu.json")
    url = "%s%st=%d" % (LIVE_DB, "&" if "?" in LIVE_DB else "?", time.time())

    def local_copy():
        return json.load(open(local_path, encoding="utf-8"))

    try:
        raw = urllib.request.urlopen(url, timeout=30).read()
        online = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print("  線上字典抓取失敗（%s），改用本機副本" % e)
        return local_copy()

    if os.path.exists(local_path):
        try:
            local = local_copy()
        except Exception:
            local = None
        if local is not None and len(online) < len(local):
            print("  線上字典比本機副本少（%d < %d），保留本機副本（線上大概是 CDN 舊版）"
                  % (len(online), len(local)))
            return local

    open(local_path, "wb").write(raw)
    print("  已由線上更新 DB_suhu.json（%d 字）" % len(online))
    return online


def sync_bar_chars():
    """同步狀態條各狀態文案裡的字（三語），去掉標籤與 {佔位符}。"""
    out = set()
    sys.path.insert(0, HERE)
    try:
        import i18n_data
        for L in (i18n_data.WU, i18n_data.EN, i18n_data.JA):
            for k in SYNC_KEYS:
                out.update(re.sub(r"<[^>]+>|\{\w+\}", " ", L.get(k, "")))
    except Exception as e:
        print("  ⚠ 無法載入 i18n_data.py：%s" % e)
    return out


def first_paint_chars():
    """首屏（預設收合、未開彈窗）真正會渲染到的字。

    權威來源是同目錄的 firstpaint.txt —— 那是用瀏覽器實測出來的：分別以
    ?lang=wu / ?lang=en / ?lang=ja 載入頁面，走訪「display 不為 none」的文字節點，
    取三語可見字的並集，再加上 ASCII、Latin-1 與幾個會動態出現的符號。
    （量測腳本見 measure_firstpaint.py，頁面大改之後重跑一次即可。）

    沒有 firstpaint.txt 時退回下面這套保守估計：只取介面文字、三語詞表、音系與韻目，
    再把展開韻圖／開彈窗才用到的欄位統統歸給第二片。
    """
    p = os.path.join(HERE, "firstpaint.txt")
    if os.path.exists(p):
        s = set(open(p, encoding="utf-8").read())
        print("  首屏字表來自 firstpaint.txt（瀏覽器實測）")
        extra = sync_bar_chars()
        if extra - s:
            print("  ＋ 同步狀態條其餘狀態的字 %d 個" % len(extra - s))
        s |= extra
        return {c for c in s if ord(c) >= 0x20 and c != "\x7f"}

    print("  ⚠ 找不到 firstpaint.txt，改用保守估計（可跑 measure_firstpaint.py 重測）")
    s = set()

    # 1) index.html 的靜態文字（去掉 <script>/<style> 再剝標籤）
    html = _read("index.html")
    body = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html)
    s.update(re.sub(r"<[^>]+>", " ", body))

    # 2) scheme.json：音系與韻目（韻目取字之讀音、呼位說明、聲母表、聲調表…）
    try:
        walk_strings(json.loads(_read("scheme.json")), s)
    except Exception:
        pass

    # 3) 三語詞表 ＋ 各韻中古來源註解
    sys.path.insert(0, HERE)
    try:
        import i18n_data
        walk_strings(i18n_data.I18N, s)
        walk_strings(i18n_data.GLOSS, s)
    except Exception as e:
        print("  ⚠ 無法載入 i18n_data.py：%s" % e)

    # 4) 分韻總表／聲調表會用到的欄位（韻母、音值、呼位、類別、數目），但不含字表本身。
    #    yuntu_data.json 的 rhymes/hu_units 是有名字的欄位，所以用白名單挑；
    #    snapshot.json 的 cells 是 [聲母, 韻母, 調, 音值, 一整串字] 的無名陣列，整份略過。
    KEEP = {"name", "core", "label_read", "cls", "hu", "desc", "finals", "ipa",
            "final", "count", "rhyme", "nSys", "nChar"}
    try:
        y = json.loads(_read("yuntu_data.json"))
        for u in y.get("hu_units", []):
            for k, v in u.items():
                if k in KEEP:
                    walk_strings(v, s)
        for r in y.get("rhymes", []):
            for k, v in r.items():
                if k in KEEP:
                    walk_strings(v, s)
    except Exception:
        pass

    # 5) ASCII：數字、拉丁、基本標點隨時可能出現
    s.update(chr(c) for c in range(0x20, 0x100))
    return {c for c in s if ord(c) >= 0x20 and c != "\x7f"}


def all_page_chars():
    """index.html 裡（含內嵌 JSON）可能出現的全部字，取超集最保險。"""
    s = set(_read("index.html"))
    return {c for c in s if ord(c) >= 0x20 and c != "\x7f"}


# ---------------------------------------------------------------- 產出
CACHE = os.path.join(HERE, "font_cache.json")


def _sig(payload):
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _src_fingerprint():
    st = os.stat(SRC)
    return "%d-%d" % (st.st_size, int(st.st_mtime))


def run_cached(key, dst, args, label, payload):
    """輸入沒變就跳過子集化（完整字集要跑將近三分鐘，能省則省）。"""
    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            cache = {}
    sig = _sig(payload + "|" + _src_fingerprint())
    if os.path.exists(dst) and cache.get(key) == sig:
        mb = os.path.getsize(dst) / 1048576
        print("  %-20s %6.2f MB    （輸入未變，跳過）  %s"
              % (os.path.basename(dst), mb, label))
        return mb
    mb = run(dst, args, label)
    cache[key] = sig
    json.dump(cache, open(CACHE, "w", encoding="utf-8"))
    return mb


def run(dst, args, label):
    t = time.time()
    subset.main([SRC, "--output-file=" + dst] + args + BASE_ARGS)
    mb = os.path.getsize(dst) / 1048576
    print("  %-20s %6.2f MB  %5.1fs  %s" % (os.path.basename(dst), mb, time.time() - t, label))
    return mb


def main():
    if not os.path.exists(SRC):
        print("找不到源字體：", SRC)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)

    print("· 收集字集")
    collect_online_dict()
    vis = first_paint_chars()
    page = all_page_chars()
    deep = page - vis
    print("  首屏字集        %5d 字" % len(vis))
    print("  全頁字集        %5d 字" % len(page))
    print("  展開後才出現    %5d 字" % len(deep))

    src_cmap = cmap_codepoints(SRC)
    print("  源字體碼位      %5d 個" % len(src_cmap))

    ui_p = os.path.join(OUT, "_ui.txt")
    dt_p = os.path.join(OUT, "_dict.txt")
    open(ui_p, "w", encoding="utf-8").write("".join(sorted(vis)))
    open(dt_p, "w", encoding="utf-8").write("".join(sorted(deep)))

    print("· 子集化")
    report = []

    mb = run_cached("ui", os.path.join(OUT, "wk-ui.woff2"), ["--text-file=" + ui_p],
                    "首屏字集（介面・韻目・註釋）", open(ui_p, encoding="utf-8").read())
    cui = cmap_codepoints(os.path.join(OUT, "wk-ui.woff2"))
    report.append({"file": "wk-ui.woff2", "family": "LXGW WenKai",
                   "range": compact_ranges(cui), "mb": round(mb, 2)})

    mb = run_cached("dict", os.path.join(OUT, "wk-dict.woff2"), ["--text-file=" + dt_p],
                    "字典字集（展開韻圖後才需要）", open(dt_p, encoding="utf-8").read())
    cdt = cmap_codepoints(os.path.join(OUT, "wk-dict.woff2"))
    report.append({"file": "wk-dict.woff2", "family": "LXGW WenKai",
                   "range": compact_ranges(cdt), "mb": round(mb, 2)})

    # 完整字集：源字體在 CJK 區段裡的全部字形。
    # 刻意「不」扣掉前兩片已有的字 —— 這樣它的輸入只跟源字體有關，
    # 改介面文字時不需要重跑這一步（這一步要跑將近三分鐘）。
    # 檔內多收的字不會造成浪費：字型棧裡 wk-ui／wk-dict 排在前面，同一碼位由它們先接。
    ext_cps = sorted(c for c in src_cmap if c >= EXT_MIN_CP)
    ext_arg = ",".join("U+%04X" % c for c in ext_cps)
    mb = run_cached("ext", os.path.join(OUT, "wk-ext.woff2"),
                    ["--unicodes=" + ext_arg],
                    "完整字集（最後回退，平時不下載）", ext_arg)
    cext = cmap_codepoints(os.path.join(OUT, "wk-ext.woff2"))
    report.append({"file": "wk-ext.woff2", "family": "LXGW WenKai Fallback",
                   "range": compact_ranges(cext), "mb": round(mb, 2)})

    for p in (ui_p, dt_p):
        os.remove(p)

    json.dump(report, open(os.path.join(HERE, "font_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- 覆蓋率自檢：每個 woff2 檔只包含它自己宣告的碼位 ----
    print("· 覆蓋率自檢")
    page_in_src = {c for c in page if ord(c) in src_cmap}
    covered = cui | cdt
    missing_core = sorted(c for c in page_in_src if ord(c) not in covered)
    print("  頁面上源字體有的字  %5d，前三片未覆蓋 %d" % (len(page_in_src), len(missing_core)))
    if missing_core:
        print("    !! 未覆蓋：", "".join(missing_core[:40]))
    gone = sorted(c for c in page if ord(c) not in src_cmap)
    print("  源字體就沒有的字    %5d（%s%s）" % (len(gone), "".join(gone[:24]),
                                          "…" if len(gone) > 24 else ""))
    print("  完成，報告寫入 font_report.json；總計 %.2f MB"
          % sum(r["mb"] for r in report))


if __name__ == "__main__":
    main()
