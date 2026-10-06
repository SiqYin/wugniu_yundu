
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

;

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
  document.getElementById('btnSong').textContent = t('btn_song');
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
          + (shu?'#e8f0f8':'#fdeeea')+'">'+esc(shu?t('kind_shu'):t('kind_ru'))+'</td></tr>';
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
    link: '<a href="'+SCHEME.dict_url+'?lang='+LANG+'" target="_blank">'+esc(t('link_dict'))+'</a>'
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
        + '<td class="mi">'+esc(c.ini||'∅')+'<br><span style="font-size:10.5px;color:#7a99b5">'
        + SCHEME.initials[c.ini][2]+'</span></td>'
        + '<td class="mp">'+esc(c.syl)+'<br><span style="font-size:11px;color:#7a99b5">['
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
        + '<br><span style="font-size:10.5px;color:#7a99b5">'+SCHEME.initials[c.ini][2]
        + '</span></td><td class="mp">'+esc(c.syl)
        + '<br><span style="font-size:11px;color:#7a99b5">['
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
var S2T = null, S2T_P = null, SAME_LAST = '', SAME_TOKEN = 0;
function loadS2T(){
  if (!S2T_P){
    S2T_P = fetch('s2t.json', {cache:'force-cache'}).then(function(r){
      if (!r.ok) throw new Error('HTTP '+r.status);
      return r.json();
    }).then(function(j){ S2T = j || {}; return S2T; })
      .catch(function(){ S2T = {}; return S2T; });   /* 抓不到就只支援繁體輸入 */
  }
  return S2T_P;
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
function closeSame(){ closeCharInfo(); document.getElementById('same').classList.remove('on'); return false; }

function doSame(){
  var raw = (document.getElementById('srInput').value || '').trim();
  SAME_LAST = raw;
  var out = document.getElementById('sameout');
  var cs = Array.from(raw).filter(function(c){ return /\S/.test(c); });
  if (!cs.length){ out.innerHTML = '<div class="srerr">'+esc(t('sr_empty'))+'</div>'; return false; }
  if (cs.length > 8){ out.innerHTML = '<div class="srerr">'+esc(t('sr_max'))+'</div>'; return false; }
  /* 簡繁對照表是非同步抓的，必須等它到位才能展開簡體字，否則第一次查簡體字會誤報「查不到」 */
  var token = ++SAME_TOKEN;
  out.innerHTML = '<div class="srerr">'+esc(t('sr_loading'))+'</div>';
  loadS2T().then(function(){
    if (token !== SAME_TOKEN) return;          /* 期間又查了別的，這次作廢 */
    renderSame(raw, out);
  });
  return false;
}

function renderSame(raw, out){
  closeCharInfo();
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
            + '</div><div class="srchars">'+charSpans(chs, ri)+'</div></div>';
    });
    html += '</div>';
  });
  out.innerHTML = (any ? '<p class="cphint">'+esc(t('cp_hint'))+'</p>' : '')
                + (html || '<div class="srerr">'+esc(t('sr_empty'))+'</div>');
  fixMods(out);
}

/* ---------- 歌詞押韻查詢（同韻查詢 ＋ 近韻相押） ----------
   近韻相押：有星韻讀音接近，勒勿同人个語感裡向可能通押——有人押，有人勿押。
   前四組（八陌／打黨／麻模／資支）是固定个兩韻組合，勾一个就當伊拉相押。
   第五組「微余仙侵雲雪月」一韻一格：勾起來个韻混作一組、彼此相押；
   沒勾个就各論各个。無論勾著啥，結果一律仍按韻分列。 */
var NEAR_FIX = [['八','陌'],['打','黨'],['麻','模'],['資','支']];
var NEAR_CX  = ['微','余','仙','侵','雲','雪','月'];
var NEAR_ON  = {};                       /* 'f0'..'f3' -> true：前四組勾了沒 */
var NEAR_SEL = {};                       /* '微' -> true：第五組勾起來个韻 */
var SONG_LAST = '', SONG_TOKEN = 0;
var RH_IX = null;

function rhIndex(){
  if (!RH_IX){ RH_IX = {}; RH.forEach(function(r,i){ RH_IX[r.name] = i; }); }
  return RH_IX;
}

/* 查某一韻時，連帶要列出个韻（含本身） */
function nearSet(name){
  var out = [name], ix = rhIndex(), add = function(n){
    if (ix[n] == null || out.indexOf(n) >= 0) return;
    out.push(n);
  };
  NEAR_FIX.forEach(function(p, i){
    if (!NEAR_ON['f' + i]) return;           /* 沒勾就當勿相押 */
    if (p[0] === name) add(p[1]);
    else if (p[1] === name) add(p[0]);
  });
  if (NEAR_SEL[name]){                       /* 第五組：勾起來个全部混作一組 */
    NEAR_CX.forEach(function(nm){ if (NEAR_SEL[nm]) add(nm); });
  }
  return out;
}

