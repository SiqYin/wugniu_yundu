# -*- coding: utf-8 -*-
"""苏沪混合腔韵图 —— 生成 index.html（数据驱动单页应用）

页面结构与分韵方案（scheme.json，静态）内嵌于 HTML，字音数据有两条来源：
  1. 线上字音库（实时抓取 https://siqyin.github.io/wugniu_zyinzozin/data/DB_suhu.json）
  2. 内建快照（snapshot.json，离线兜底）
两条来源解析出的结果结构相同，全部渲染由 JS 完成，因此线上字音一更新，本页随之更新。

界面文字支持三语：wu（吴语，繁体中文，默认）／en／ja，词表见 i18n_data.py。
首次访问按「手动选择 > 浏览器语言 > IP 归属地 > 英文兜底」自动判定。

输出：index.html
"""
import json, os

from i18n_data import I18N, GLOSS

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEME = json.load(open(os.path.join(HERE, "scheme.json"), encoding="utf-8"))
SNAP = json.load(open(os.path.join(HERE, "snapshot.json"), encoding="utf-8"))

N_FINALS = len(SCHEME["finals"])
N_INITIALS = len(SCHEME["initial_order"])
N_CHARS = SNAP["chars"]
N_RECORDS = SNAP["records"]
N_SYLL = SNAP["syllables"]

SCHEME_JSON = json.dumps(SCHEME, ensure_ascii=False, separators=(",", ":"))
SNAP_JSON = json.dumps(SNAP, ensure_ascii=False, separators=(",", ":"))
I18N_JSON = json.dumps(I18N, ensure_ascii=False, separators=(",", ":"))
GLOSS_JSON = json.dumps(GLOSS, ensure_ascii=False, separators=(",", ":"))


