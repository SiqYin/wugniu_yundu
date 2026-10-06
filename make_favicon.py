# -*- coding: utf-8 -*-
"""把字音查詢網站的圖示搬到本頁。

字音查詢網站的 favicon 是**內嵌在 HTML 裡的 base64 ICO**（256×256），沒有獨立檔案可抓，
所以這裡照樣從它的首頁把那段 base64 解出來，再切成：

    favicon.ico             16／32／48／64 四種尺寸（瀏覽器分頁圖示）
    apple-touch-icon.png    180×180（iOS 加到主畫面用）

執行（需要 Pillow）：

    <venv python> make_favicon.py

之後重跑 `python generate_html.py` 讓 <link rel="icon"> 生效。
"""
import base64, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "https://siqyin.github.io/wugniu_zyinzozin/"
UA = "Mozilla/5.0 (compatible; wugniu_yundu icon sync)"
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64)]
TOUCH = 180


def main():
    req = urllib.request.Request(SRC, headers={"User-Agent": UA})
    page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    m = re.search(r'<link[^>]+rel="icon"[^>]*base64,([A-Za-z0-9+/=]+)', page)
    if not m:
        print("!! 字音查詢網站的首頁找不到內嵌 favicon，可能改版了")
        sys.exit(1)

    tmp = os.path.join(HERE, "__icon_src.ico")
    with open(tmp, "wb") as f:
        f.write(base64.b64decode(m.group(1)))

    try:
        from PIL import Image
    except ImportError:
        print("!! 需要 Pillow，請用托管 venv 跑：")
        print("   C:/Users/29736/.workbuddy-ai/binaries/python/envs/default/Scripts/python.exe "
              "make_favicon.py")
        sys.exit(1)

    im = Image.open(tmp).convert("RGBA")
    im.save(os.path.join(HERE, "favicon.ico"), sizes=ICO_SIZES)
    im.resize((TOUCH, TOUCH), Image.LANCZOS).save(os.path.join(HERE, "apple-touch-icon.png"))
    os.remove(tmp)

    for name in ("favicon.ico", "apple-touch-icon.png"):
        print("  %-22s %6d bytes" % (name, os.path.getsize(os.path.join(HERE, name))))
    print("來源圖 %dx%d（取自 %s）" % (im.size[0], im.size[1], SRC))


if __name__ == "__main__":
    main()