function syncNearBoxes(){
  document.querySelectorAll('#nearrows input.nrcb').forEach(function(b){
    var r = b.dataset.rhyme;
    b.checked = r ? !!NEAR_SEL[r] : !!NEAR_ON['f' + b.dataset.fix];
  });
}
function buildNear(){
  var ix = rhIndex(), html = '';
  NEAR_FIX.forEach(function(p, i){
    html += '<div class="nrrow"><label><input type="checkbox" class="nrcb" data-fix="'+i
          + '"><span class="nrl">'
          + esc(rhName(RH[ix[p[0]]]) + '／' + rhName(RH[ix[p[1]]]))
          + '</span></label><span class="nrn">' + esc(t(i < 2 ? 'sg_g_often' : 'sg_g_tend'))
          + '</span></div>';
  });
  /* 第五組：微余仙侵雲雪月，一韻一格 */
  var box = '';
  NEAR_CX.forEach(function(nm){
    box += '<label><input type="checkbox" class="nrcb" data-rhyme="'+esc(nm)+'">'
         + '<span class="nrl">'+esc(nm)+'</span></label>';
  });
  html += '<div class="nrrow nrcx"><div class="nrhd">'
        + '<span class="nrl">'+esc(NEAR_CX.join('／'))+'</span>'
        + '<span class="nrn">'+esc(t('sg_g_mixed'))+'</span></div>'
        + '<div class="nrmx"><div class="cxrow">'+box+'</div>'
        + '<p class="nrtip">'+esc(t('sg_tip'))+'</p></div></div>';
  document.getElementById('nearrows').innerHTML = html;
  syncNearBoxes();
}
function clearNear(){
  NEAR_ON = {}; NEAR_SEL = {}; syncNearBoxes();
  if (SONG_LAST) doSong();
}

function renderSongChrome(){
  document.getElementById('btnSong').textContent = t('btn_song');
  document.getElementById('i-sg-title').textContent = t('sg_title');
  document.getElementById('i-sg-sub').textContent = t('sg_sub');
  document.getElementById('sgInput').placeholder = t('sg_ph');
  document.getElementById('sgGo').textContent = t('sg_go');
  document.getElementById('i-sg-hint').textContent = t('sg_hint');
  document.getElementById('i-sg-near').textContent = t('sg_near');
  document.getElementById('i-sg-nearnote').textContent = t('sg_nearnote');
  document.getElementById('sgClear').textContent = t('sg_clear');
  document.getElementById('i-sg-only').textContent = t('sg_only');
  document.getElementById('i-sg-help').textContent = t('sg_help');
  document.getElementById('i-sg-helpbody').innerHTML = t('sg_helpbody');
  buildNear();
}
function openSong(){
  loadS2T(); renderSongChrome();
  document.getElementById('song').classList.add('on');
  setTimeout(function(){
    var i = document.getElementById('sgInput');
    if (i) i.focus();
  }, 40);
  return false;
}
function closeSong(){ closeCharInfo(); document.getElementById('song').classList.remove('on'); return false; }

function doSong(){
  var raw = (document.getElementById('sgInput').value || '').trim();
  SONG_LAST = raw;
  var out = document.getElementById('songout');
  var cs = Array.from(raw).filter(function(c){ return /\S/.test(c); });
  if (!cs.length){ out.innerHTML = '<div class="srerr">'+esc(t('sr_empty'))+'</div>'; return false; }
  if (cs.length > 8){ out.innerHTML = '<div class="srerr">'+esc(t('sr_max'))+'</div>'; return false; }
  var token = ++SONG_TOKEN;
  out.innerHTML = '<div class="srerr">'+esc(t('sr_loading'))+'</div>';
  loadS2T().then(function(){
    if (token !== SONG_TOKEN) return;
    renderSong(raw, out);
  });
  return false;
}

