# -*- coding: utf-8 -*-
"""實測「首屏可見字」，產出 firstpaint.txt 供 make_font.py 使用。

原理：把一個探針腳本注入 index.html 的副本，用無頭 Chrome 以 ?lang=wu / en / ja 載入，
走訪整棵 DOM 但跳過 display:none / visibility:hidden 的子樹（收合的韻圖、沒開的彈窗都算
不可見），把三種語言看得到的文字取並集，再加 ASCII、Latin-1 與幾個會動態出現的符號。

改過版面或介面文字之後，重跑一次本腳本即可：
    python measure_firstpaint.py

需要：本機有 Chrome，且能以 http 方式訪問本目錄（腳本會自己起一個臨時服務器）。
"""
import io, os, re, sys, html, shutil, subprocess, threading, http.server, socketserver, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
]

PROBE = u"""
<script>
setTimeout(function(){
  function txt(el){
    var s='';
    (function w(n){
      if(n.nodeType===3){ s+=n.nodeValue; return; }
      if(n.nodeType===1){
        if(n.tagName==='SCRIPT'||n.tagName==='STYLE') return;
        var cs=getComputedStyle(n);
        if(cs.display==='none'||cs.visibility==='hidden') return;
        for(var i=0;i<n.childNodes.length;i++) w(n.childNodes[i]);
      }
    })(el);
    return s;
  }
  var p=document.createElement('pre'); p.id='FP';
  p.textContent='[VIS]'+txt(document.body)+'[/VIS]';
  document.documentElement.appendChild(p);
},1500);
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    print("找不到 Chrome，請自行設定 CHROME_CANDIDATES")
    sys.exit(1)


def serve(directory):
    """起一個只綁 127.0.0.1 的臨時靜態伺服器，回傳 (port, shutdown_fn)。"""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=directory, **k)

        def log_message(self, *a):
            pass

    srv = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1], srv.shutdown


def main():
    src = os.path.join(HERE, "index.html")
    if not os.path.exists(src):
        print("找不到 index.html，請先跑 build_data.py ＋ generate_html.py")
        sys.exit(1)

    probe_name = "__fp_probe.html"
    probe_path = os.path.join(HERE, probe_name)
    io.open(probe_path, "w", encoding="utf-8").write(
        io.open(src, encoding="utf-8").read().replace("</body>", PROBE + "\n</body>"))

    chrome = find_chrome()
    port, shutdown = serve(HERE)
    union = set()
    try:
        for lang in ("wu", "en", "ja"):
            url = "http://127.0.0.1:%d/%s?lang=%s" % (port, probe_name, lang)
            out = subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--window-size=1400,1000", "--virtual-time-budget=15000",
                 "--dump-dom", url],
                capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
            m = re.search(r'<pre id="FP">\[VIS\](.*?)\[/VIS\]</pre>', out, re.S)
            got = set(html.unescape(m.group(1))) if m else set()
            print("  ?lang=%-3s 可見字 %d" % (lang, len(got)))
            union |= got
    finally:
        shutdown()
        os.remove(probe_path)

    n0 = len(union)
    union |= {chr(c) for c in range(0x20, 0x100)}
    union |= set("▼▶■□●○◆◇·—–…「」『』（）《》〈〉〔〕、。，：；！？　・～×÷±≈")
    union |= set("βʐɿʮᵝᶽ")
    union = {c for c in union if ord(c) >= 0x20 and c != "\x7f"}

    io.open(os.path.join(HERE, "firstpaint.txt"), "w", encoding="utf-8").write("".join(sorted(union)))
    print("三語並集 %d 字，加安全邊際後 %d 字 → firstpaint.txt" % (n0, len(union)))


if __name__ == "__main__":
    main()