def _read_file(name):
    """讀一段原文照搬的 HTML —— 音系浮窗正文，取自字音查詢網站的同一份內容。"""
    p = os.path.join(HERE, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


PHON_WU = _read_file("phon_wu.html")
PHON_EN = _read_file("phon_en.html")
PHON_JA = _read_file("phon_ja.html")

CSS = """
:root{--ink:#1c1f23;--ink2:#5a6470;--ink3:#8b95a1;--line:#dfe4ea;--line2:#eef1f5;
--bg:#fbfcfd;--card:#fff;--yin:#e8f2fb;--yinb:#5b9bd5;--yang:#e9f6ee;--yangb:#4aa96c;
--ru:#fdeeea;--rub:#e07a5f;--te:#fdf6e3;--teb:#c2a24a;--sys:#3f6fa8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,"SimSun",serif;
 font-size:14.5px;line-height:1.75}
.wrap{max-width:1500px;margin:0 auto;padding:26px 22px 90px;position:relative}
header.top{border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:20px}
h1{font-size:29px;margin:0 0 6px;letter-spacing:.06em;padding-right:200px}
h1 small{font-size:13.5px;color:var(--ink2);font-weight:400;letter-spacing:0}
.clnote{font-size:.56em;color:var(--ink3);font-weight:400;letter-spacing:0;white-space:nowrap}
.sub{color:var(--ink2);font-size:13.5px;margin:4px 0;padding-right:200px}
.phonintro{margin:7px 0 3px;font-size:12.8px;color:var(--ink2);padding-right:200px}
.phonintro a{color:var(--yinb);text-decoration:none;border-bottom:1px dotted var(--yinb)}
.phonintro strong{color:var(--ink)}
.sub a{color:var(--yinb);text-decoration:none;border-bottom:1px dotted var(--yinb)}
h2{font-size:20px;margin:30px 0 12px;padding-left:10px;border-left:4px solid var(--ink);
 letter-spacing:.04em}
h2 small{font-weight:400;font-size:13px;color:var(--ink2);margin-left:8px;letter-spacing:0}
h2.cstitle{padding:6px 12px;border-left-width:6px;border-radius:0 8px 8px 0}
h2.cls-shu{background:#eef4fa;border-left-color:var(--sys)}
h2.cls-ru{background:var(--ru);border-left-color:var(--rub)}
h2.cls-te{background:var(--te);border-left-color:var(--teb)}
section.broad{margin-bottom:44px}
p.broadnote{margin:2px 0 6px;font-size:13.5px;color:var(--ink2);background:#f6f8fb;
 border-left:3px solid var(--line);padding:8px 12px;border-radius:0 6px 6px 0}
h3.subcls{font-size:15.5px;margin:26px 0 2px;padding:4px 12px;border-radius:0 6px 6px 0;
 letter-spacing:.08em;font-weight:700}
h3.subcls small{font-weight:400;font-size:12px;color:var(--ink2);letter-spacing:0}
h3.subcls.cls-yin{background:var(--yin);border-left:5px solid var(--yinb)}
h3.subcls.cls-yang{background:var(--yang);border-left:5px solid var(--yangb)}
h3.rname{font-size:17.5px;margin:30px 0 4px;letter-spacing:.05em;scroll-margin-top:12px}
h3.rname small{font-size:12.5px;color:var(--ink2);font-weight:400}
p.rsrc{margin:0 0 10px;font-size:12.5px;color:var(--ink2);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 6px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:8px;
 padding:8px 14px;min-width:106px}
.stat b{display:block;font-size:21px;line-height:1.25}
.stat span{font-size:12px;color:var(--ink2);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.prose{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:14px 16px 14px 36px;margin:12px 0;font-size:13.8px}
.prose li{margin:8px 0}
.prose p{margin:8px 0}
code{background:#f2f5f8;border:1px solid var(--line2);border-radius:4px;padding:0 4px;
 font-family:"SFMono-Regular",Consolas,monospace;font-size:12.5px}
.tw{overflow:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:separate;border-spacing:0;width:100%}
table.fenyun th,table.fenyun td,table.units th,table.units td{
 border-bottom:1px solid var(--line2);border-right:1px solid var(--line2);
 padding:4px 7px;font-size:12.5px;vertical-align:top;text-align:center;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
table.fenyun thead th,table.units thead th{background:#f3f6f9;font-weight:600;
 position:sticky;top:0;z-index:3;white-space:nowrap}
table.fenyun td.core,table.units td.core{font-family:Georgia,serif;color:var(--ink2);
 white-space:nowrap}
table.fenyun th.rn a,table.units th.rn a{font-family:"Songti SC","SimSun",serif;
 font-size:16px;font-weight:700;color:var(--ink);text-decoration:none;white-space:nowrap}
td.yes{background:#f8fbf9}
td.yes .hu-t{display:block;font-size:11px;color:var(--ink3)}
td.no{color:#c7ced6;background:#fafbfc}
.ipa{color:var(--ink2);font-family:Georgia,serif}
td.lab{font-family:"Songti SC","SimSun",serif;font-size:15px;white-space:nowrap}
td.lab .rd{display:block;font-family:Georgia,serif;font-size:11px;color:var(--ink3)}
td.num{color:var(--ink2)}
td.hu{white-space:nowrap;font-weight:600}
td.fin,td.rn{white-space:nowrap}
td.fin{font-weight:700}
tr.div td{background:#e9eef4;color:#3f4a56;font-weight:600;font-size:12px;
 text-align:left;padding:5px 10px;letter-spacing:.06em;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
button.cnt,button.sys{border-radius:9px;cursor:pointer;font-size:11px;padding:0 7px;
 margin:2px 2px 0;line-height:17px;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
button.cnt{border:1px solid #d5dee8;background:#f4f8fc;color:#3a6a99}
button.sys{border:1px solid #e2d6c0;background:#fdf8ef;color:#96702c}
button.cnt:hover{background:#e6f0fa;border-color:#9fc2e2}
button.sys:hover{background:#f8eed9;border-color:#d9bd85}
.mhint{font-size:13px;color:var(--ink2);margin:2px 0 6px;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
table.mtbl{width:100%;border-collapse:collapse;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
table.mtbl tr.msysrow{cursor:pointer}
table.mtbl tr.msysrow:hover{background:#f2f8ff}
table.mtbl tr.msysrow td{border-bottom:1px solid var(--line2)}
table.mtbl td{border-bottom:1px solid var(--line2);padding:5px 8px;font-size:12.8px;
 vertical-align:top}
table.mtbl td.mi{width:96px;white-space:nowrap;color:var(--ink2);font-family:Georgia,serif}
table.mtbl td.mp{width:180px;white-space:nowrap;font-family:Georgia,serif;color:#3a6a99}
table.mtbl td.mc{font-family:"Songti SC","SimSun",serif;font-size:15.5px;line-height:1.9;
 letter-spacing:.18em;word-break:break-all}
table.mtbl td.mn{width:88px;text-align:right;color:var(--ink3);font-size:11.5px;
 white-space:nowrap}
table.mtbl .dim{color:var(--ink3);font-size:13px}
.syschars{margin:4px 0 8px;background:#fbfcfe;border:1px solid var(--line2);
 border-radius:8px;padding:10px 12px;
 font-family:"Songti SC","SimSun",serif;font-size:21px;line-height:2.1;
 letter-spacing:.22em;word-break:break-all}
.mback{border:1px solid var(--line);background:#fff;border-radius:7px;padding:4px 11px;
 cursor:pointer;font-size:12.5px;color:var(--ink2);white-space:nowrap}
.mback:hover{background:#f0f3f7}
/* ---- 韻圖折疊區（預設收合，點標頭展開） ---- */
.rh{border:1px solid var(--line);border-radius:10px;background:var(--card);
 margin:13px 0;overflow:hidden;scroll-margin-top:14px}
.rh-head{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;cursor:pointer;
 padding:9px 14px;background:#f7f9fb;border-left:5px solid var(--line)}
.rh-head:hover{background:#eef4fa}
.rh.on>.rh-head{background:#e9f2fa;border-left-color:var(--yinb)}
.rh-caret{font-size:12px;color:var(--ink3);width:11px;flex:none}
.rh.on .rh-caret{color:var(--yinb)}
.rh-name{font-size:18px;font-weight:700;letter-spacing:.06em;flex:none}
.rh-meta{font-size:12px;color:var(--ink2);font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;flex:none}
.rh-hus{font-size:12px;color:var(--ink2);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;
 display:flex;gap:8px;flex-wrap:wrap}
.rh-hus .rh-hu{background:#eef2f6;border-radius:5px;padding:0 6px;white-space:nowrap}
.rh-hus .rh-hu b{font-family:Georgia,serif;color:#3a6a99}
.rh-go{margin-left:auto;font-size:12px;color:#3a6a99;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;flex:none}
.rh-body{display:none;padding:12px 14px 6px}
.rh.on>.rh-body{display:block}
sup.mod,.mod{font-size:.74em;vertical-align:.46em;line-height:0}
.yt{margin:12px 0 22px}
.yt-h{display:flex;align-items:baseline;gap:12px;padding:0 2px 6px;flex-wrap:wrap}
.yt-t{font-size:17px;font-weight:700;letter-spacing:.05em}
.yt-t i{font-style:normal;font-size:12.5px;color:var(--ink2);margin-left:5px;font-weight:400}
.yt-f{font-family:Georgia,serif;font-size:14px;color:var(--ink2)}
.yt-s{margin-left:auto;display:flex;gap:7px;align-items:baseline}
table.yuntu th,table.yuntu td{border-bottom:1px solid var(--line2);
 border-right:1px solid var(--line2);padding:2px 4px;text-align:center}
table.yuntu thead th{background:#f3f6f9;font-size:11.5px;font-weight:600;
 position:sticky;top:0;z-index:2;white-space:nowrap;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
table.yuntu thead th .pt{display:block;font-weight:400;color:var(--ink3);font-size:10px}
table.yuntu th.corner{background:#e9eef4;min-width:96px;position:sticky;left:0;z-index:4;
 font-size:11.5px;color:var(--ink2)}
table.yuntu tr.grp th{background:#f7f9fb;font-size:11px;color:var(--ink3);
 text-align:left;letter-spacing:.15em;padding:1px 6px;font-weight:500;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
table.yuntu tr.inirow.alle{opacity:.3}
table.yuntu th.ini{background:#fafbfc;position:sticky;left:0;z-index:1;
 font-family:Georgia,serif;font-size:12.5px;font-weight:600;white-space:nowrap;
 border-right:1px solid var(--line)}
table.yuntu th.ini .iv{display:block;font-size:10px;color:var(--ink3);font-weight:400}
table.yuntu td.c{min-width:53px;cursor:default}
table.yuntu td.c .ch{display:block;font-family:"Songti SC","SimSun",serif;font-size:15px;
 line-height:1.3}
table.yuntu td.c .py{display:block;font-family:Georgia,serif;font-size:9.5px;
 color:var(--ink3);line-height:1.1;white-space:nowrap}
table.yuntu td.c:hover{background:#fff8e1;outline:1.5px solid #f0c040;outline-offset:-1.5px}
table.yuntu td.e{color:#dde2e8;font-size:10px}
#tip{position:fixed;pointer-events:none;background:#20262e;color:#fff;border-radius:6px;
 padding:6px 9px;font-size:12px;max-width:460px;line-height:1.5;display:none;z-index:199;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.bars{margin:8px 0 4px;font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.bar-row{display:flex;align-items:center;gap:8px;font-size:12px;margin:2px 0}
.bar-row .bl{width:140px;text-align:right;color:var(--ink2);font-family:"Songti SC","SimSun",serif}
.bar-row .bl i{font-style:normal;font-family:Georgia,serif;color:var(--ink3);margin-left:3px}
.bar-row .bt{flex:1;height:11px;background:#f0f3f7;border-radius:6px;overflow:hidden}
.bar-row .bt i{display:block;height:100%;background:linear-gradient(90deg,#8fb8e0,#5b9bd5)}
.bar-row .bn{width:38px;color:var(--ink2);font-family:Georgia,serif}
.tools{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap}
.tools button{border:1px solid var(--line);background:var(--card);border-radius:7px;
 padding:5px 11px;font-size:12.5px;cursor:pointer;color:var(--ink2);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.tools button:hover{background:#f3f6f9}
.syncbar{display:flex;align-items:flex-start;gap:9px;flex-wrap:wrap;
 border-radius:8px;padding:8px 13px;font-size:12.8px;margin:10px 0 0;line-height:1.7;
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.syncbar.ok{background:#eef7f1;border:1px solid #c8e3d3;color:#2c6a45}
.syncbar.builtin{background:#fff8e8;border:1px solid #eeddb0;color:#8a6d1c}
.syncbar .dot{font-size:14px;line-height:1.5}
.syncbar a{color:inherit;font-weight:700}
footer{margin-top:36px;padding-top:14px;border-top:1px solid var(--line);
 font-size:12px;color:var(--ink3);
 font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
footer a{color:var(--yinb);text-decoration:none}
/* ---- 語言切換（右上角）＋ 同韻查詢按鈕（在它左邊） ---- */
.topbar{position:absolute;top:26px;right:22px;z-index:120;display:flex;gap:8px;align-items:flex-start}
.lang-switcher{position:relative}
.lang-btn{display:flex;align-items:center;gap:6px;font-size:12.5px;padding:5px 12px;
 border:1px solid var(--line);background:var(--card);border-radius:8px;cursor:pointer;
 color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.lang-btn:hover{background:#f3f6f9;border-color:#c3ced9}
.lang-caret{font-size:9px;color:var(--ink3)}
.lang-menu{display:none;position:absolute;top:calc(100% + 5px);right:0;background:var(--card);
 border:1px solid var(--line);border-radius:8px;overflow:hidden;min-width:132px;
 box-shadow:0 8px 22px rgba(20,30,45,.14)}
.lang-menu.on{display:block}
.lang-menu button{display:block;width:100%;text-align:left;padding:8px 14px;border:0;
 background:none;cursor:pointer;font-size:12.8px;color:var(--ink);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.lang-menu button:hover{background:#f2f6fa}
.lang-menu button.cur{background:#e9f2fa;font-weight:700;color:#2c5f8d}
/* ---- 同韻查詢（全螢幕浮層） ---- */
#same{position:fixed;inset:0;background:rgba(20,25,32,.5);display:none;z-index:400;
 overflow:auto;padding:30px 16px 60px}
#same.on{display:block}
.samebox{background:#fff;border-radius:14px;max-width:1180px;margin:0 auto;
 box-shadow:0 18px 50px rgba(0,0,0,.3);overflow:hidden}
.samehead{display:flex;align-items:baseline;gap:12px;padding:15px 22px;
 border-bottom:1px solid var(--line);background:#f7f9fb;flex-wrap:wrap}
.samehead b{font-size:20px;letter-spacing:.05em}
.samehead .ss{font-size:12.5px;color:var(--ink2);font-family:var(--ui);flex:1;min-width:220px}
.samehead button{margin-left:auto;border:1px solid var(--line);background:#fff;border-radius:7px;
 padding:5px 13px;cursor:pointer;font-size:12.5px;color:var(--ink2);white-space:nowrap;
 font-family:var(--ui)}
.samehead button:hover{background:#f0f3f7}
.samebody{padding:22px 22px 28px}
.sameform{display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap}
.sameform input{font-size:17px;padding:9px 14px;border:1px solid var(--line);border-radius:9px;
 width:min(360px,70vw);font-family:var(--wk);letter-spacing:.08em;color:var(--ink)}
.sameform input:focus{outline:none;border-color:var(--yinb);box-shadow:0 0 0 3px #e3eefa}
.sameform button{font-size:14px;padding:9px 24px;border:1px solid #9fc2e2;background:#f4f8fc;
 color:#2c5f8d;border-radius:9px;cursor:pointer;font-family:var(--ui);white-space:nowrap}
.sameform button:hover{background:#e6f0fa}
.samehint{text-align:center;font-size:12.5px;color:var(--ink2);margin:10px 0 0;
 font-family:var(--ui);line-height:1.6}
.sameonly{text-align:center;font-size:12.5px;color:#8a6d1c;background:#fdf8ef;
 border:1px solid #eeddb0;border-radius:8px;padding:6px 12px;margin:14px auto 0;max-width:620px;
 font-family:var(--ui)}
#sameout{margin-top:6px}
.srchar{border:1px solid var(--line);border-radius:11px;margin:16px 0 0;overflow:hidden}
.srchar>h3{margin:0;padding:8px 16px;background:#f7f9fb;border-left:5px solid var(--yinb);
 font-size:17px;letter-spacing:.05em;font-weight:700}
.srchar>h3 small{font-weight:400;font-size:12px;color:var(--ink3);margin-left:9px;letter-spacing:0}
.srread{padding:10px 16px 12px;border-top:1px solid var(--line2)}
.srread .hd{font-size:12.8px;color:var(--ink2);font-family:var(--ui);margin-bottom:7px;
 line-height:1.7}
.srread .hd b{color:var(--ink);font-size:14.5px;letter-spacing:.04em}
.srread .hd code{font-size:12.5px}
.srchars{background:#fbfcfe;border:1px solid var(--line2);border-radius:8px;
 padding:8px 11px;font-size:19px;line-height:1.95;letter-spacing:.14em;word-break:break-all;
 font-family:var(--wk)}
.srerr{padding:12px 16px;color:#a33;background:#fdeeea;border:1px solid #f2cdc4;border-radius:8px;
 margin:14px 0 0;font-family:var(--ui);font-size:13px}
/* ---- 音系浮窗（內容照字音查詢網站） ---- */
#phon{position:fixed;inset:0;background:rgba(20,25,32,.45);display:none;z-index:500;
 overflow:auto;padding:36px 16px 60px}
#phon.on{display:block}
.phon-panel{max-width:830px;margin:0 auto;background:#fff;border-radius:12px;
 box-shadow:0 18px 50px rgba(0,0,0,.28);padding:26px 34px 30px;position:relative}
.phon-panel h2{font-size:1.22em;color:#1a5276;margin:0 0 14px;padding:0 66px 8px 0;
 border-left:0;border-bottom:2px solid #c8dae8;letter-spacing:0}
.phon-panel>div{font-family:var(--ipa);color:#1a2a3a;font-size:13.5px;line-height:1.8}
.phon-close{position:absolute;top:20px;right:28px;background:#2980b9;color:#fff;border:0;
 border-radius:6px;padding:5px 13px;cursor:pointer;font-size:12.5px;font-family:var(--ui)}
.phon-close:hover{background:#1a5276}
@media (max-width:760px){
  .topbar{position:static;margin:0 0 10px}
  h1,.sub,.phonintro{padding-right:0}
  .lang-menu{right:auto;left:0}
}
#modal{position:fixed;inset:0;background:rgba(20,25,32,.45);display:none;
 align-items:flex-start;justify-content:center;z-index:300;padding:36px 16px;overflow:auto}
#modal.on{display:flex}
.mbox{background:#fff;border-radius:12px;max-width:1080px;width:100%;
 box-shadow:0 18px 50px rgba(0,0,0,.28);overflow:hidden}
.mhead{display:flex;align-items:baseline;gap:12px;padding:14px 18px;
 border-bottom:1px solid var(--line);background:#f7f9fb;position:sticky;top:0;z-index:2}
.mhead b{font-size:19px;letter-spacing:.05em}
.mhead .ms{font-size:12.5px;color:var(--ink2);
 font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
.mhead button{border:1px solid var(--line);background:#fff;border-radius:7px;
 padding:4px 12px;cursor:pointer;font-size:12.5px;color:var(--ink2);white-space:nowrap}
.mhead #mclose{margin-left:auto}
.mhead button:hover{background:#f0f3f7}
.mbody{padding:14px 18px 20px}
.mtone{margin:12px 0 4px;font-size:13.5px;font-weight:700;color:#3a4a5c;
 border-left:4px solid var(--yinb);padding-left:9px}
.mtone small{font-weight:400;color:var(--ink3);font-size:12px;margin-left:6px}
"""

# ---------------- 字體：霞鶩文楷（自託管 woff2 分片） ----------------
# make_font.py 產出 fonts/*.woff2 與 font_report.json；此處依報告生成 @font-face。
#
# 三片的 unicode-range 都是「精確」的（由各檔自身 cmap 壓縮而成，彼此不重疊）：
#   wk-ui   首屏就要用到的字        —— 訪客第一個下載的就是這一片
#   wk-dict 展開韻圖／開彈窗才用到的字 —— 使用者真的展開某個韻時才下載
#   wk-ext  霞鶩文楷收的全部 CJK 字形 —— 只有出現前兩片沒有的字時才會下載
# 精確範圍的好處：霞鶩文楷根本沒有的字（本頁有 104 個擴展 B 生僻字、2 個上游 PUA 佔位字）
# 不會誤觸 wk-ext，瀏覽器會直接交給系統字型，省掉 5 MB 的無謂下載。
FONT_FACES = []
_rep = os.path.join(HERE, "font_report.json")
if os.path.exists(_rep):
    for _it in json.load(open(_rep, encoding="utf-8")):
        # local() 優先：若使用者電腦已安裝霞鶩文楷就直接用，不必下載
        FONT_FACES.append(
            '@font-face{font-family:"%s";font-style:normal;font-weight:400;'
            'font-display:swap;src:local("LXGW WenKai"),local("霞鶩文楷"),'
            'url("fonts/%s?v=1522b") format("woff2");unicode-range:%s}'
            % (_it["family"], _it["file"], ",".join(_it["range"])))
FONTFACE_CSS = "\n".join(FONT_FACES)

# 字體棧：霞鶩文楷（兩片）放最前，其後接完整字集（回退）；
# 再後面接幾個「系統自帶、專門收擴展 B 區」的字型名稱，讓霞鶩文楷缺的生僻字也能好好顯示，
# 最後才是通用的宋體／襯線字族。
_EXTB = ('"SimSun-ExtB","MingLiU-ExtB","MiSans L3","I.Ming",'
         '"HanaMinB","BabelStone Han",')
FONT_VARS = """
:root{
--wk:"LXGW WenKai","LXGW WenKai Fallback",%s"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,"SimSun",serif;
--ui:"LXGW WenKai","LXGW WenKai Fallback",%ssystem-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;
--ipa:"LXGW WenKai","LXGW WenKai Fallback",Georgia,"Times New Roman",serif;
--mono:"LXGW WenKai","LXGW WenKai Fallback","SFMono-Regular",Consolas,"Courier New",monospace}
""" % (_EXTB, _EXTB)
_STACK_MAP = [
    ('"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,"SimSun",serif', 'var(--wk)'),
    ('"Songti SC","SimSun",serif', 'var(--wk)'),
    ('system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif', 'var(--ui)'),
    ('system-ui,-apple-system,"Segoe UI",sans-serif', 'var(--ui)'),
    ('"SFMono-Regular",Consolas,monospace', 'var(--mono)'),
    ('Georgia,serif', 'var(--ipa)'),
]
for _a, _b in _STACK_MAP:
    CSS = CSS.replace(_a, _b)
CSS = FONTFACE_CSS + "\n" + FONT_VARS + CSS

# ---------------- 首訪語言自動判定 ----------------
LANGDETECT = r"""
/* 首訪語言自動判斷：手選（localStorage 或 ?lang=） > 瀏覽器語言 > IP 歸屬地 > 英文兜底。
   單頁站，直接 setLang 切換，不產生跳轉。 */
(function () {
  var KEY = 'wugniu-yuntu-lang';
  var REGIONS = { wu: ['CN', 'HK', 'MO', 'TW'], ja: ['JP'] };
  var GEO = 'https://api.country.is/';
  var GEO_ALT = 'https://www.cloudflare.com/cdn-cgi/trace';
  var LANGS = { wu: 1, en: 1, ja: 1 };
  var setter = null, pending = null, manual = false, done = false;

  function saved() { try { var v = localStorage.getItem(KEY); return LANGS[v] ? v : null; } catch (e) { return null; } }
  function toLang(c) {
    c = String(c || '').toUpperCase();
    for (var k in REGIONS) { if (REGIONS[k].indexOf(c) >= 0) return k; }
    return 'en';
  }
  function apply(l) {
    if (!l || !LANGS[l]) return;
    if (!setter) { pending = l; return; }
    if (done) return;
    done = true; setter(l);
  }
  function fixed() { return done || !!pending; }

  var forced = null;
  try {
    var q = /[?&]lang=([a-z]+)/i.exec(location.search);
    if (q) {
      forced = q[1].toLowerCase();
      if (forced === 'auto') { try { localStorage.removeItem(KEY); } catch (e) {} forced = null; }
    }
  } catch (e) {}
  if (forced && LANGS[forced]) { manual = true; apply(forced); }

  /* 本機開啟、本機預覽不自動判斷 */
  var H = location.hostname;
  var online = location.protocol !== 'file:' && H && H !== 'localhost' && H !== '127.0.0.1' && H !== '::1';
  /* 爬蟲維持頁面預設（漢語），免得搜尋引擎收錄到英文版 */
  var isBot = /bot|crawler|spider|slurp|yandex|baiduspider|googlebot|bingbot/i.test(navigator.userAgent || '');

  if (!fixed() && !manual && online && !isBot) {
    var pick = saved();
    if (pick) { manual = true; apply(pick); }
    if (!fixed()) {
      var ls = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || ''];
      for (var i = 0; i < ls.length && !fixed(); i++) {
        var l = String(ls[i] || '').toLowerCase();
        if (/^zh(-|$)/.test(l)) apply('wu');
        else if (/^ja(-|$)/.test(l)) apply('ja');
        else if (/^en(-|$)/.test(l)) apply('en');
      }
    }
    if (!fixed()) {
      var giveUp = function () { if (!manual) apply('en'); };
      var alt = function () {
        try {
          var y = new XMLHttpRequest();
          y.open('GET', GEO_ALT, true); y.timeout = 1500;
          y.onload = function () {
            if (manual) return;
            var mm = /(?:^|\n)loc=([A-Za-z]{2})/.exec(y.responseText || '');
            apply(mm ? toLang(mm[1]) : 'en');
          };
          y.onerror = y.ontimeout = giveUp; y.send();
        } catch (e) { giveUp(); }
      };
      try {
        var x = new XMLHttpRequest();
        x.open('GET', GEO, true); x.timeout = 1500;
        x.onload = function () {
          if (manual) return;
          try { apply(toLang(JSON.parse(x.responseText).country)); } catch (e) { alt(); }
        };
        x.onerror = x.ontimeout = alt; x.send();
      } catch (e) { alt(); }
    }
  }

  window.__yuntuLang = {
    ready: function (fn) {
      setter = fn;
      if (pending) { var p = pending; pending = null; apply(p); return true; }
      return done;
    },
    pick: function (l) { manual = true; done = true; try { localStorage.setItem(KEY, l); } catch (e) {} }
  };
})();
"""

JS = r"""
var SCHEME = JSON.parse(document.getElementById('scheme').textContent);
var SNAP   = JSON.parse(document.getElementById('snapshot').textContent);
var I18N   = JSON.parse(document.getElementById('i18n').textContent);
var GLOSS  = JSON.parse(document.getElementById('gloss').textContent);

function esc(s){return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

/* ---------- 三語 ---------- */
var LANG = 'wu';
function t(k){
  var d = I18N[LANG] || {};
  return (d[k] !== undefined) ? d[k] : (I18N.wu[k] !== undefined ? I18N.wu[k] : k);
}
function n(k, o){
  return t(k).replace(/\{(\w+)\}/g, function(m, x){
    return (o && o[x] !== undefined) ? o[x] : m;
  });
}
var LANG_LABEL = {wu:'lang_wu', en:'lang_en', ja:'lang_ja'};
function langLabel(l){ return t(LANG_LABEL[l]); }

/* 把 [[读音, 代表字], …] 排成「讀音「字」」並以該語言的頓號相連 */
function sylList(list){
  var op = (LANG === 'en') ? ' ' : '「', cl = (LANG === 'en') ? '' : '」';
  return list.map(function(x){
    return '<code>'+esc(x[0])+'</code>' + (x[1] ? op+esc(x[1])+cl : '');
  }).join(t('list_sep'));
}

/* 霞鶩文楷缺 U+1D5D（ᵝ）與 U+1DBD（ᶽ）兩個修飾字母，
   改以上標的 β／ʐ 呈現，音值完全等價。 */
var MODMAP = {'\u1d5d':'β', '\u1dbd':'\u0290'};
function plainMod(s){
  return String(s).replace(/\u1d5d/g,'β').replace(/\u1dbd/g,'\u0290');
}
function fixMods(root){
  if (!root) root = document.body;
  var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), list=[], n_;
  while ((n_ = w.nextNode())){
    var p = n_.parentNode; if (!p) continue;
    var tag = p.nodeName;
    if (tag==='SCRIPT'||tag==='STYLE'||tag==='TITLE') continue;
    if (/\u1d5d|\u1dbd/.test(n_.nodeValue)) list.push(n_);
  }
  list.forEach(function(node){
    var s = node.nodeValue, frag = document.createDocumentFragment(), buf='', i, c, sp;
    for (i=0;i<s.length;i++){
      c = s.charAt(i);
      if (MODMAP[c] !== undefined){
        if (buf){ frag.appendChild(document.createTextNode(buf)); buf=''; }
        sp = document.createElement('span'); sp.className='mod';
        sp.textContent = MODMAP[c]; frag.appendChild(sp);
      } else buf += c;
    }
    if (buf) frag.appendChild(document.createTextNode(buf));
    node.parentNode.replaceChild(frag, node);
  });
}

/* ---------- 音節解析 ---------- */
var FINALS = {}; SCHEME.finals.forEach(function(f){FINALS[f]=1;});
var PAL = SCHEME.pal_map, ZERO = SCHEME.zero_map, PLAIN = SCHEME.plain;
var PAL_INIS = ['chi','shi','ci','ji'];
var HU_ORDER = SCHEME.hu_order;
var HU_KEY = {'開':'hu_kai','合':'hu_he','齊':'hu_qi','撮':'hu_cuo','特':'hu_te'};
var HU_GROUP = {};                    /* 韻 -> 陰聲/陽聲/入聲/特例 */
SCHEME.groups.forEach(function(g, gi){
  var nm = {'唇音':'grp_唇音','舌音':'grp_舌音','牙音':'grp_牙音',
            '腭音':'grp_腭音','齒音':'grp_齒音','喉音':'grp_喉音'}[g[0]] || g[0];
  SCHEME.groups[gi] = [nm, g[1]];
});
function huFull(hu){ return t(HU_KEY[hu]) + (hu==='特' ? '' : t('hu_suffix')); }
function huShort(hu){ var s = t(HU_KEY[hu]); return LANG==='en' ? s : s.charAt(0); }
var RH = SCHEME.rhymes;
/* 調類一律由 scheme.json 推出，不再手寫，免得數字跟實際調數脫節 */
var TONES_ALL = Object.keys(SCHEME.tone_info);
var TONES_SHU = SCHEME.shu_tones, TONES_RU = SCHEME.ru_tones;

/* 韵母 -> [韵序, 呼] */
var SLOT = {};
RH.forEach(function(rh, ri){
  rh.hus.forEach(function(h){
    h.finals.forEach(function(f){ SLOT[f.final] = [ri, h.hu]; });
  });
});

function parseSyl(s){
  if (s==='m'||s==='n'||s==='ng') return ['', s];
  for (var i=0;i<PAL_INIS.length;i++){
    var p=PAL_INIS[i];
    if (s.indexOf(p)===0){ var r=s.slice(p.length); return [p, PAL[r]!==undefined?PAL[r]:r]; }
  }
  for (var j=0;j<PLAIN.length;j++){
    var q=PLAIN[j];
    if (s.indexOf(q)===0) return [q, s.slice(q.length)];
  }
  if (ZERO[s]!==undefined) return ['', ZERO[s]];
  if (FINALS[s]) return ['', s];
  return null;
}

/* ---------- 两种数据源 -> 统一的小韵表 ---------- */
var CELLS = [], CELLKEY = {};
var META = {chars:0, records:0, syllables:0, skipped:0};

function addReading(syl, tone, ipa, ch){
  var p = parseSyl(syl);
  if (!p) { META.skipped++; return; }
  var ini=p[0], fin=p[1], slot=SLOT[fin];
  if (!slot) { META.skipped++; return; }
  var key = slot[0]+'|'+slot[1]+'|'+fin+'|'+ini+'|'+tone;
  var c = CELLKEY[key];
  if (!c){
    c = {ri:slot[0], hu:slot[1], fin:fin, ini:ini, tone:tone,
         ipa:[], chars:[], syl:syl+tone};
    CELLKEY[key]=c; CELLS.push(c);
  }
  if (c.ipa.indexOf(ipa)<0) c.ipa.push(ipa);
  if (ch && c.chars.indexOf(ch)<0) c.chars.push(ch);
}

function loadFromSnapshot(){
  CELLS=[]; CELLKEY={};
  META = {chars:SNAP.chars, records:SNAP.records, syllables:0, skipped:0,
          untone:SNAP.untone||[], words:SNAP.words||[], strings:SNAP.strings||0};
  SNAP.cells.forEach(function(row){
    var ini=row[0], fin=row[1], tone=row[2], ipa=row[3], chars=row[4];
    var slot=SLOT[fin]; if(!slot) return;
    var c = {ri:slot[0], hu:slot[1], fin:fin, ini:ini, tone:tone,
             ipa:[ipa], chars:Array.from(chars), syl:ini+fin+tone};
    CELLKEY[slot[0]+'|'+slot[1]+'|'+fin+'|'+ini+'|'+tone]=c; CELLS.push(c);
  });
  META.syllables = CELLS.length;
  META.single = META.syllables + META.untone.length;
}

/* 读音串去重后分三类：单音节带调（＝格位）／单音节无调／非单音节。
   无调与非单音节的条目单独收起来，供补充说明逐条列出。 */
function finishMeta(){
  var all = Object.keys(META.strSeen), unt=[], wrd=[];
  META.strings = all.length;
  all.forEach(function(s){
    var chars = META.strChars[s].join(''), mm = /^(.*?)([0-9])$/.exec(s);
    if (!mm) unt.push([s, chars]);
    else {
      var p = parseSyl(mm[1]);
      if (!p || !SLOT[p[1]]) wrd.push([s, chars]);
    }
  });
  function bySyl(a,b){ return a[0] < b[0] ? -1 : (a[0] > b[0] ? 1 : 0); }
  META.untone = unt.sort(bySyl); META.words = wrd.sort(bySyl);
  META.single = META.syllables + META.untone.length;
}

function loadFromLive(db){
  CELLS=[]; CELLKEY={};
  META = {chars:db.length, records:0, syllables:0, skipped:0,
          strSeen:{}, strChars:{}};
  db.forEach(function(rec){
    var ch = rec.character, ms = rec.meaning || [];
    META.records += ms.length;
    ms.forEach(function(m){
      var s = String(m[0]);
      if (META.strSeen[s] === undefined){ META.strSeen[s]=1; META.strChars[s]=[]; }
      if (META.strChars[s].indexOf(ch) < 0) META.strChars[s].push(ch);
      var mm = /^(.*?)([0-9])$/.exec(s);
      if (!mm) { META.skipped++; return; }
      addReading(mm[1], mm[2], m[1]||'', ch);
    });
  });
  META.syllables = CELLS.length;
  finishMeta();
}

/* ---------- 代表字：按小韵字数升序贪心分配，尽量不重复 ---------- */
function assignReps(){
  var order = CELLS.slice().sort(function(a,b){return a.chars.length-b.chars.length;});
  var used = {};
  order.forEach(function(c){
    var rep = null;
    for (var i=0;i<c.chars.length;i++) if(!used[c.chars[i]]){rep=c.chars[i];break;}
    if (rep===null) rep = c.chars[0] || '';
    c.rep = rep; used[rep]=1;
  });
  CELLS.forEach(function(c){ if(!c.rep) c.rep = c.chars[0]||''; });
}

/* ---------- 呼位（韵 × 呼）索引 ---------- */
var UNIT = [];
function buildUnits(){
  UNIT = [];
  RH.forEach(function(rh, ri){
    rh.hus.forEach(function(h){
      var cells = CELLS.filter(function(c){return c.ri===ri && c.hu===h.hu;});
      var seen = {}, chars = [];
      cells.forEach(function(c){
        c.chars.forEach(function(x){ if(!seen[x]){seen[x]=1; chars.push(x);} });
      });
      UNIT.push({ri:ri, hu:h.hu, fin:h.finals[0].final, ipa:h.finals[0].ipa,
                 cells:cells, chars:chars, nSys:cells.length, nChar:chars.length});
    });
  });
}
function unitOf(ri,hu){
  for (var i=0;i<UNIT.length;i++) if(UNIT[i].ri===ri && UNIT[i].hu===hu) return UNIT[i];
  return null;
}
function huCount(){
  var c = {}; UNIT.forEach(function(u){ c[u.hu] = (c[u.hu]||0) + 1; }); return c;
}

/* ---------- 韻目名稱與中古來源 ---------- */
function rhName(rh){ return rh.name + t('word_rhyme'); }
function glossOf(ri){
  var g = GLOSS[LANG];
  return (g && g[ri]) ? g[ri] : RH[ri].src;
}

/* ---------- 静态骨架文字 ---------- */
function renderChrome(){
  document.title = t('page_title');
  document.getElementById('i-h1').innerHTML = t('h1')
    + ' <small>' + t('tagline') + '</small>';
  document.getElementById('i-based').innerHTML = n('based_on', {
    dict: '<a href="'+SCHEME.dict_url+'" target="_blank">'+esc(t('link_dict'))+'</a>',
    rime: '<a href="https://github.com/SiqYin/wugniu_suwu" target="_blank">'+esc(t('link_rime'))+'</a>',
    chars: META.chars, records: META.records, syll: META.syllables
  });

  document.getElementById('btnSame').textContent = t('btn_same');
  document.getElementById('i-phonintro').innerHTML = t('phon_intro');
  document.getElementById('btnSync').textContent = t('btn_sync');
  document.getElementById('btnAll').textContent  = ALLOPEN ? t('btn_collapse') : t('btn_expand');
  document.getElementById('btnTop').textContent  = t('btn_top');
  document.getElementById('btnE').textContent    = hideEmpty ? t('btn_show') : t('btn_hide');
  document.getElementById('langCur').textContent = langLabel(LANG);
  /* 語言選單的三個名稱一律用同一個詞表（漢語／English／日本語），
     不管當前介面是哪一語，選項名稱都保持不變。 */
  document.getElementById('langMenu').querySelectorAll('button[data-lang]').forEach(function(b){
    b.textContent = langLabel(b.dataset.lang);
  });

  document.getElementById('i-sec-overview').textContent = t('sec_overview');
  document.getElementById('i-sec-rhymes').textContent   = t('sec_rhymes');
  document.getElementById('i-sec-units').textContent    = t('sec_units');
  document.getElementById('i-sec-yuntu').textContent    = t('sec_yuntu');
  document.getElementById('i-sec-bars').textContent     = t('sec_bars');
  document.getElementById('i-sec-notes').textContent    = t('sec_notes');

  function stat(v, label){ return '<div class="stat"><b>'+v+'</b><span>'+esc(label)+'</span></div>'; }
  document.getElementById('i-stats').innerHTML =
      stat(SCHEME.initial_order.length, t('st_initials'))
    + stat(SCHEME.finals.length, t('st_finals'))
    + stat(RH.length, t('st_rhymes'))
    + stat(UNIT.length, t('st_units'))
    + stat(TONES_ALL.length, n('st_tones', {shu: TONES_SHU.length, ru: TONES_RU.length}))
    + stat(META.syllables, t('st_cells'));

  /* 聲調表 */
  document.getElementById('i-tonetable').innerHTML =
    '<thead><tr><th>'+esc(t('th_no'))+'</th><th>'+esc(t('th_cls'))+'</th>'
    + '<th>'+esc(t('th_val'))+'</th><th>'+esc(t('th_kind'))+'</th></tr></thead><tbody>'
    + TONES_ALL.map(function(tn){
        var info = SCHEME.tone_info[tn], shu = info[2]==='舒';
        return '<tr><td class="num">'+tn+'</td><td>'+esc(t('tone_'+tn))+'</td>'
          + '<td class="ipa">'+info[1]+'</td><td style="background:'
          + (shu?'#e8f2fb':'#fdeeea')+'">'+esc(shu?t('kind_shu'):t('kind_ru'))+'</td></tr>';
      }).join('') + '</tbody>';
  document.getElementById('i-tonenote').textContent = n('tone_note', {total: TONES_ALL.length});

  /* 音系總覽要點 */
  var hc = huCount();
  var ovv = {rhymes:RH.length, units:UNIT.length, syll:META.syllables, chars:META.chars,
             strings:META.strings, n_untone:META.untone.length, n_word:META.words.length,
             n_single:META.single,
             list_untone:sylList(META.untone), list_word:sylList(META.words),
             n_kai:hc['開']||0, n_he:hc['合']||0, n_qi:hc['齊']||0,
             n_cuo:hc['撮']||0, n_te:hc['特']||0, btn_expand:t('btn_expand')};
  document.getElementById('i-ovlist').innerHTML =
    ['ov1','ov2','ov3','ov4','ov5','ov6','ov7','ov8','ov9']
      .map(function(k){ return '<li>'+n(k, ovv)+'</li>'; }).join('');

  document.getElementById('i-rt-note').innerHTML = t('rt_note');
  document.getElementById('i-ut-note').innerHTML = t('ut_note');
  document.getElementById('i-yt-note').innerHTML = n('ov9', ovv);
  document.getElementById('i-barsnote').textContent = t('bars_note');

  document.getElementById('i-notelist').innerHTML =
    ['n1','n2','n3','n4','n5','n6','n7','n8','n9']
      .map(function(k){ return '<p>'+n(k, ovv)+'</p>'; }).join('');

  document.getElementById('i-footer').innerHTML = n('footer', {
    rhymes: RH.length, units: UNIT.length, finals: SCHEME.finals.length,
    link: '<a href="'+SCHEME.dict_url+'" target="_blank">'+esc(t('link_dict'))+'</a>'
  });

  paintSync();
}

/* ---------- 表格按钮 ---------- */
function cntBtn(ri,hu,label){
  return '<button class="cnt" data-ri="'+ri+'" data-hu="'+hu+'">'+esc(label)+'</button>';
}
function sysBtn(ri,hu,label){
  return '<button class="sys" data-ri="'+ri+'" data-hu="'+hu+'">'+esc(label)+'</button>';
}
function unitBtns(ri,hu,u){
  return sysBtn(ri,hu,u.nSys+' '+t('word_sys')) + cntBtn(ri,hu,u.nChar+' '+t('word_chars'));
}

function renderRhymeTable(){
  var rows = [], lastBroad = null;
  RH.forEach(function(rh, ri){
    var broad = rh.cls==='入聲韻' ? '入' : (rh.cls==='特例韻' ? '特' : '舒');
    if (broad !== lastBroad){
      lastBroad = broad;
      rows.push('<tr class="div"><td colspan="12">'
        + esc(t({'舒':'div_shu','入':'div_ru','特':'div_te'}[broad])) + '</td></tr>');
    }
    var cells='', nSys=0, nChar=0, nHu=0;
    HU_ORDER.forEach(function(hu){
      var u = unitOf(ri,hu);
      if (u){
        nHu++; nSys+=u.nSys; nChar+=u.nChar;
        cells += '<td class="yes"><span class="hu-t">'+esc(huFull(hu))+'</span><b>'+u.fin
               + '</b> <span class="ipa">['+u.ipa+']</span>'
               + '<span style="display:block">' + unitBtns(ri,hu,u) + '</span></td>';
      } else cells += '<td class="no">—</td>';
    });
    var clsShort = {'陰聲韻':'cls_yin','陽聲韻':'cls_yang','入聲韻':'cls_ru','特例韻':'cls_te'}[rh.cls];
    rows.push('<tr><th class="rn"><a href="#r-'+ri+'">'+esc(rhName(rh))+'</a></th>'
      + '<td class="core">['+rh.core+']</td><td>'+esc(t(clsShort))+'</td>'
      + '<td class="lab">'+esc(rh.name)+'<span class="rd">'+esc(rh.label_read)+'</span></td>'
      + cells + '<td class="num">'+nHu+'</td><td class="num">'+nSys+'</td>'
      + '<td class="num">'+nChar+'</td></tr>');
  });
  document.getElementById('tbl-rhymes').innerHTML =
    '<table class="fenyun"><thead>'
    + '<tr><th rowspan="2">'+esc(t('word_rhyme').trim())+'</th>'
    + '<th rowspan="2">'+esc(t('lbl_core'))+'</th><th rowspan="2">'+esc(t('th_class'))+'</th>'
    + '<th rowspan="2">'+esc(t('rh_label'))+'</th>'
    + '<th colspan="5">'+esc(t('rt_hu4'))
    + '</th><th rowspan="2">'+esc(t('lbl_hu'))+'</th>'
    + '<th rowspan="2">'+esc(t('lbl_sys'))+'</th>'
    + '<th rowspan="2">'+esc(t('lbl_chars'))+'</th></tr>'
    + '<tr>' + HU_ORDER.map(function(h){return '<th>'+esc(huFull(h))+'</th>';}).join('') + '</tr>'
    + '</thead><tbody>' + rows.join('') + '</tbody></table>';
}

function renderUnitTable(){
  var rows = [], lastBroad = null;
  UNIT.forEach(function(u, i){
    var cls = RH[u.ri].cls;
    var broad = cls==='入聲韻' ? '入' : (cls==='特例韻' ? '特' : '舒');
    if (broad !== lastBroad){
      lastBroad = broad;
      rows.push('<tr class="div"><td colspan="9">'
        + esc(t({'舒':'div_shu_short','入':'div_ru_short','特':'div_te_short'}[broad]))
        + '</td></tr>');
    }
    var clsShort = {'陰聲韻':'cls_yin','陽聲韻':'cls_yang','入聲韻':'cls_ru','特例韻':'cls_te'}[cls];
    rows.push('<tr><td class="num">'+(i+1)+'</td>'
      + '<td class="rn"><a href="#r-'+u.ri+'-'+u.hu+'">'+esc(rhName(RH[u.ri]))+'</a></td>'
      + '<td class="core">['+RH[u.ri].core+']</td><td>'+esc(t(clsShort))+'</td>'
      + '<td class="hu">'+esc(huFull(u.hu))+'</td><td class="fin">'+u.fin+'</td>'
      + '<td class="ipa">['+u.ipa+']</td>'
      + '<td class="num">'+sysBtn(u.ri,u.hu,u.nSys)+'</td>'
      + '<td class="num">'+cntBtn(u.ri,u.hu,u.nChar)+'</td></tr>');
  });
  document.getElementById('tbl-units').innerHTML =
    '<table class="units"><thead><tr><th>#</th>'
    + '<th>'+esc(t('word_rhyme').trim())+'</th><th>'+esc(t('lbl_core'))+'</th>'
    + '<th>'+esc(t('th_class'))+'</th><th>'+esc(t('lbl_hu'))+'</th>'
    + '<th>'+esc(t('st_finals'))+'</th><th>IPA</th>'
    + '<th>'+esc(t('lbl_sys'))+'</th><th>'+esc(t('lbl_chars'))+'</th></tr></thead>'
    + '<tbody>' + rows.join('') + '</tbody></table>';
}

/* ---------- 韻圖 ---------- */
function toneList(rh){ return (rh.cls==='入聲韻') ? SCHEME.ru_tones : SCHEME.shu_tones; }

function yuntuTable(u){
  var rh = RH[u.ri];
  var tones = toneList(rh);
  var body = [];
  SCHEME.groups.forEach(function(g){
    body.push('<tr class="grp"><th colspan="'+(tones.length+1)+'">'+esc(t(g[0]))+'</th></tr>');
    g[1].forEach(function(ini){
      var tds = [], empty = true;
      tones.forEach(function(tn){
        var c = null;
        for (var i=0;i<u.cells.length;i++)
          if (u.cells[i].ini===ini && u.cells[i].tone===tn){c=u.cells[i];break;}
        if (c){
          empty = false;
          var tip = c.rep+'　'+c.syl+'　['+c.ipa.join('/')+']　'
                  + n('md_n_chars', {n:c.chars.length}) + '：'+c.chars.slice(0,80).join('');
          tds.push('<td class="c" data-tip="'+esc(tip)+'"><span class="ch">'+esc(c.rep)
                 + '</span><span class="py">'+esc(c.syl.slice(0,-1))+'</span></td>');
        } else tds.push('<td class="e">·</td>');
      });
      body.push('<tr class="inirow'+(empty?' alle':'')+'"><th class="ini">'+esc(ini||'∅')
        + '<span class="iv">'+SCHEME.initials[ini][2]+'</span></th>'+tds.join('')+'</tr>');
    });
  });
  return '<div class="yt" id="r-'+u.ri+'-'+u.hu+'"><div class="yt-h">'
    + '<span class="yt-t">'+esc(rh.name)+'<i>'+esc(huFull(u.hu))+'</i></span>'
    + '<span class="yt-f">'+u.fin+' <b>['+u.ipa+']</b></span>'
    + '<span class="yt-s">' + unitBtns(u.ri,u.hu,u) + '</span></div>'
    + '<div class="tw"><table class="yuntu"><thead><tr><th class="corner">'
    + esc(t('yt_corner'))+'</th>'
    + tones.map(function(tn){return '<th>'+esc(t('tone_'+tn))+'<span class="pt">'
        + SCHEME.tone_info[tn][1]+'</span></th>';}).join('')
    + '</tr></thead><tbody>'+body.join('')+'</tbody></table></div></div>';
}

function rhymeBlock(rh, ri){
  var nu = rh.hus.length, nSys = 0, nChar = 0;
  rh.hus.forEach(function(h){
    var u = unitOf(ri, h.hu); nSys += u.nSys; nChar += u.nChar;
  });
  var hus = rh.hus.map(function(h){
    var u = unitOf(ri, h.hu);
    return '<span class="rh-hu">'+esc(huFull(h.hu))+' <b>'+u.fin+'</b> [<span class="ipa">'
      + u.ipa + '</span>]</span>';
  }).join('');
  return '<div class="rh" id="rh-'+ri+'">'
    + '<div class="rh-head" data-ri="'+ri+'">'
    + '<span class="rh-caret">▶</span>'
    + '<span class="rh-name">'+esc(rhName(rh))+'</span>'
    + '<span class="rh-meta">'+esc(t('lbl_core'))+' ['+rh.core+'] ・ '
    + esc(t({'陰聲韻':'div_shu_short','陽聲韻':'div_shu_short',
              '入聲韻':'div_ru_short','特例韻':'div_te_short'}[rh.cls]))+' ・ '
    + esc(t('lbl_hu'))+' '+nu+' ・ '+esc(t('lbl_sys'))+' '+nSys
    + ' ・ '+esc(t('lbl_chars'))+' '+nChar+'</span>'
    + '<span class="rh-hus">'+hus+'</span>'
    + '<span class="rh-go">'+esc(t('rh_open'))+' ▼</span>'
    + '</div>'
    + '<div class="rh-body" id="rhb-'+ri+'"></div></div>';
}

/* 韻圖預設收合，展開時才即時繪製 */
var rhOpen = {}, ALLOPEN = false;

function renderRhymeBody(ri){
  var box = document.getElementById('rhb-'+ri);
  if (!box || box.dataset.done === '1') return;
  var rh = RH[ri], html = '';
  rh.hus.forEach(function(h){ html += yuntuTable(unitOf(ri, h.hu)); });
  box.innerHTML = '<p class="rsrc">'+esc(t('rh_label'))+'：<b>'+esc(rh.name)+'</b> ＝ '
    + esc(rh.label_read)+'；'+esc(t('rh_src'))+'：'+esc(glossOf(ri))+'</p>' + html;
  box.dataset.done = '1';
  applyHideEmpty(box);
  fixMods(box);
}

function expandRhyme(ri, noScroll){
  var d = document.getElementById('rh-'+ri);
  if (!d) return;
  renderRhymeBody(ri);
  d.classList.add('on'); rhOpen[ri] = 1;
  if (!noScroll) d.scrollIntoView({block:'nearest'});
}

function collapseRhyme(ri){
  var d = document.getElementById('rh-'+ri);
  if (!d) return;
  d.classList.remove('on'); rhOpen[ri] = 0;
}

function toggleRhyme(ri){
  var d = document.getElementById('rh-'+ri);
  if (!d) return;
  if (d.classList.contains('on')) collapseRhyme(ri); else expandRhyme(ri, true);
}

function allRhymes(open){
  RH.forEach(function(rh, ri){ if (open) expandRhyme(ri, true); else collapseRhyme(ri); });
  ALLOPEN = open;
  document.getElementById('btnAll').textContent = open ? t('btn_collapse') : t('btn_expand');
  return false;
}

function goUnit(ri, hu){
  expandRhyme(ri, true);
  var el = document.getElementById('r-'+ri+'-'+hu);
  if (el) el.scrollIntoView({block:'start'});
}

function renderYuntu(){
  var parts = [];
  function pick(cls){
    var a=[]; RH.forEach(function(r,i){ if(r.cls===cls) a.push([r,i]); }); return a;
  }
  function sum(arr){
    var cnt=arr.length, hu=0, sy=0, ch=0;
    arr.forEach(function(x){
      hu += x[0].hus.length;
      x[0].hus.forEach(function(h){
        var u = unitOf(x[1], h.hu); sy += u.nSys; ch += u.nChar;
      });
    });
    return {n:cnt, hu:hu, sy:sy, ch:ch};
  }
  var yin=pick('陰聲韻'), yang=pick('陽聲韻'), ru=pick('入聲韻'), te=pick('特例韻');
  var su = sum(yin.concat(yang));
  function meta(o){ return ' ・ ' + esc(t('lbl_hu')) + ' ' + o.hu + ' ・ '
    + esc(t('lbl_sys')) + ' ' + o.sy + ' ・ ' + esc(t('lbl_chars')) + ' ' + o.ch; }

  parts.push('<section class="sect broad"><h2 class="cstitle cls-shu">'+esc(t('yt_shu'))
    + ' <small>' + su.n + ' ・ ' + esc(t('div_shu_short')) + meta(su) + '</small></h2>'
    + '<p class="broadnote">' + t('yt_shu_note') + '</p>');

  [['陰聲韻','yt_yin','yt_yin_note','yin',yin],
   ['陽聲韻','yt_yang','yt_yang_note','yang',yang]].forEach(function(g){
    var s = sum(g[4]);
    parts.push('<h3 class="subcls cls-'+g[3]+'">'+esc(t(g[1]))
      + ' <small>'+esc(t(g[2]))+' ・ ' + s.n + meta(s) + '</small></h3>');
    g[4].forEach(function(x){ parts.push(rhymeBlock(x[0], x[1])); });
  });
  parts.push('</section>');

  var sru = sum(ru);
  parts.push('<section class="sect broad"><h2 class="cstitle cls-ru">'+esc(t('yt_ru'))
    + ' <small>' + sru.n + meta(sru) + '</small></h2>'
    + '<p class="broadnote">' + t('yt_ru_note') + '</p>');
  ru.forEach(function(x){ parts.push(rhymeBlock(x[0], x[1])); });
  parts.push('</section>');

  var ste = sum(te);
  parts.push('<section class="sect broad"><h2 class="cstitle cls-te">'+esc(t('yt_te'))
    + ' <small>' + ste.n + meta(ste) + '</small></h2>'
    + '<p class="broadnote">' + t('yt_te_note') + '</p>');
  te.forEach(function(x){ parts.push(rhymeBlock(x[0], x[1])); });
  parts.push('</section>');

  document.getElementById('sections').innerHTML = parts.join('');
}

function renderBars(){
  var top = UNIT.slice().sort(function(a,b){return b.nChar-a.nChar;}).slice(0,24);
  var max = top.length ? top[0].nChar : 1;
  document.getElementById('bars').innerHTML = top.map(function(u){
    return '<div class="bar-row"><span class="bl">'+esc(rhName(RH[u.ri]))+esc(huShort(u.hu))
      + '<i>'+u.fin+'</i></span><span class="bt"><i style="width:'
      + (u.nChar/max*100).toFixed(1)+'%"></i></span><span class="bn">'+u.nChar
      + '</span></div>';
  }).join('');
}

/* ---------- 交互：收合、錨點 ---------- */
var hideEmpty = false;
function applyHideEmpty(scope){
  (scope || document).querySelectorAll('table.yuntu tr.inirow').forEach(function(tr){
    tr.style.display = (hideEmpty && tr.classList.contains('alle')) ? 'none' : '';
  });
}
function toggleEmpty(){
  hideEmpty = !hideEmpty;
  applyHideEmpty(document);
  document.getElementById('btnE').textContent = hideEmpty ? t('btn_show') : t('btn_hide');
  return false;
}
function toggleLangMenu(){
  var m = document.getElementById('langMenu');
  m.classList.toggle('on');
  return false;
}
function pickLang(l){
  window.__yuntuLang.pick(l);
  document.getElementById('langMenu').classList.remove('on');
  applyLang(l);
  return false;
}

/* ---------- 彈窗：呼位 → 小韻一覽 → 某個小韻的全部字 ---------- */
function iniByOrder(a, b){
  return SCHEME.initial_order.indexOf(a.ini) - SCHEME.initial_order.indexOf(b.ini);
}

function showSysList(ri, hu){
  var u = unitOf(ri, hu), rh = RH[ri];
  var html = '<p class="mhint">' + n('md_hint_sys', {
    rhyme: esc(rhName(rh)), hu: esc(huFull(hu)), fin: u.fin, ipa: u.ipa,
    nsys: u.nSys }) + '</p>';
  toneList(rh).forEach(function(tn){
    var cs = u.cells.filter(function(c){return c.tone===tn;}).sort(iniByOrder);
    if (!cs.length) return;
    var cnt = 0; cs.forEach(function(c){ cnt += c.chars.length; });
    html += '<div class="mtone">' + n('md_tone_head', {
      name: esc(t('tone_'+tn)), no: tn, val: SCHEME.tone_info[tn][1],
      nsys: cs.length, nchars: cnt
    }) + '</div><table class="mtbl"><tbody>';
    cs.forEach(function(c){
      html += '<tr class="msysrow" data-ri="'+ri+'" data-hu="'+hu+'" data-ini="'
        + c.ini+'" data-tone="'+c.tone+'">'
        + '<td class="mi">'+esc(c.ini||'∅')+'<br><span style="font-size:10.5px;color:#8b95a1">'
        + SCHEME.initials[c.ini][2]+'</span></td>'
        + '<td class="mp">'+esc(c.syl)+'<br><span style="font-size:11px;color:#8b95a1">['
        + esc(c.ipa.join('/'))+']</span></td>'
        + '<td class="mc">'+esc(c.chars.slice(0,14).join(' '))
        + (c.chars.length>14 ? ' <span class="dim">'+esc(t('md_etc'))+'</span>' : '')+'</td>'
        + '<td class="mn">' + c.chars.length + ' ' + esc(t('word_char')) + '</td></tr>';
    });
    html += '</tbody></table>';
  });
  openModal(rhName(rh) + ' ' + huFull(hu),
            n('md_sys_sub', {fin:u.fin, ipa:u.ipa, nchars:u.nChar, nsys:u.nSys}), html, true);
  MODAL = {kind:'syslist', ri:ri, hu:hu};
}

function showSysChars(ri, hu, ini, tone){
  var u = unitOf(ri, hu), rh = RH[ri], c = null;
  for (var i=0;i<u.cells.length;i++)
    if (u.cells[i].ini===ini && u.cells[i].tone===tone){c=u.cells[i];break;}
  if (!c) return;
  var html = '<div class="mtone">'+esc(t('md_allchars'))
    + '<small>'+n('md_n_chars',{n:c.chars.length})+'</small></div>'
    + '<div class="syschars">'+esc(c.chars.join(' '))+'</div>';
  openModal(rhName(rh) + ' ' + huFull(hu) + '　' + c.syl,
            n('md_direct_sub', {nchars:c.chars.length}), html, false);
  MODAL = {kind:'syschars', ri:ri, hu:hu, ini:ini, tone:tone};
}

function showUnitAllChars(ri, hu){
  var u = unitOf(ri, hu), rh = RH[ri];
  var html = '<div class="mtone">' + n('md_allchars_head', {nchars:u.nChar, nsys:u.nSys})
    + '</div><div class="syschars">'+esc(u.chars.join(' '))+'</div>';
  toneList(rh).forEach(function(tn){
    var cs = u.cells.filter(function(c){return c.tone===tn;}).sort(iniByOrder);
    if (!cs.length) return;
    var cnt = 0; cs.forEach(function(c){ cnt += c.chars.length; });
    html += '<div class="mtone">' + n('md_tone_head', {
      name: esc(t('tone_'+tn)), no: tn, val: SCHEME.tone_info[tn][1],
      nsys: cs.length, nchars: cnt
    }) + '</div><table class="mtbl"><tbody>';
    cs.forEach(function(c){
      html += '<tr><td class="mi">'+esc(c.ini||'∅')
        + '<br><span style="font-size:10.5px;color:#8b95a1">'+SCHEME.initials[c.ini][2]
        + '</span></td><td class="mp">'+esc(c.syl)
        + '<br><span style="font-size:11px;color:#8b95a1">['
        + esc(c.ipa.join('/'))+']</span></td>'
        + '<td class="mc">'+esc(c.chars.join(' '))+'</td>'
        + '<td class="mn">'+c.chars.length+' '+esc(t('word_char'))+'</td></tr>';
    });
    html += '</tbody></table>';
  });
  openModal(rhName(rh) + ' ' + huFull(hu),
            n('md_sys_sub', {fin:u.fin, ipa:u.ipa, nchars:u.nChar, nsys:u.nSys}), html, false);
  MODAL = {kind:'unitall', ri:ri, hu:hu};
}

var CUR = null;            /* 目前彈窗所在的呼位，供「返回」用 */
var MODAL = null;          /* 目前彈窗的層級，供切換語言時重繪 */
function reopenModal(){
  if (!MODAL) return;
  if (MODAL.kind === 'syslist') showSysList(MODAL.ri, MODAL.hu);
  else if (MODAL.kind === 'unitall') showUnitAllChars(MODAL.ri, MODAL.hu);
  else showSysChars(MODAL.ri, MODAL.hu, MODAL.ini, MODAL.tone);
}
function openModal(title, sub, bodyHtml, isList){
  document.getElementById('mtitle').textContent = title;
  document.getElementById('msub').textContent = sub;
  document.getElementById('mbody').innerHTML = bodyHtml;
  document.getElementById('mback').style.display = isList ? 'none' : '';
  document.getElementById('mback').textContent = t('md_back');
  document.getElementById('mclose').textContent = t('md_close');
  document.getElementById('modal').classList.add('on');
  fixMods(document.getElementById('mbody'));
}
function closeModal(){ document.getElementById('modal').classList.remove('on'); }

/* ---------- 音系浮窗：正文與字音查詢網站同一份，三語各一份 ---------- */
var PHON = {};
['wu','en','ja'].forEach(function(l){
  var el = document.getElementById('phon-'+l);
  if (el) PHON[l] = el.textContent;
});
function openPhon(){
  document.getElementById('phonClose').textContent = t('sr_close');
  document.getElementById('phonBody').innerHTML = PHON[LANG] || PHON.wu || '';
  document.getElementById('phon').classList.add('on');
  fixMods(document.getElementById('phonBody'));
  return false;
}
function closePhon(){ document.getElementById('phon').classList.remove('on'); }

/* ---------- 同韻查詢 ----------
   輸入漢字 -> 逐一取其在韻圖裡的每個讀音 -> 列出該讀音所屬韻的全部字（不分呼）。
   簡繁對照表 s2t.json 只在第一次打開時抓一次，抓不到就只支援繁體輸入。 */
var S2T = null, S2T_DONE = false, SAME_LAST = '';
function loadS2T(){
  if (S2T_DONE) return;
  S2T_DONE = true;
  fetch('s2t.json', {cache:'force-cache'}).then(function(r){
    if (!r.ok) throw new Error('HTTP '+r.status);
    return r.json();
  }).then(function(j){ S2T = j || {}; }).catch(function(){ S2T = {}; });
}

/* 一個字在韻圖裡的全部讀音（每個讀音就是一個小韻格） */
function readingsOf(ch){
  return CELLS.filter(function(c){ return c.chars.indexOf(ch) >= 0; });
}

/* 一個韻底下的全部字（開合齊撮都收，按字去重） */
var RH_CHARS = [];
function rhymeChars(ri){
  if (RH_CHARS[ri]) return RH_CHARS[ri];
  var seen = {}, out = [];
  CELLS.forEach(function(c){
    if (c.ri !== ri) return;
    c.chars.forEach(function(x){ if (!seen[x]){ seen[x]=1; out.push(x); } });
  });
  RH_CHARS[ri] = out;
  return out;
}

/* 簡體 -> 繁體候選；一簡對多繁時全部展開，來源字本身也保留 */
function expandInput(str){
  var out = [], seen = {};
  Array.from(str).forEach(function(c){
    if (!/\S/.test(c) || seen[c]) return;
    seen[c] = 1;
    var tg = (S2T && S2T[c]) || [];
    if (!tg.length){ out.push({ch:c}); return; }
    if (tg.indexOf(c) >= 0) out.push({ch:c});
    tg.forEach(function(x){
      if (x === c || seen[x]) return;
      seen[x] = 1;
      out.push({ch:x, from:c});
    });
  });
  return out;
}

function renderSameChrome(){
  document.getElementById('btnSame').textContent = t('btn_same');
  document.getElementById('srClose').textContent = t('sr_close');
  document.getElementById('i-sr-title').textContent = t('sr_title');
  document.getElementById('i-sr-sub').textContent = t('sr_sub');
  document.getElementById('srInput').placeholder = t('sr_ph');
  document.getElementById('srGo').textContent = t('sr_go');
  document.getElementById('i-sr-hint').textContent = t('sr_hint');
  document.getElementById('i-sr-only').textContent = t('sr_only');
}
function openSame(){
  loadS2T(); renderSameChrome();
  document.getElementById('same').classList.add('on');
  setTimeout(function(){
    var i = document.getElementById('srInput');
    if (i) i.focus();
  }, 40);
  return false;
}
function closeSame(){ document.getElementById('same').classList.remove('on'); return false; }

function doSame(){
  var raw = (document.getElementById('srInput').value || '').trim();
  SAME_LAST = raw;
  var out = document.getElementById('sameout');
  var cs = Array.from(raw).filter(function(c){ return /\S/.test(c); });
  if (!cs.length){ out.innerHTML = '<div class="srerr">'+esc(t('sr_empty'))+'</div>'; return false; }
  if (cs.length > 8){ out.innerHTML = '<div class="srerr">'+esc(t('sr_max'))+'</div>'; return false; }
  loadS2T();

  var html = '', any = false;
  expandInput(raw).forEach(function(item){
    var c = item.ch, rs = readingsOf(c);
    if (!rs.length){
      if (!item.from) html += '<div class="srerr">'+esc(n('sr_none', {c:c}))+'</div>';
      return;
    }
    any = true;
    html += '<div class="srchar"><h3>'+esc(c)
          + (item.from ? '<small>'+esc(n('sr_conv', {c:item.from}))+'</small>' : '')
          + '</h3>';
    var byR = {};
    rs.forEach(function(cc){ (byR[cc.ri] = byR[cc.ri] || []).push(cc); });
    Object.keys(byR).sort(function(a,b){ return a-b; }).forEach(function(k){
      var ri = +k, group = byR[k], chs = rhymeChars(ri);
      var seenSyl = {}, syls = [];
      group.forEach(function(cc){
        if (seenSyl[cc.syl]) return;
        seenSyl[cc.syl] = 1;
        syls.push('<code>'+esc(cc.syl)+'</code> ['+esc(plainMod(cc.ipa.join('/')))+']');
      });
      html += '<div class="srread"><div class="hd">'
            + '<b>'+esc(rhName(RH[ri]))+'</b> ・ ' + syls.join(' ・ ')
            + ' ・ ' + esc(n('sr_words', {n: chs.length}))
            + '</div><div class="srchars">'+esc(chs.join(''))+'</div></div>';
    });
    html += '</div>';
  });
  out.innerHTML = html || '<div class="srerr">'+esc(t('sr_empty'))+'</div>';
  fixMods(out);
  return false;
}

document.addEventListener('click', function(e){
  var hd = e.target.closest('.rh-head');
  if (hd && !e.target.closest('button')){ toggleRhyme(+hd.dataset.ri); return; }

  var an = e.target.closest('a[href^="#r-"]');
  if (an){
    var m = an.getAttribute('href').match(/^#r-(\d+)(?:-(.+))?$/);
    if (m){
      e.preventDefault();
      if (m[2]) goUnit(+m[1], m[2]); else expandRhyme(+m[1]);
      return;
    }
  }
  var b = e.target.closest('button.sys');
  if (b){
    CUR = {ri:+b.dataset.ri, hu:b.dataset.hu};
    showSysList(CUR.ri, CUR.hu); return;
  }
  var c = e.target.closest('button.cnt');
  if (c){
    CUR = {ri:+c.dataset.ri, hu:c.dataset.hu};
    showUnitAllChars(CUR.ri, CUR.hu); return;
  }
  var row = e.target.closest('tr.msysrow');
  if (row){
    CUR = {ri:+row.dataset.ri, hu:row.dataset.hu};
    showSysChars(CUR.ri, row.dataset.hu, row.dataset.ini, row.dataset.tone); return;
  }
  if (e.target.closest('#mback')){
    if (CUR) showSysList(CUR.ri, CUR.hu);
    return;
  }
  if (e.target.id==='modal' || e.target.closest('#mclose')) closeModal();
});
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape'){ closeModal(); closeSame(); closePhon(); }
});

document.addEventListener('mouseover', function(e){
  var td = e.target.closest('td.c');
  if (!td) return;
  var tip = document.getElementById('tip');
  tip.textContent = plainMod(td.dataset.tip); tip.style.display = 'block';
});
document.addEventListener('mousemove', function(e){
  var tip = document.getElementById('tip');
  if (tip.style.display !== 'block') return;
  var x = e.clientX+14, y = e.clientY+16, r = tip.getBoundingClientRect();
  if (x+r.width > innerWidth-10) x = e.clientX-r.width-14;
  if (y+r.height > innerHeight-10) y = e.clientY-r.height-16;
  tip.style.left = x+'px'; tip.style.top = y+'px';
});
document.addEventListener('mouseout', function(e){
  if (e.target.closest('td.c')) document.getElementById('tip').style.display='none';
});

/* ---------- 同步狀態條 ---------- */
var SYNC = {type:'loading', data:{}};
function paintSync(){
  var el = document.getElementById('syncbar'), cls = 'builtin', html = '';
  if (SYNC.type === 'loading'){
    html = '<span class="dot">⏳</span><span>'+esc(t('sync_loading'))+'</span>';
  } else if (SYNC.type === 'ok'){
    cls = 'ok';
    html = '<span class="dot">✅</span><span>' + n('sync_ok', {
      link: '<a href="'+SCHEME.dict_url+'" target="_blank">'+esc(t('link_dict'))+'</a>',
      chars: META.chars, records: META.records, syll: META.syllables,
      stamp: SYNC.data.stamp ? n('sync_ok_stamp', {t:SYNC.data.stamp}) : ''
    }) + '</span>';
  } else if (SYNC.type === 'stale'){
    html = '<span class="dot">⚠️</span><span>' + n('sync_stale', {
      link: '<a href="'+SCHEME.dict_url+'" target="_blank">'+esc(t('link_dict'))+'</a>',
      live: SYNC.data.live, snap: META.chars, btn: esc(t('btn_sync'))
    }) + '</span>';
  } else {
    html = '<span class="dot">⚠️</span><span>' + n('sync_fail', {
      err: esc(SYNC.data.err||''), chars: META.chars, records: META.records }) + '</span>';
  }
  el.className = 'syncbar ' + cls;
  el.innerHTML = html;
}

function fmtDate(s){
  if (!s) return '';
  var d = new Date(s);
  if (isNaN(d.getTime())) return s;
  function p(x){ return (x<10?'0':'')+x; }
  return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '
       + p(d.getHours())+':'+p(d.getMinutes());
}

function sync(){
  SYNC = {type:'loading', data:{}}; paintSync();
  fetch(SCHEME.live_url, {cache:'no-store'}).then(function(r){
    if (!r.ok) throw new Error('HTTP '+r.status);
    var stamp = r.headers.get('last-modified') || '';
    return r.json().then(function(db){ return {db:db, stamp:stamp}; });
  }).then(function(res){
    /* 線上抓回來的若比內建快照還舊（見 liveOlderThanSnapshot），
       就用內建快照，別拿舊的蓋掉新的。 */
    if (liveOlderThanSnapshot(res.db)){
      loadFromSnapshot(); renderAll();
      SYNC = {type:'stale', data:{live:res.db.length}}; paintSync();
      return;
    }
    loadFromLive(res.db); renderAll();
    SYNC = {type:'ok', data:{stamp: fmtDate(res.stamp)}}; paintSync();
  }).catch(function(err){
    loadFromSnapshot(); renderAll();
    SYNC = {type:'fail', data:{err: err.message || String(err)}}; paintSync();
  });
}

var SNAP_CHARS = null;
function snapCharSet(){
  if (!SNAP_CHARS){
    SNAP_CHARS = {};
    SNAP.cells.forEach(function(row){
      Array.from(row[4]).forEach(function(c){ SNAP_CHARS[c] = 1; });
    });
    if (SNAP.extra_chars) Array.from(SNAP.extra_chars).forEach(function(c){ SNAP_CHARS[c] = 1; });
  }
  return SNAP_CHARS;
}

/* 線上字庫是不是「內建快照的真子集」？是的話就代表線上那份是舊版
   （字典網站的 Pages 還在部署，或 CDN 還在端十分鐘前的快取），
   此時頁面寧可顯示較新的內建快照，也不要讓數字往回走。
   若線上少了某些字、卻又多了快照沒有的字，那就不是舊版，照用線上。 */
function liveOlderThanSnapshot(db){
  if (!(SNAP.chars > db.length)) return false;
  var have = snapCharSet();
  /* 字典的 key 有多音節詞（如「如何」「如何然」）與兩字合收的條目（如「介兒」），
     所以逐字比對；字串一律用 Array.from 按碼點切，才不會把擴展 B 區的字拆成代理對。 */
  for (var i=0;i<db.length;i++){
    var cs = Array.from(db[i].character);
    for (var j=0;j<cs.length;j++) if (!have[cs[j]]) return false;
  }
  return true;
}

/* ---------- 渲染與語言切換 ---------- */
function renderAll(){
  assignReps(); buildUnits();
  RH_CHARS = [];              /* 資料源換了（線上／內建快照），韻→字的快取要重算 */
  renderChrome(); renderRhymeTable(); renderUnitTable(); renderYuntu(); renderBars();
  fixMods(document.body);
}

function applyLang(l){
  if (!I18N[l]) l = 'wu';
  LANG = l;
  document.documentElement.lang = (l === 'wu') ? 'zh-Hant' : l;
  /* 已展開的韻圖要重繪（文字換語言） */
  var opened = [];
  RH.forEach(function(rh, ri){ if (rhOpen[ri]) opened.push(ri); });
  RH.forEach(function(rh, ri){
    var box = document.getElementById('rhb-'+ri);
    if (box){ box.dataset.done = '0'; box.innerHTML = ''; }
  });
  document.querySelectorAll('#langMenu button').forEach(function(b){
    b.classList.toggle('cur', b.dataset.lang === l);
  });
  renderAll();
  opened.forEach(function(ri){ expandRhyme(ri, true); });
  if (document.getElementById('modal').classList.contains('on')) reopenModal();
  /* 同韻查詢與音系浮窗的文字也要跟著換語言 */
  renderSameChrome();
  if (SAME_LAST) doSame();
  if (document.getElementById('phon').classList.contains('on')) openPhon();
}

/* 先把內建快照渲染出來，再嘗試聯網更新；語言同步判定 */
loadFromSnapshot();
buildUnits(); assignReps();
if (!window.__yuntuLang.ready(applyLang)) applyLang('wu');
sync();

/* 同韻查詢：輸入框按 Enter 直接查；兩個浮層點背景關閉 */
(function(){
  var box = document.getElementById('srInput');
  if (box) box.addEventListener('keydown', function(e){
    if (e.key === 'Enter'){ e.preventDefault(); doSame(); }
  });
  [['same', closeSame], ['phon', closePhon]].forEach(function(pair){
    var el = document.getElementById(pair[0]);
    if (el) el.addEventListener('click', function(e){
      if (e.target === el) pair[1]();
    });
  });
})();
"""

HTML = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>__CSS__</style>
<script>__LANGDETECT__</script>
</head><body>
<div class="wrap">

<div class="topbar">
<button class="lang-btn" id="btnSame" onclick="openSame()"></button>
<div class="lang-switcher">
<button class="lang-btn" id="langBtn" onclick="toggleLangMenu()" aria-haspopup="true">
<span id="langCur">漢語</span><span class="lang-caret" aria-hidden="true">▼</span></button>
<div class="lang-menu" id="langMenu">
<button data-lang="wu" onclick="pickLang('wu')">漢語</button>
<button data-lang="en" onclick="pickLang('en')">English</button>
<button data-lang="ja" onclick="pickLang('ja')">日本語</button>
</div>
</div>
</div>

<header class="top">
<h1 id="i-h1"></h1>
<p class="phonintro" id="i-phonintro"></p>
<p class="sub" id="i-based"></p>
<div class="syncbar builtin" id="syncbar"></div>
<div class="tools">
<button id="btnSync" onclick="sync()"></button>
<button id="btnAll" onclick="return allRhymes(!ALLOPEN)"></button>
<button id="btnTop" onclick="window.scrollTo({top:0,behavior:'smooth'})"></button>
<button id="btnE" onclick="return toggleEmpty()"></button>
</div>
</header>

<section>
<h2 id="i-sec-overview"></h2>
<div class="stats" id="i-stats"></div>
<div class="tw" style="display:inline-block;padding:0;margin:8px 0 2px;width:auto">
<table class="units" style="width:auto" id="i-tonetable"></table>
</div>
<p class="broadnote" id="i-tonenote"></p>
<ol class="prose" id="i-ovlist"></ol>
</section>

<section>
<h2 id="i-sec-rhymes"></h2>
<div class="tw" id="tbl-rhymes"></div>
<p class="sub" id="i-rt-note" style="margin-top:8px"></p>
</section>

<section>
<h2 id="i-sec-units"></h2>
<div class="tw" style="max-height:640px" id="tbl-units"></div>
<p class="sub" id="i-ut-note" style="margin-top:8px"></p>
</section>

<section>
<h2 id="i-sec-yuntu"></h2>
<p class="broadnote" id="i-yt-note"></p>
<div id="sections"></div>
</section>

<section>
<h2 id="i-sec-bars"></h2>
<div class="bars" id="bars"></div>
<p class="sub" id="i-barsnote"></p>
</section>

<section>
<h2 id="i-sec-notes"></h2>
<div class="prose" id="i-notelist"></div>
</section>

<footer id="i-footer"></footer>
</div>

<div id="modal"><div class="mbox">
<div class="mhead"><b id="mtitle"></b><span class="ms" id="msub"></span>
<button class="mback" id="mback" style="display:none"></button>
<button id="mclose"></button></div>
<div class="mbody" id="mbody"></div>
</div></div>
<div id="tip"></div>

<div id="same"><div class="samebox">
<div class="samehead">
<b id="i-sr-title"></b>
<span class="ss" id="i-sr-sub"></span>
<button id="srClose" onclick="closeSame()"></button>
</div>
<div class="samebody">
<div class="sameform">
<input id="srInput" type="text" maxlength="8" autocomplete="off" spellcheck="false">
<button id="srGo" onclick="doSame()"></button>
</div>
<p class="samehint" id="i-sr-hint"></p>
<p class="sameonly" id="i-sr-only"></p>
<div id="sameout"></div>
</div>
</div></div>

<div id="phon"><div class="phon-panel">
<button class="phon-close" id="phonClose" onclick="closePhon()"></button>
<div id="phonBody"></div>
</div></div>

<script id="phon-wu" type="text/html">__PHON_WU__</script>
<script id="phon-en" type="text/html">__PHON_EN__</script>
<script id="phon-ja" type="text/html">__PHON_JA__</script>

<script id="scheme" type="application/json">__SCHEME__</script>
<script id="snapshot" type="application/json">__SNAP__</script>
<script id="i18n" type="application/json">__I18N__</script>
<script id="gloss" type="application/json">__GLOSS__</script>
<script>__JS__</script>
</body></html>"""

OUT = (HTML.replace("__CSS__", CSS)
           .replace("__LANGDETECT__", LANGDETECT)
           .replace("__SCHEME__", SCHEME_JSON)
           .replace("__SNAP__", SNAP_JSON)
           .replace("__I18N__", I18N_JSON)
           .replace("__GLOSS__", GLOSS_JSON)
           .replace("__PHON_WU__", PHON_WU)
           .replace("__PHON_EN__", PHON_EN)
           .replace("__PHON_JA__", PHON_JA)
           .replace("__JS__", JS)
           .replace("__TITLE__", I18N["wu"]["page_title"]))

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(OUT)
print("written index.html", len(OUT.encode("utf-8")), "bytes (%d chars)" % len(OUT))