/* 一個韻一截；本韻照讀音資訊，近韻另外標出來 */
function readBlock(ri, group, isNear){
  var chs = rhymeChars(ri), syls = [], seen = {};
  (group || []).forEach(function(cc){
    if (seen[cc.syl]) return;
    seen[cc.syl] = 1;
    syls.push('<code>'+esc(cc.syl)+'</code> ['+esc(plainMod(cc.ipa.join('/')))+']');
  });
  return '<div class="srread'+(isNear ? ' near' : '')+'"><div class="hd">'
       + (isNear ? '<i class="ntag">'+esc(t('sg_tag'))+'</i>' : '')
       + '<b>'+esc(rhName(RH[ri]))+'</b>'
       + (syls.length ? ' ・ ' + syls.join(' ・ ') : '')
       + ' ・ ' + esc(n('sr_words', {n: chs.length}))
       + '</div><div class="srchars">'+charSpans(chs, ri)+'</div></div>';
}

function renderSong(raw, out){
  closeCharInfo();
  var html = '', any = false, ix = rhIndex();
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
    var byR = {}, order = [];
    rs.forEach(function(cc){
      if (!byR[cc.ri]){ byR[cc.ri] = []; order.push(cc.ri); }
      byR[cc.ri].push(cc);
    });
    order.sort(function(a,b){ return a - b; });
    var own = {}, extra = [];
    order.forEach(function(ri){ own[ri] = 1; });
    order.forEach(function(ri){
      nearSet(RH[ri].name).forEach(function(nm){
        var j = ix[nm];
        if (j == null || own[j] || extra.indexOf(j) >= 0) return;
        extra.push(j);
      });
    });
    extra.sort(function(a,b){ return a - b; });
    order.forEach(function(ri){ html += readBlock(ri, byR[ri], false); });
    extra.forEach(function(ri){ html += readBlock(ri, null, true); });
    html += '</div>';
  });
  out.innerHTML = (any ? '<p class="cphint">'+esc(t('cp_hint'))+'</p>' : '')
                + (html || '<div class="srerr">'+esc(t('sr_empty'))+'</div>');
  fixMods(out);
}

/* ---------- 結果裡的字：拼音標注 ＋ 點擊看字音 ----------
   標注：只有多音字（全圖有兩個以上小韻）才在字的上方標出**它在本韻裡的讀音**；
   只標拼音，不加備註和音標——目的就是讓使用者看清是哪一個音壓得上。
   點擊：只有點了才顯示字音卡（韻、呼、韻母、聲母、聲調、拼音、音值），不點不顯示。 */
var CH_IX = null, CI_ON = null;
function charCells(ch){
  if (!CH_IX){
    CH_IX = {};
    CELLS.forEach(function(c){
      c.chars.forEach(function(x){ (CH_IX[x] = CH_IX[x] || []).push(c); });
    });
  }
  return CH_IX[ch] || [];
}
function cellsInRhyme(ch, ri){
  return charCells(ch).filter(function(c){ return c.ri === ri; });
}
/* 這個字在本韻裡的讀音（拼音，去重） */
function rhymePys(ch, ri){
  var seen = {}, out = [];
  cellsInRhyme(ch, ri).forEach(function(c){
    if (!seen[c.syl]){ seen[c.syl] = 1; out.push(c.syl); }
  });
  return out;
}
/* 全圖有兩個以上讀音（＝多音字）才標，其餘不標 */
function charPy(ch, ri){
  return charCells(ch).length > 1 ? rhymePys(ch, ri).join('/') : '';
}
function charSpans(chs, ri){
  var h = '';
  chs.forEach(function(ch){
    var py = charPy(ch, ri);
    h += '<span class="sc" data-ri="' + ri + '"'
       + (py ? ' data-py="' + esc(py) + '"' : '') + '>' + esc(ch) + '</span>';
  });
  return h;
}
/* 韻母音值：取自該呼位的韻母表（＝音系表的值） */
function finalIpa(ri, hu, fin){
  var hus = RH[ri].hus;
  for (var i = 0; i < hus.length; i++){
    if (hus[i].hu !== hu) continue;
    for (var j = 0; j < hus[i].finals.length; j++)
      if (hus[i].finals[j].final === fin) return hus[i].finals[j].ipa;
  }
  return '';
}
function closeCharInfo(){
  var box = document.getElementById('chinfo');
  if (box) box.classList.remove('on');
  if (CI_ON){ CI_ON.classList.remove('on'); CI_ON = null; }
}
function ciRow(k, v){ return '<dt>' + esc(k) + '</dt><dd>' + v + '</dd>'; }
function showCharInfo(sp){
  var ch = sp.textContent, ri = +sp.dataset.ri, box = document.getElementById('chinfo');
  if (!box) return;
  var cs = cellsInRhyme(ch, ri);
  if (!cs.length){
    box.innerHTML = '<div class="cih"><b>' + esc(ch) + '</b></div><div class="cir">'
                  + esc(t('cp_none')) + '</div>';
  } else {
    var html = '<div class="cih"><b>' + esc(ch) + '</b><span>' + esc(rhName(RH[ri]))
             + '</span><button type="button" id="ciClose">✕</button></div>';
    cs.forEach(function(c){
      html += '<div class="cir"><dl">'
            + ciRow(t('cp_hu'), esc(huFull(c.hu)))
            + ciRow(t('cp_fin'), '<code>' + esc(c.fin) + '</code> ['
                     + esc(plainMod(finalIpa(c.ri, c.hu, c.fin))) + ']')
            + ciRow(t('cp_ini'), c.ini ? esc(c.ini) + ' [' + esc(SCHEME.initials[c.ini][2]) + ']'
                                       : '∅')
            + ciRow(t('cp_tone'), n('cp_toneval', {name: t('tone_' + c.tone),
                     val: SCHEME.tone_info[c.tone][1]}))
            + ciRow(t('cp_syl'), '<code>' + esc(c.syl) + '</code>')
            + ciRow(t('cp_ipa'), '[' + esc(plainMod(c.ipa.join('/'))) + ']')
            + '</dl></div>';
    });
    box.innerHTML = html;
  }
  box.classList.add('on');
  if (CI_ON) CI_ON.classList.remove('on');
  CI_ON = sp; sp.classList.add('on');
  var r = sp.getBoundingClientRect(), b = box.getBoundingClientRect();
  var x = r.left + r.width / 2 - b.width / 2, y = r.bottom + 8;
  x = Math.max(8, Math.min(x, window.innerWidth - b.width - 8));
  if (y + b.height > window.innerHeight - 8) y = Math.max(8, r.top - b.height - 8);
  box.style.left = Math.round(x) + 'px'; box.style.top = Math.round(y) + 'px';
  var cb = document.getElementById('ciClose');
  if (cb) cb.onclick = function(){ closeCharInfo(); };
}

