# -*- coding: utf-8 -*-
"""臨時：抓線上頁面 → 注入探針 → 本機起服務跑無頭 Chrome，確認發布真的生效。

線上頁面不能改，所以做法是：
  1. curl 把線上 index.html 抓回本機；
  2. 注入 <base href="線上網址/">，讓字型／s2t.json／字音庫仍從線上載入；
  3. 起一個只綁 127.0.0.1 的臨時靜態伺服器，用 ?lang=wu/en/ja 分別跑。
"""
import io, os, re, html, subprocess, threading, http.server, socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LIVE = "https://siqyin.github.io/wugniu_yundu/"

PROBE = r"""
<script>
setTimeout(function(){
  var L=[];
  function add(k,v){ L.push('##'+k+'##'+String(v==null?'':v)); }
  function flat(el){ return el ? el.textContent.replace(/\s+/g,' ').trim() : '(null)'; }
  try{
    add('title', document.title);
    add('intro', flat(document.getElementById('i-phonintro')));
    add('btn', flat(document.getElementById('btnSame')));
    add('btn_at_left_of_lang',
        document.getElementById('btnSame').parentNode.firstElementChild
          === document.getElementById('btnSame'));
    var rows=document.querySelectorAll('#tbl-rhymes tbody tr');
    function rowOf(ch){ for(var i=0;i<rows.length;i++){ var nm=rows[i].querySelector('th.rn');
      if(nm && nm.textContent.indexOf(ch)===0) return flat(rows[i]).slice(0,90); }
      return '(沒有 '+ch+' 韻列)'; }
    add('da_row', rowOf('\u6253'));
    add('dang_row', rowOf('\u9ee8'));
    var stales=['\u967d','\u6c5f','\u9b5a'];
    add('stale_rhyme_rows', stales.map(function(c){
      for(var i=0;i<rows.length;i++){ var nm=rows[i].querySelector('th.rn');
        if(nm && nm.textContent.indexOf(c)===0) return '!! 仍有'+c+'韻'; }
      return '無'+c+'韻 OK'; }).join(' | '));
  }catch(e){ add('chrome_err', e.message); }
  try{
    openSame();
    add('only', flat(document.getElementById('i-sr-only')));
    var inp=document.getElementById('srInput');
    inp.value='\u590f'; doSame();
    add('xia', flat(document.getElementById('sameout')).slice(0,120));
    inp.value='\u53a6'; doSame();
    add('xia_simp', flat(document.getElementById('sameout')).slice(0,120));
    inp.value='\u540e'; doSame();
    add('hou', flat(document.getElementById('sameout')).slice(0,110));
    inp.value='\u590f\u9ebb\u54e5'; doSame();
    add('multi_blocks', (flat(document.getElementById('sameout')).match(/\u5171 \d+ \u5b57/g)||[]).join(' / '));
    inp.value=''; doSame();
    add('empty', flat(document.getElementById('sameout')));
  }catch(e){ add('same_err', e.message); }
  try{
    openPhon();
    add('phon_h2', flat(document.querySelector('#phonBody h2')));
    add('phon_len', flat(document.getElementById('phonBody')).length);
  }catch(e){ add('phon_err', e.message); }
  var p=document.createElement('pre'); p.id='TESTOUT'; p.textContent=L.join('\n');
  document.documentElement.appendChild(p);
}, 12000);
</script>
"""


def serve(directory):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=directory, **k)
        def log_message(self, *a):
            pass
    srv = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1], srv.shutdown


def main():
    raw = subprocess.run(["curl", "-s", "-H", "Cache-Control: no-cache",
                          LIVE + "index.html?cb=" + str(os.getpid())],
                         capture_output=True).stdout.decode("utf-8", "replace")
    if "btnSame" not in raw:
        print("!! 線上還是舊版（抓不到 btnSame），%d bytes" % len(raw))
        return
    print("線上 index.html 抓到，%d bytes" % len(raw))

    probe_file = os.path.join(HERE, "__live_probe_copy.html")
    io.open(probe_file, "w", encoding="utf-8").write(
        raw.replace("<head>", "<head>\n<base href='" + LIVE + "'>", 1)
           .replace("</body>", PROBE + "\n</body>"))

    port, shutdown = serve(HERE)
    try:
        for lang in ("wu", "en", "ja"):
            url = "http://127.0.0.1:%d/__live_probe_copy.html?lang=%s" % (port, lang)
            out = subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--window-size=1400,1100", "--virtual-time-budget=60000",
                 "--dump-dom", url],
                capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
            m = re.search(r'<pre id="TESTOUT">(.*?)</pre>', out, re.S)
            print("=" * 26, lang)
            if m:
                print(html.unescape(m.group(1)))
            else:
                print("!! 沒抓到 TESTOUT；len=%d" % len(out))
    finally:
        shutdown()
        os.remove(probe_file)


if __name__ == "__main__":
    main()
