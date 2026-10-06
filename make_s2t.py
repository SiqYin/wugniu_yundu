# -*- coding: utf-8 -*-
"""從字音查詢網站抓 S2T.json，精簡成本頁「同韻查詢」用的簡繁對照表。

上游 `https://siqyin.github.io/wugniu_zyinzozin/data/S2T.json` 有 9680 條、
約 685 KB，其中大半是「自己對自己」（如 凘→[凘]）這種不必轉換的條目。
本頁只需要：

  1. 真的有變化（t != [s]）的；以及
  2. 轉換結果裡至少有一個字能在本頁字典（DB_suhu.json）查到。

其餘留著也沒用 —— 轉出來的字查不到，同韻查詢一樣是空的。
精簡後約 2500 條、35 KB，只在點開「同韻查詢」時才下載：

    python make_s2t.py

抓不到網路時會保留原有的 s2t.json，不會把檔案清空。
"""
import json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UPSTREAM = "https://siqyin.github.io/wugniu_zyinzozin/data/S2T.json"
DB = os.path.join(HERE, "DB_suhu.json")
DST = os.path.join(HERE, "s2t.json")


def fetch(url):
    req = urllib.request.Request(url + "?t=%d" % time.time(),
                                 headers={"User-Agent": "wugniu-yundu/make_s2t"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    if not os.path.exists(DB):
        print("找不到 DB_suhu.json，先跑 build_data.py。")
        sys.exit(1)

    db = json.load(open(DB, encoding="utf-8"))
    known = set()
    for rec in db:
        known.update(rec["character"])

    try:
        raw = fetch(UPSTREAM)
    except Exception as e:
        if os.path.exists(DST):
            print("抓不到上游 S2T.json（%s），保留原有的 s2t.json 不動。" % e)
            return
        raise

    if not isinstance(raw, list):
        print("上游 S2T.json 格式不如預期，中止。")
        sys.exit(1)

    table, dropped, keep_all = {}, 0, 0
    for rec in raw:
        s, t = rec.get("s"), rec.get("t")
        if not isinstance(s, str) or not isinstance(t, list) or not t:
            continue
        if t == [s]:
            continue
        keep_all += 1
        hit = [x for x in t if x in known]
        if hit:
            table[s] = hit
        else:
            dropped += 1

    # 拼音排序，輸出穩定，diff 才看得出來
    ordered = {k: table[k] for k in sorted(table)}
    data = json.dumps(ordered, ensure_ascii=False, separators=(",", ":"))
    open(DST, "w", encoding="utf-8").write(data + "\n")

    print("上游條目      %5d" % len(raw))
    print("有變化的      %5d" % keep_all)
    print("  保留        %5d（轉換結果在字典裡查得到）" % len(table))
    print("  略過        %5d（轉出來的字字典沒有，留著也是空查詢）" % dropped)
    print("寫入 s2t.json  %.1f KB" % (len(data.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