document.addEventListener('click', function(e){
  var sp = e.target.closest('.srchars .sc');
  if (sp){ if (sp === CI_ON) closeCharInfo(); else showCharInfo(sp); return; }
  if (!e.target.closest('#chinfo')) closeCharInfo();

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
  if (e.key === 'Escape'){ closeModal(); closeSame(); closeSong(); closePhon(); }
});
/* 字音卡是固定定位的，浮層一捲動就會跟字分家，索性關掉 */
window.addEventListener('scroll', function(){ closeCharInfo(); }, true);
window.addEventListener('resize', function(){ closeCharInfo(); });

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
  /* 同韻查詢、歌詞押韻查詢與音系浮窗的文字也要跟著換語言 */
  renderSameChrome();
  renderSongChrome();
  if (SAME_LAST) doSame();
  if (SONG_LAST) doSong();
  if (document.getElementById('phon').classList.contains('on')) openPhon();
}

/* 先把內建快照渲染出來，再嘗試聯網更新；語言同步判定 */
loadFromSnapshot();
buildUnits(); assignReps();
if (!window.__yuntuLang.ready(applyLang)) applyLang('wu');
sync();

/* 從「蘇滬混合腔字音查詢」的「歌詞押韻查詢」按鈕跳過來時，直接開浮層。
   網址寫 ?song=1（或 #song）即可，不必先載入頁面再手動點按鈕。 */
if (/[?&]song\b/i.test(location.search) || /^#song$/i.test(location.hash)) openSong();

/* 同韻查詢、歌詞押韻查詢：輸入框按 Enter 直接查；三個浮層點背景關閉 */
(function(){
  [['srInput', doSame], ['sgInput', doSong]].forEach(function(p){
    var box = document.getElementById(p[0]);
    if (box) box.addEventListener('keydown', function(e){
      if (e.key === 'Enter'){ e.preventDefault(); p[1](); }
    });
  });
  /* 近韻相押个勾選：改動就重出結果 */
  var nr = document.getElementById('nearrows');
  if (nr) nr.addEventListener('change', function(e){
    var b = e.target.closest('input.nrcb');
    if (!b) return;
    var r = b.dataset.rhyme;
    if (r){ if (b.checked) NEAR_SEL[r] = 1; else delete NEAR_SEL[r]; }
    else { var k = 'f' + b.dataset.fix;
           if (b.checked) NEAR_ON[k] = 1; else delete NEAR_ON[k]; }
    if (SONG_LAST) doSong();
  });
  [['same', closeSame], ['song', closeSong], ['phon', closePhon]].forEach(function(pair){
    var el = document.getElementById(pair[0]);
    if (el) el.addEventListener('click', function(e){
      if (e.target === el) pair[1]();
    });
  });
})();
