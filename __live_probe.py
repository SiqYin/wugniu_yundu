# -*- coding: utf-8 -*-
"""臨時：對線上站點跑一次同韻查詢／音系浮窗／韻目，確認發布生效。"""
import re, html, subprocess, sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "https://siqyin.github.io/wugniu_yundu/"

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
    var bar=document.getElementById('btnSame').parentNode;
    add('btn_before_lang', bar.firstElementChild===document.getElementById('btnSame'));
    var rows=document.querySelectorAll('#tbl-rhymes tbody tr'), hit=null, bad=null;
    for(var i=0;i<rows.length;i++){
      var nm=rows[i].querySelector('th.rn');
      if(!nm) continue;
      if(nm.textContent.indexOf('\u4f59')===0) hit=rows[i];
      if(nm.textContent.indexOf('\u9b5a')===0) bad=rows[i];
    }
    add('yu_row', hit ? flat(hit) : '(沒有余韻列)');
    add('yu_bad', bad ? '!! 仍有魚韻列: '+flat(bad) : 'OK 無魚韻列');
  }catch(e){ add('chrome_err', e.message); }
  try{
    openSame();
    var inp=document.getElementById('srInput');
    add('only', flat(document.getElementById('i-sr-only')));
    inp.value='\u590f'; doSame();
    add('xia', flat(document.getElementById('sameout')).slice(0,140));
    inp.value='\u53a6'; doSame();
    add('xia_simp', flat(document.getElementById('sameout')).slice(0,140));
    inp.value='\u540e'; doSame();
    add('hou', flat(document.getElementById('sameout')).slice(0,120));
    inp.value='\u590f\u9ebb\u54e5'; doSame();
    add('multi_n', (flat(document.getElementById('sameout')).match(/共 \d+ 字/g)||[]).join(','));
    inp.value=''; doSame();
    add('empty', flat(document.getElementById('sameout')));
  }catch(e){ add('same_err', e.message); }
  try{
    openPhon();
    add('phon_h2', flat(document.querySelector('#phonBody h2')));
  }catch(e){ add('phon_err', e.message); }
  var p=document.createElement('pre'); p.id='TESTOUT'; p.textContent=L.join('\n');
  document.documentElement.appendChild(p);
}, 9000);
</script>
"""


def main():
    probe = "C:/tmp_live_probe.html"
    import io
    io.open(probe, "w", encoding="utf-8").write(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>x</title></head><body>"
        + PROBE + "</body></html>")
    for lang in ("wu", "en", "ja"):
        out = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--window-size=1400,1100", "--virtual-time-budget=40000",
             "--dump-dom", URL + "?lang=" + lang],
            capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
        m = re.search(r'<pre id="TESTOUT">(.*?)</pre>', out, re.S)
        print("=" * 28, lang)
        if m:
            print(html.unescape(m.group(1)))
        else:
            print("!! 沒抓到；len=%d" % len(out))
            print("   title:", re.findall(r'<title>(.*?)</title>', out, re.S)[:1])
            print("   錯誤：", re.findall(r'(Uncaught[^<\n]{0,200})', out)[:3])
            io.open("live_dump_%s.html" % lang, "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    main()
