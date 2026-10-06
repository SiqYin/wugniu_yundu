# -*- coding: utf-8 -*-
"""韻圖介面文字的三語詞表：漢語（繁體中文，預設）／English／日本語。

規則：
  * 只翻譯「介面文字」——標題、欄名、按鈕、說明文字。
  * 漢字本身（韻目、代表字、轄字）、拼音、音標一律不譯。
  * 中古來源雖是說明文字，但含大量韻目字，故另行逐韻譯出（見 GLOSS）。
"""

WU = {
 "page_title": "蘇滬混合腔韻圖",
 "h1": "蘇滬混合腔韻圖",
 "tagline": "按今音韻基分韻，開合齊撮逐位列出，一位一圖",
 "based_on": "依據 SiqYin 的 {dict}（字音查詢）與 {rime} 編製。本頁收字 <b>{chars}</b>，"
             "讀音條目 <b>{records}</b>，合法音節（含聲調）<b>{syll}</b>。",
 "link_dict": "蘇滬混合腔線上字典",
 "link_rime": "RIME 輸入方案",
 "btn_sync": "重新同步線上字音庫",
 "btn_expand": "全部展開韻圖",
 "btn_collapse": "全部收合韻圖",
 "btn_top": "回到頂端",
 "btn_hide": "隱藏全空的聲母行",
 "btn_show": "顯示全空的聲母行",
 "sync_loading": "正在讀取線上字音庫……",
 "sync_ok": "已同步線上字音庫（{link}）：收字 <b>{chars}</b>，讀音 <b>{records}</b> 條，"
            "合法音節 <b>{syll}</b> 個{stamp}。字音查詢那邊一有更新，重新整理本頁就會跟著更新。",
 "sync_ok_stamp": "；線上資料檔最後更新於 {t}",
 "sync_fail": "目前連不上線上字音庫（{err}），顯示的是頁面內建的離線快照"
              "（{chars} 字 / {records} 條讀音）。連上網路後按下面的「重新同步」即可取得最新字音。",

 "sec_overview": "音系總覽",
 "sec_rhymes": "分韻總表",
 "sec_units": "各呼位總覽",
 "sec_yuntu": "韻圖",
 "sec_bars": "各呼位字數",
 "sec_notes": "補充說明",

 "st_initials": "聲母", "st_finals": "韻母", "st_rhymes": "韻（按韻基分）",
 "st_units": "呼位（韻 × 呼）", "st_tones": "聲調（{shu} 舒 {ru} 入）", "st_cells": "小韻格位",

 "th_no": "調號", "th_cls": "調類", "th_val": "調值", "th_kind": "舒／入",
 "th_class": "類",
 "rt_hu4": "四呼（韻母・音值・小韻數・字數）",
 "kind_shu": "舒聲", "kind_ru": "入聲",
 "tone_1": "陰平", "tone_2": "陽平", "tone_3": "陰上", "tone_5": "陰去",
 "tone_6": "陽上去", "tone_7": "陰入", "tone_8": "陽入",
 "tone_note": "蘇滬混合腔沒有陽上和陽去的分別，這兩類現在的讀音合併成調 6「陽上去」，"
              "所以總共只有 {total} 個聲調。",

 "ov1": "<b>分韻只看今音的韻基。</b>韻基就是主元音加韻尾。韻基不同，就算中古時屬於同一韻攝，"
        "也要分成不同的韻；韻基相同，就算中古時來自不同韻攝，也歸為同一個韻。"
        "所以 <code>i[iᶽ]</code> 和 <code>iu[y]</code> 分成微韻和魚韻，"
        "<code>y[ɿ]</code> 和 <code>yu[ʮ]</code> 分成資韻和支韻；"
        "入聲的 <code>eq[əʔ]</code>、<code>ueq[uəʔ]</code>（主元音是 <code>ə</code>）和 "
        "<code>iq[iɪʔ]</code>（主元音是 <code>ɪ</code>）分成質韻和雪韻，"
        "<code>iuq[yɪʔ]</code> 另立為月韻。"
        "合起來一共 <b>{rhymes} 個韻</b>。",
 "ov2": "<b>開合齊撮逐位列出。</b>一個韻裡面佔了幾個呼，就列出幾個呼位，"
        "<b>一個呼位畫一張圖</b>。全部共 <b>{units} 個呼位</b>，其中開口 {n_kai} 位、"
        "合口 {n_he} 位、齊齒 {n_qi} 位、撮口 {n_cuo} 位、特例 {n_te} 位。"
        "四個呼都齊全的只有「八」韻一個；只佔一個呼位的有十個韻——"
        "模（合）、魚（撮）、支（撮）、資（齊）、微（齊）、仙（齊）、侵（齊）、雲（撮）、"
        "雪（齊）、月（撮）。",
 "ov3": "<b>韻目代表字都經過核對。</b>每個韻的名字，都取一個本韻裡真的有這個讀音的字，"
        "而且由程式逐一驗證過。例如「談」現在讀 <code>de6</code>〔dᴇ〕，屬於灰韻，"
        "所以不再拿它來當 －n 韻的韻目；「歌」現在讀 <code>ku1</code>〔kuᵝ〕，屬於模韻；"
        "「支」讀 <code>tsyu1</code>〔tsʮ〕，正好用來當撮口擦化韻的韻目；"
        "「雪」讀 <code>siq7</code>〔siɪʔ〕是齊齒，「月」讀 <code>yuq8</code>〔yɪʔ〕是撮口，"
        "各如其分。總表「韻目取字」那一欄的小字，就是這個韻目字的實際讀音。",
 "ov4": "<b>四呼怎麼判定。</b>有 <code>u</code> 介音或主元音是 <code>u</code> 的算合口，"
        "有 <code>i</code> 介音或主元音是 <code>i</code> 的算齊齒，"
        "有 <code>yu</code> 介音或主元音是 <code>yu</code>（〔y〕）的算撮口，其餘算開口。"
        "<b>擦化元音按它原本的元音來算</b>：〔ɿ〕是〔i〕的擦化，所以整個韻都是齊齒；"
        "〔ʮ〕是〔y〕的擦化，所以整個韻都是撮口。",
 "ov5": "<b>舒聲韻和入聲韻分開。</b><b>舒聲韻是聲調 1、2、3、5、6</b>，"
        "<b>入聲韻是聲調 7、8</b>。舒聲韻內部不再分平上去，一張圖橫向列出五個舒聲調，"
        "這個韻平上去的字都在同一張圖裡；入聲韻單獨列成一區，收喉塞尾 <code>[ʔ]</code>，"
        "圖裡只列陰入、陽入兩個調。全圖 {rhymes} 個韻，"
        "沒有任何一個韻同時混有舒聲和入聲的字。",
 "ov6": "<b>特例四韻。</b><b>嘸</b><code>m</code>〔m̩〕、<b>唔</b><code>n</code>〔n̩〕、"
        "<b>五</b><code>ng</code>〔ŋ̩〕是成音節鼻音，<b>而</b><code>er</code>〔əl〕是捲舌元音；"
        "這四個韻<b>不分開合齊撮</b>，各只有一個呼位，所以另外列在入聲韻之後。",
 "ov7": "<b>每一格就是一個小韻，也就是一個合法音節。</b>格子上方是代表字，下方是拼音，"
        "滑鼠移到格子上會顯示這個小韻的全部字。蘇滬混合腔的 <b>{syll} 個合法音節全部在圖中</b>，"
        "一格一韻，不會重複安放。",
 "ov8": "<b>每個呼位都標了小韻數和字數，兩個數字都能點。</b>"
        "點<b>小韻數</b>會打開這個呼位的小韻一覽，再點其中任何一個小韻，就能看到那個小韻的全部轄字；"
        "點<b>字數</b>則直接列出這個呼位的全部漢字（按聲調分組）。"
        "分韻總表、各呼位總覽和每張韻圖的標題上都有這兩個按鈕。",
 "ov9": "<b>韻圖預設收合。</b>下面的韻圖按韻排列，預設只顯示韻目與統計，"
        "點標頭即可展開該韻的圖，再點一下收合；要一次全開可以按上方的「{btn_expand}」。",

 "rt_note": "「韻基」是這個韻的主元音和韻尾；「呼位數」是這個韻佔了四呼中的幾位；"
            "「小韻合計」是這個韻實際有的合法音節（含聲調）數量；"
            "「字數合計」是這個韻底下所有漢字的去重總數。"
            "「類」欄：<b>陰</b>＝陰聲韻，<b>陽</b>＝陽聲韻，<b>入</b>＝入聲韻，<b>特</b>＝特例韻；"
            "陰聲韻和陽聲韻都屬於舒聲韻。每一格裡的「<b>N 小韻</b>」和「<b>N 字</b>」按鈕都可以點："
            "點小韻數會列出該呼位的全部小韻（再點其中一個小韻，即可看到它的全部轄字），"
            "點字數則直接列出該呼位的全部漢字。",
 "ut_note": "逐條列出每個呼位：韻目、呼、韻母、音值、小韻數與字數。"
            "「小韻數」與「字數」都是按鈕，點下去分別看小韻一覽與全部漢字。",

 "cls_yin": "陰", "cls_yang": "陽", "cls_ru": "入", "cls_te": "特",
 "div_shu": "舒聲韻　聲調 1・2・3・5・6　平上去不分開，同一個韻的平上去字都在同一張圖裡",
 "div_ru": "入聲韻　聲調 7・8　收喉塞尾 [ʔ]，單獨列出",
 "div_te": "特例四韻　不分開合齊撮（成音節鼻音 m／n／ng 與捲舌元音 er）",
 "div_shu_short": "舒聲韻", "div_ru_short": "入聲韻", "div_te_short": "特例四韻（不分四呼）",

 "hu_kai": "開口", "hu_he": "合口", "hu_qi": "齊齒", "hu_cuo": "撮口", "hu_te": "特例",
 "hu_suffix": "呼",

 "yt_shu": "舒聲韻", "yt_yin": "陰聲韻", "yt_yang": "陽聲韻",
 "yt_ru": "入聲韻", "yt_te": "特例四韻",
 "yt_shu_note": "舒聲韻指聲調是 1、2、3、5、6 的字，也就是不帶喉塞尾的音節。"
                "<b>同一個韻的平、上、去不再分開</b>：下面每一張圖橫向列出五個舒聲調，"
                "這個韻平上去的字全部收在同一張圖裡。每張圖標題上的「N 字」都可以點，"
                "點開就能看到這個呼位底下的全部漢字。",
 "yt_yin_note": "沒有韻尾（開音節）", "yt_yang_note": "鼻音韻尾或鼻化",
 "yt_ru_note": "入聲韻和舒聲韻分開排列，收喉塞尾 <code>[ʔ]</code>，圖裡只列陰入、陽入兩個調。"
               "入聲韻同樣有開、合、齊、撮的差別，所以也逐位畫圖。"
               "<code>iq</code>〔ɪʔ〕屬<b>雪</b>韻（全韻齊齒），<code>iuq</code>〔yɪʔ〕屬<b>月</b>韻"
               "（全韻撮口），所以各立一韻。",
 "yt_te_note": "這四個韻的聲調屬於舒聲（1、2、3、5、6），但元音自成一套，<b>不分開合齊撮</b>，"
               "所以另外列成一區：<code>m</code>〔m̩〕、<code>n</code>〔n̩〕、<code>ng</code>〔ŋ̩〕"
               "是成音節鼻音，<code>er</code>〔əl〕是捲舌元音。四個韻各只有一個呼位，"
               "圖裡仍按五個舒聲調列字。",
 "rh_open": "展開", "rh_close": "收合",
 "rh_label": "韻目取字", "rh_src": "中古可能的來源（僅供參考）",
 "yt_corner": "聲母＼調",
 "grp_唇音": "唇音", "grp_舌音": "舌音", "grp_牙音": "牙音",
 "grp_腭音": "腭音", "grp_齒音": "齒音", "grp_喉音": "喉音",

 "lbl_core": "韻基", "lbl_hu": "呼位", "lbl_sys": "小韻", "lbl_chars": "字數",
 "word_rhyme": "韻", "word_sys": "小韻", "word_chars": "字", "word_char": "字",

 "bars_note": "字數最多的 24 個呼位。",

 "md_back": "‹ 返回小韻一覽", "md_close": "關閉（Esc）",
 "md_hint_sys": "下面是「<b>{rhyme}{hu}</b>」（{fin} 〔{ipa}〕）底下的全部小韻，"
                "共 <b>{nsys} 個</b>。點任何一列，就能看到那個小韻的全部轄字。",
 "md_tone_head": "{name}<small>調 {no}（{val}）・{nsys} 個小韻 ・共 {nchars} 字</small>",
 "md_rep": "代表字", "md_allchars": "全部轄字",
 "md_sys_sub": "{fin} [{ipa}] ・ 共 {nchars} 個字 ・ {nsys} 個小韻"
               "（同一個字在本呼位有兩個讀音時會分別列出）",
 "md_direct_sub": "{nchars} 個字 ・ 點「返回小韻一覽」可回上一層",
 "md_n_chars": "{n} 個字",
 "md_allchars_head": "全部轄字<small>共 {nchars} 個字（{nsys} 個小韻）</small>",
 "md_etc": "…等",

 "footer": "蘇滬混合腔韻圖 ・ 分韻 {rhymes} 個，呼位 {units} 個，韻母 {finals} 個"
           " ・ 字音資料同步自 {link}（SiqYin）",

 "n1": "<b>一、舊稿的「談韻」和「歌韻」用錯了韻目。</b>早先拿「談」當 －n 韻的韻目，"
       "但「談」現在讀 <code>de6</code>〔dᴇ〕，跟「戴」「帶」「來」「海」是同一個韻（灰韻），"
       "名實不符。現在 <code>an／uan／ian</code> 這個韻改用「<b>陽</b>」當韻目："
       "陽讀 <code>yan2</code>〔iã〕，正好在它的齊齒位上。同樣地，「歌」現在讀 "
       "<code>ku1</code>〔kuᵝ〕，屬於模韻，所以〔o̝〕這個韻改用「<b>麻</b>」當韻目"
       "（麻讀 <code>mo2</code>），〔uᵝ〕這個韻就用「<b>模</b>」當韻目（模讀 <code>mu2</code>）。",
 "n2": "<b>二、「支」和「資」為什麼要分開。</b>「支」讀 <code>tsyu1</code>〔tsʮ〕，"
       "「資」讀 <code>tsy1</code>〔tsɿ〕，主元音一個是 ʮ、一個是 ɿ，韻基不同，所以各立一韻："
       "支韻整個是撮口，資韻整個是齊齒。同樣地，「微」〔iᶽ〕和「魚」〔y〕也各自立韻，不相統屬。",
 "n3": "<b>三、入聲六韻，以及 iq 和 iuq 為什麼要分開。</b>入聲單獨列出，共六個韻："
       "八〔aʔ〕、陌〔ɑʔ〕、質〔əʔ〕、雪〔ɪʔ〕、月〔yɪʔ〕、屋〔oʔ〕。"
       "<b><code>iq</code>〔iɪʔ〕歸「雪」韻（整個韻都是齊齒），"
       "<code>iuq</code>〔yɪʔ〕另立「月」韻（整個韻都是撮口）</b>。"
       "理由是：這兩個韻母的主元音是 <code>ɪ</code>，跟質韻的 <code>eq</code>〔əʔ〕、"
       "<code>ueq</code>〔uəʔ〕（主元音是 <code>ə</code>）明顯不同，按「韻基相同才同韻」的原則，"
       "不能跟質韻混在一起；而 iq 只有齊齒、iuq 只有撮口，所以各自立韻，一個韻一個呼位。"
       "韻目也很貼切：「雪」讀 <code>siq7</code>〔siɪʔ〕，「月」讀 <code>yuq8</code>〔yɪʔ〕。"
       "（<code>iuq</code> 的音值以前誤標成〔yeʔ〕，現在已經改正為〔yɪʔ〕。）",
 "n4": "<b>四、陽韻齊齒位的 iã／iɛ̃ 是文白異讀。</b>陽韻齊齒的 <code>ian</code> 這個位子，"
       "字典裡同時記了〔iã〕和〔iɛ̃〕兩種音值，例如「羊」讀〔iã〕、「良」讀〔liɛ̃〕。"
       "這是文讀和白讀的差別，韻基沒有變，所以仍然算同一個韻、同一個呼位。",
 "n5": "<b>五、特例四韻是怎麼來的。</b>嘸 <code>m</code>〔m̩〕、唔 <code>n</code>〔n̩〕、"
       "五 <code>ng</code>〔ŋ̩〕、而 <code>er</code>〔əl〕這四個韻，聲調屬於舒聲，"
       "但元音自成一套，沒有介音可言，<b>不分開合齊撮</b>，所以另外歸為「特例」一類，"
       "各只有一個呼位，不跟四呼混在一起列。",
 "n6": "<b>六、少數沒有收進圖裡的條目。</b>字典裡的 <code>ba</code>「吧」、<code>kha</code>「快」、"
       "<code>don</code>「丼」三條沒有標聲調，另外「如何」「如何然」兩條是多音節詞，"
       "都不是單音節的合法音節，所以不立格子；"
       "其餘 <b>{syll} 個合法音節全部收進圖裡</b>。",
 "n7": "<b>七、中古來源只是參考。</b>每一韻的「中古可能的來源」那一欄，是為了方便跟傳統韻書對讀而設的。"
       "同一個韻常常同時收了幾個不同韻攝的字（例如泰韻兼收麻韻見系，灰韻兼收止攝合口），"
       "本圖分韻一律以今音韻基為準，不依中古韻攝。",
 "n8": "<b>八、本頁的字音會跟著線上字音庫更新。</b>本頁開啟時會即時讀取"
       "「蘇滬混合腔字音查詢」的資料檔（<code>data/DB_suhu.json</code>），在瀏覽器裡重新分韻排圖。"
       "所以字音查詢那邊新增字或是補上讀音之後，重新整理本頁就會看到最新的字。"
       "如果連不上網路，頁面會改用內建的離線快照（<b>{chars}</b> 字），"
       "並在上方顯示提示；連上網路後按「重新同步線上字音庫」即可。",
 "n9": "<b>九、字型。</b>本頁預設使用<b>霞鶩文楷</b>（LXGW WenKai）顯示，因為字典收了大量生僻字，"
       "一般系統字型顯示不出來。字型已子集化後隨頁面一起提供，分「核心字集」與「完整字集」兩級，"
       "正常只會下載前者（約 2 MB）。",

 "lang_label": "語言", "lang_wu": "漢語", "lang_en": "English", "lang_ja": "日本語",
}

EN = {
 "page_title": "Su–Hu Mixed Wu Rhyme Chart",
 "h1": "Su–Hu Mixed Wu Rhyme Chart",
 "tagline": "Rhymes divided by modern rhyme base · the four divisions listed slot by slot · one chart per slot",
 "based_on": "Compiled from SiqYin's {dict} and the {rime}. This page contains "
             "<b>{chars}</b> characters, <b>{records}</b> readings, and <b>{syll}</b> valid syllables (tones included).",
 "link_dict": "Su–Hu Mixed Wu online dictionary",
 "link_rime": "Rime input scheme",
 "btn_sync": "Re-sync the online reading database",
 "btn_expand": "Expand all rhyme charts",
 "btn_collapse": "Collapse all rhyme charts",
 "btn_top": "Back to top",
 "btn_hide": "Hide all-empty initial rows",
 "btn_show": "Show all-empty initial rows",
 "sync_loading": "Loading the online reading database…",
 "sync_ok": "Synced with the online reading database ({link}): <b>{chars}</b> characters, "
            "<b>{records}</b> readings, <b>{syll}</b> valid syllables{stamp}. "
            "Whenever the lookup site is updated, reloading this page brings the changes in.",
 "sync_ok_stamp": "; the online file was last updated on {t}",
 "sync_fail": "The online reading database cannot be reached ({err}), so the built-in offline "
              "snapshot is being shown ({chars} characters / {records} readings). "
              "Press “Re-sync” once you are back online.",

 "sec_overview": "Phonology at a glance",
 "sec_rhymes": "Rhyme index",
 "sec_units": "All division slots",
 "sec_yuntu": "Rhyme charts",
 "sec_bars": "Characters per division slot",
 "sec_notes": "Notes",

 "st_initials": "initials", "st_finals": "finals", "st_rhymes": "rhymes (by base)",
 "st_units": "division slots", "st_tones": "tones ({shu} unchecked · {ru} checked)",
 "st_cells": "homophone groups",

 "th_no": "Tone", "th_cls": "Register", "th_val": "Value", "th_kind": "Type",
 "th_class": "Class",
 "rt_hu4": "Four divisions (final · IPA · groups · chars)",
 "kind_shu": "Unchecked", "kind_ru": "Checked",
 "tone_1": "Yin Ping", "tone_2": "Yang Ping", "tone_3": "Yin Shang", "tone_5": "Yin Qu",
 "tone_6": "Yang Shang–Qu", "tone_7": "Yin Ru", "tone_8": "Yang Ru",
 "tone_note": "Su–Hu Mixed Wu does not distinguish Yang Shang from Yang Qu; the two have merged "
              "into tone 6, “Yang Shang–Qu”. That leaves {total} tones in all.",

 "ov1": "<b>Rhymes are divided by the modern rhyme base alone.</b> The rhyme base is the main vowel "
        "plus the coda. Different bases are split into different rhymes even if they belonged to the "
        "same rhyme group in Middle Chinese; the same base is one rhyme even if it came from different "
        "Middle Chinese groups. Thus <code>i[iᶽ]</code> and <code>iu[y]</code> split into the "
        "微 and 魚 rhymes, and <code>y[ɿ]</code> and <code>yu[ʮ]</code> into 資 and 支; among the "
        "checked rhymes, <code>eq[əʔ]</code> and <code>ueq[uəʔ]</code> (main vowel <code>ə</code>) "
        "and <code>iq[iɪʔ]</code> (main vowel <code>ɪ</code>) split into 質 and 雪, and "
        "<code>iuq[yɪʔ]</code> is set up as its own rhyme 月. "
        "In total there are <b>{rhymes} rhymes</b>.",
 "ov2": "<b>Open, closed, spread and rounded are listed slot by slot.</b> However many divisions a "
        "rhyme occupies, that many slots are listed, <b>one chart per slot</b>. All told there are "
        "<b>{units} slots</b>: open {n_kai}, closed {n_he}, spread {n_qi}, rounded {n_cuo}, "
        "special {n_te}. Only the 八 rhyme fills all four; ten rhymes have just one slot — "
        "模 (closed), 魚 (rounded), 支 (rounded), 資 (spread), 微 (spread), 仙 (spread), "
        "侵 (spread), 雲 (rounded), 雪 (spread), 月 (rounded).",
 "ov3": "<b>Every rhyme name has been checked.</b> Each rhyme takes its name from a character that "
        "genuinely has that reading in the rhyme, verified one by one by the build script. "
        "談, for instance, is now read <code>de6</code> [dᴇ] and belongs to the 灰 rhyme, so it is no "
        "longer used as the label of the −n rhyme; 歌 is now <code>ku1</code> [kuᵝ] and belongs to 模; "
        "支 is <code>tsyu1</code> [tsʮ], a perfect label for the rounded fricated rhyme; "
        "雪 is <code>siq7</code> [siɪʔ] (spread) and 月 is <code>yuq8</code> [yɪʔ] (rounded). "
        "The small text under “Rhyme label” in the index is that character's actual reading.",
 "ov4": "<b>How the four divisions are decided.</b> A <code>u</code> medial or a main vowel "
        "<code>u</code> counts as closed; <code>i</code> as spread; <code>yu</code> ([y]) as rounded; "
        "everything else is open. <b>Fricated vowels count as the vowel they come from</b>: "
        "[ɿ] is the fricated form of [i], so that whole rhyme is spread; [ʮ] is the fricated form "
        "of [y], so that whole rhyme is rounded.",
 "ov5": "<b>Unchecked and checked rhymes are kept apart.</b> <b>Unchecked rhymes are tones "
        "1, 2, 3, 5 and 6</b>; <b>checked rhymes are tones 7 and 8</b>. Within an unchecked rhyme the "
        "level, rising and departing tones are no longer separated: one chart across the page lists "
        "the five unchecked tones and holds every level, rising and departing character of that rhyme. "
        "Checked rhymes form a separate block with the glottal-stop coda <code>[ʔ]</code>, listing "
        "only Yin Ru and Yang Ru. Across all {rhymes} rhymes, no rhyme mixes unchecked and checked "
        "characters.",
 "ov6": "<b>The four special rhymes.</b> 嘸 <code>m</code> [m̩], 唔 <code>n</code> [n̩] and "
        "五 <code>ng</code> [ŋ̩] are syllabic nasals, and 而 <code>er</code> [əl] is a retroflex vowel. "
        "These four <b>take no part in the four divisions</b> and have a single slot each, so they are "
        "listed after the checked rhymes.",
 "ov7": "<b>Each cell is one homophone group, that is, one legal syllable.</b> The representative "
        "character sits above and the romanization below; hovering over a cell shows every character "
        "in that group. All <b>{syll} legal syllables</b> of Su–Hu Mixed Wu are in the charts, one "
        "syllable to a cell, never placed twice.",
 "ov8": "<b>Every division slot is labelled with a group count and a character count, and both "
        "numbers are clickable.</b> Clicking the <b>group count</b> opens the list of homophone "
        "groups in that slot; clicking any group then shows all of its characters. Clicking the "
        "<b>character count</b> lists every character in the slot at once, grouped by tone. "
        "Both buttons appear in the rhyme index, the slot index and every chart heading.",
 "ov9": "<b>The rhyme charts start collapsed.</b> The charts below are arranged by rhyme and show "
        "only the label and its statistics by default; click a header to open that rhyme's charts, "
        "click again to close it. To open them all at once, press “{btn_expand}” above.",

 "rt_note": "“Base” is the rhyme's main vowel and coda; “slots” is how many of the four divisions "
            "the rhyme occupies; “groups” is the number of legal syllables (tones included) the rhyme "
            "actually has; “characters” is the deduplicated total of all characters under it. "
            "The “Class” column: <b>陰</b> unchecked with a vowel ending, <b>陽</b> unchecked with a "
            "nasal ending, <b>入</b> checked, <b>特</b> special. Both 陰 and 陽 belong to the unchecked "
            "rhymes. The “<b>N groups</b>” and “<b>N chars</b>” buttons in each cell are clickable: "
            "the group count lists the slot's groups (click one to see all its characters), and the "
            "character count lists every character in the slot outright.",
 "ut_note": "Every division slot listed one by one: rhyme, division, final, phonetic value, group "
            "count and character count. Both numbers are buttons — click to see the group list or "
            "all the characters.",

 "cls_yin": "陰", "cls_yang": "陽", "cls_ru": "入", "cls_te": "特",
 "div_shu": "Unchecked rhymes · tones 1・2・3・5・6 · level, rising and departing are not separated; "
            "all of a rhyme's characters sit in one chart",
 "div_ru": "Checked rhymes · tones 7・8 · with the glottal-stop coda [ʔ], listed separately",
 "div_te": "The four special rhymes · no four-division split (syllabic nasals m／n／ng and the "
           "retroflex vowel er)",
 "div_shu_short": "Unchecked rhymes", "div_ru_short": "Checked rhymes",
 "div_te_short": "Special rhymes (no four divisions)",

 "hu_kai": "Open", "hu_he": "Closed", "hu_qi": "Spread", "hu_cuo": "Rounded", "hu_te": "Special",
 "hu_suffix": "",

 "yt_shu": "Unchecked rhymes", "yt_yin": "Vowel-ending rhymes", "yt_yang": "Nasal-ending rhymes",
 "yt_ru": "Checked rhymes", "yt_te": "The four special rhymes",
 "yt_shu_note": "Unchecked rhymes are the ones with tones 1, 2, 3, 5 and 6 — syllables without a "
                "glottal-stop coda. <b>Level, rising and departing are no longer separated within a "
                "rhyme</b>: each chart below runs across the five unchecked tones and holds every "
                "character of that rhyme. The “N chars” on each chart heading is clickable and shows "
                "all the characters in that slot.",
 "yt_yin_note": "no coda (open syllables)", "yt_yang_note": "nasal coda or nasalised",
 "yt_ru_note": "Checked rhymes are kept apart from unchecked ones. They take the glottal-stop coda "
               "<code>[ʔ]</code> and their charts list only Yin Ru and Yang Ru. They show the same "
               "open／closed／spread／rounded distinctions, so they are charted slot by slot too. "
               "<code>iq</code> [ɪʔ] belongs to the 雪 rhyme (spread throughout) and "
               "<code>iuq</code> [yɪʔ] to the 月 rhyme (rounded throughout), so each is its own rhyme.",
 "yt_te_note": "These four rhymes have unchecked tones (1, 2, 3, 5, 6), but their vowels stand "
               "apart and they have no medial, so they <b>take no part in the four divisions</b> and "
               "are listed as a separate block: <code>m</code> [m̩], <code>n</code> [n̩] and "
               "<code>ng</code> [ŋ̩] are syllabic nasals, <code>er</code> [əl] a retroflex vowel. "
               "Each has a single slot and still lists characters under the five unchecked tones.",
 "rh_open": "Open", "rh_close": "Close",
 "rh_label": "Label read as", "rh_src": "Probable Middle Chinese sources (for reference only)",
 "yt_corner": "Initial ＼ Tone",
 "grp_唇音": "Labials", "grp_舌音": "Dentals & Alveolars", "grp_牙音": "Velars",
 "grp_腭音": "Palatals", "grp_齒音": "Sibilants", "grp_喉音": "Gutturals",

 "lbl_core": "Base", "lbl_hu": "slots", "lbl_sys": "groups", "lbl_chars": "chars",
 "word_rhyme": " rhyme", "word_sys": "groups", "word_chars": "chars", "word_char": "chars",

 "bars_note": "The 24 division slots with the most characters.",

 "md_back": "‹ Back to the group list", "md_close": "Close (Esc)",
 "md_hint_sys": "Below are all the homophone groups under <b>{rhyme}{hu}</b> "
                "({fin} [{ipa}]) — <b>{nsys}</b> in total. Click any row to see every character in "
                "that group.",
 "md_tone_head": "{name}<small>tone {no} ({val}) · {nsys} groups · {nchars} chars</small>",
 "md_rep": "Representative", "md_allchars": "All characters",
 "md_sys_sub": "{fin} [{ipa}] · {nchars} characters · {nsys} groups "
               "(a character with two readings in this slot is listed once for each)",
 "md_direct_sub": "{nchars} characters · press “Back to the group list” to go up one level",
 "md_n_chars": "{n} chars",
 "md_allchars_head": "All characters<small>{nchars} characters in all ({nsys} groups)</small>",
 "md_etc": " … etc.",

 "footer": "Su–Hu Mixed Wu Rhyme Chart · {rhymes} rhymes, {units} division slots, {finals} finals "
           "· readings synced from {link} (SiqYin)",

 "n1": "<b>1. The old labels 談 and 歌 were wrong.</b> 談 was once used as the label of the −n rhyme, "
       "but 談 is now read <code>de6</code> [dᴇ] and belongs with 戴, 帶, 來 and 海 in the 灰 rhyme, "
       "so the name did not fit. The <code>an／uan／ian</code> rhyme now takes <b>陽</b> as its label: "
       "陽 is <code>yan2</code> [iã], right in its spread slot. Likewise 歌 is now "
       "<code>ku1</code> [kuᵝ] and belongs to 模, so the [o̝] rhyme takes <b>麻</b> as its label "
       "(麻 is <code>mo2</code>) and the [uᵝ] rhyme takes <b>模</b> (模 is <code>mu2</code>).",
 "n2": "<b>2. Why 支 and 資 are separate.</b> 支 is <code>tsyu1</code> [tsʮ] and 資 is "
       "<code>tsy1</code> [tsɿ]: one has ʮ as its main vowel and the other ɿ, so the bases differ and "
       "each forms its own rhyme — 支 rounded throughout, 資 spread throughout. In the same way "
       "微 [iᶽ] and 魚 [y] are separate rhymes that do not subsume one another.",
 "n3": "<b>3. The six checked rhymes, and why iq and iuq are split.</b> Six checked rhymes are "
       "listed separately: 八 [aʔ], 陌 [ɑʔ], 質 [əʔ], 雪 [ɪʔ], 月 [yɪʔ], 屋 [oʔ]. "
       "<b><code>iq</code> [iɪʔ] goes to the 雪 rhyme (spread throughout), and <code>iuq</code> [yɪʔ] "
       "forms its own 月 rhyme (rounded throughout).</b> The reason: their main vowel is "
       "<code>ɪ</code>, plainly different from the <code>ə</code> of <code>eq</code> [əʔ] and "
       "<code>ueq</code> [uəʔ] in the 質 rhyme, so by the rule “same base, same rhyme” they cannot be "
       "lumped in with 質; and since iq is only spread while iuq is only rounded, each becomes its own "
       "rhyme with a single slot. The labels fit too: 雪 is <code>siq7</code> [siɪʔ], 月 is "
       "<code>yuq8</code> [yɪʔ]. (The value of <code>iuq</code> was once mis-written [yeʔ]; it has "
       "been corrected to [yɪʔ].)",
 "n4": "<b>4. iã／iɛ̃ in the 陽 rhyme's spread slot are literary versus colloquial readings.</b> "
       "For <code>ian</code> in the 陽 rhyme the dictionary records both [iã] and [iɛ̃] — for example "
       "羊 [iã] and 良 [liɛ̃]. That is a literary/colloquial difference; the base is unchanged, so it "
       "remains one rhyme and one slot.",
 "n5": "<b>5. Where the four special rhymes come from.</b> 嘸 <code>m</code> [m̩], "
       "唔 <code>n</code> [n̩], 五 <code>ng</code> [ŋ̩] and 而 <code>er</code> [əl] have unchecked "
       "tones, but their vowels form a set of their own with no medial, so they <b>take no part in "
       "the four divisions</b> and are classed as “special”, each with a single slot, listed apart "
       "from the four divisions.",
 "n6": "<b>6. The few entries left out.</b> In the dictionary, <code>ba</code> 吧, "
       "<code>kha</code> 快 and <code>don</code> 丼 carry no tone mark, and 如何 and 如何然 are "
       "polysyllabic words; none of them is a single-syllable legal syllable, so no cell is made for "
       "them. The remaining <b>{syll} legal syllables are all in the charts</b>.",
 "n7": "<b>7. Middle Chinese sources are only a reference.</b> The “probable Middle Chinese sources” "
       "line exists to make comparison with the traditional rhyme books easier. A single rhyme often "
       "gathers characters from several Middle Chinese groups (the 泰 rhyme also takes the 麻 rhyme's "
       "velar series, for instance, and 灰 also takes the 止 group's closed readings). The division "
       "here always follows the modern rhyme base, never the Middle Chinese groups.",
 "n8": "<b>8. The readings follow the online database.</b> On loading, the page fetches the data file "
       "of “Su–Hu Mixed Wu Character Lookup” (<code>data/DB_suhu.json</code>) and re-divides the "
       "rhymes and re-lays the charts in the browser. So after characters or readings are added on "
       "the lookup site, reloading this page shows them. If the network is unavailable the page falls "
       "back to its built-in offline snapshot (<b>{chars}</b> characters) and says so at the top; "
       "press “Re-sync the online reading database” once you are back online.",
 "n9": "<b>9. Typeface.</b> The page uses <b>LXGW WenKai</b> by default, because the dictionary "
       "contains a great many rare characters that ordinary system fonts cannot show. The font is "
       "shipped with the site as a subset in two tiers — a core set and a full set — and normally "
       "only the former (about 2 MB) is downloaded.",

 "lang_label": "Language", "lang_wu": "漢語", "lang_en": "English", "lang_ja": "日本語",
}

JA = {
 "page_title": "蘇滬混合腔韻図",
 "h1": "蘇滬混合腔韻図",
 "tagline": "現代音の韻基で分韻し、開・合・斉・撮を一位ずつ掲げ、一位に一図",
 "based_on": "SiqYin の{dict}（字音検索）と{rime}により作成。本頁の収録字数 <b>{chars}</b>、"
             "読み <b>{records}</b> 件、合法音節（声調込み）<b>{syll}</b>。",
 "link_dict": "蘇滬混合腔オンライン字典",
 "link_rime": "RIME 輸入方案",
 "btn_sync": "オンライン字音庫を再同期",
 "btn_expand": "韻図をすべて展開",
 "btn_collapse": "韻図をすべて畳む",
 "btn_top": "ページ先頭へ",
 "btn_hide": "空の声母行を隠す",
 "btn_show": "空の声母行を表示",
 "sync_loading": "オンライン字音庫を読み込んでいます……",
 "sync_ok": "オンライン字音庫と同期しました（{link}）：収録字数 <b>{chars}</b>、"
            "読み <b>{records}</b> 件、合法音節 <b>{syll}</b> 個{stamp}。"
            "検索サイト側で更新があれば、この頁を再読み込みすれば反映されます。",
 "sync_ok_stamp": "；オンラインデータの最終更新は {t}",
 "sync_fail": "オンライン字音庫に接続できません（{err}）。表示しているのは頁に内蔵された"
              "オフラインスナップショット（{chars} 字／{records} 件の読み）です。"
              "接続できたら下の「再同期」を押してください。",

 "sec_overview": "音系概観",
 "sec_rhymes": "分韻一覧",
 "sec_units": "呼位一覧",
 "sec_yuntu": "韻図",
 "sec_bars": "呼位ごとの字数",
 "sec_notes": "補足説明",

 "st_initials": "声母", "st_finals": "韻母", "st_rhymes": "韻（韻基による）",
 "st_units": "呼位（韻×呼）", "st_tones": "声調（舒 {shu}・入 {ru}）", "st_cells": "小韻の枠",

 "th_no": "調号", "th_cls": "調類", "th_val": "調値", "th_kind": "舒／入",
 "th_class": "類",
 "rt_hu4": "四呼（韻母・音価・小韻数・字数）",
 "kind_shu": "舒声", "kind_ru": "入声",
 "tone_1": "陰平", "tone_2": "陽平", "tone_3": "陰上", "tone_5": "陰去",
 "tone_6": "陽上去", "tone_7": "陰入", "tone_8": "陽入",
 "tone_note": "蘇滬混合腔には陽上と陽去の区別がなく、この二類は現在どちらも調 6「陽上去」に"
              "統合されている。したがって声調は全部で {total} つである。",

 "ov1": "<b>分韻は現代音の韻基だけで決める。</b>韻基とは主母音と韻尾のことである。韻基が違えば、"
        "中古に同じ韻摂に属していても別の韻に分ける。韻基が同じなら、中古に別の韻摂から来ていても"
        "同じ韻にまとめる。したがって <code>i[iᶽ]</code> と <code>iu[y]</code> は微韻と魚韻に、"
        "<code>y[ɿ]</code> と <code>yu[ʮ]</code> は資韻と支韻に分かれる。入声では "
        "<code>eq[əʔ]</code>・<code>ueq[uəʔ]</code>（主母音は <code>ə</code>）と "
        "<code>iq[iɪʔ]</code>（主母音は <code>ɪ</code>）が質韻と雪韻に分かれ、"
        "<code>iuq[yɪʔ]</code> は独立して月韻となる。"
        "合わせて <b>{rhymes} 韻</b>。",
 "ov2": "<b>開・合・斉・撮を一位ずつ掲げる。</b>一つの韻がいくつの呼を占めるかによって、"
        "その数の呼位を掲げ、<b>一位に一図</b>を描く。全部で <b>{units} の呼位</b>、"
        "うち開口 {n_kai}、合口 {n_he}、斉歯 {n_qi}、撮口 {n_cuo}、特例 {n_te}。"
        "四呼がそろうのは「八」韻ただ一つ。呼位が一つだけなのは十韻——"
        "模（合）・魚（撮）・支（撮）・資（斉）・微（斉）・仙（斉）・侵（斉）・雲（撮）・"
        "雪（斉）・月（撮）。",
 "ov3": "<b>韻目の代表字はすべて検証済みである。</b>各韻の名には、その韻に本当にその読みがある字を"
        "取り、しかもプログラムで一字ずつ確かめてある。たとえば「談」は現在 <code>de6</code>〔dᴇ〕で"
        "灰韻に属するため、もはや −n 韻の韻目にはしない。「歌」は現在 <code>ku1</code>〔kuᵝ〕で"
        "模韻に属する。「支」は <code>tsyu1</code>〔tsʮ〕で、撮口の摩擦化韻の韻目にうってつけである。"
        "「雪」は <code>siq7</code>〔siɪʔ〕で斉歯、「月」は <code>yuq8</code>〔yɪʔ〕で撮口、"
        "それぞれ名実が一致する。一覧の「韻目取字」欄の小さい文字が、その韻目字の実際の読みである。",
 "ov4": "<b>四呼の判定。</b><code>u</code> の介音をもつもの、または主母音が <code>u</code> のものは"
        "合口。<code>i</code> の介音、または主母音が <code>i</code> のものは斉歯。"
        "<code>yu</code> の介音、または主母音が <code>yu</code>（〔y〕）のものは撮口。"
        "残りは開口とする。<b>摩擦化した母音は元の母音で数える</b>：〔ɿ〕は〔i〕の摩擦化なので"
        "その韻全体が斉歯、〔ʮ〕は〔y〕の摩擦化なのでその韻全体が撮口である。",
 "ov5": "<b>舒声韻と入声韻は分けて並べる。</b><b>舒声韻は声調 1・2・3・5・6</b>、"
        "<b>入声韻は声調 7・8</b>。舒声韻の内部では平・上・去をさらに分けない。一つの図に"
        "五つの舒声調を横に並べ、その韻の平・上・去の字はすべて同じ図に入る。入声韻は別の区として"
        "掲げ、喉塞尾 <code>[ʔ]</code> をもち、図には陰入と陽入の二調だけを並べる。"
        "全体で {rhymes} 韻、舒声と入声の字が混じる韻は一つもない。",
 "ov6": "<b>特例の四韻。</b><b>嘸</b><code>m</code>〔m̩〕・<b>唔</b><code>n</code>〔n̩〕・"
        "<b>五</b><code>ng</code>〔ŋ̩〕は成節鼻音、<b>而</b><code>er</code>〔əl〕は反舌母音である。"
        "この四韻は<b>開合斉撮に分かれず</b>、それぞれ呼位を一つだけもつので、"
        "入声韻の後に別に掲げる。",
 "ov7": "<b>一つの枠が一つの小韻、すなわち一つの合法音節である。</b>枠の上に代表字、下にローマ字を"
        "示し、枠にマウスを乗せるとその小韻のすべての字が表示される。蘇滬混合腔の "
        "<b>{syll} の合法音節はすべて図の中にあり</b>、一枠に一韻、重複して置かれることはない。",
 "ov8": "<b>どの呼位にも小韻数と字数が付いており、どちらの数字も押せる。</b>"
        "<b>小韻数</b>を押すとその呼位の小韻一覧が開き、その中のどれかを押せばその小韻の"
        "すべての所属字が見られる。<b>字数</b>を押すとその呼位の全漢字が声調ごとに並ぶ。"
        "分韻一覧・呼位一覧・各韻図の見出しのいずれにもこの二つのボタンがある。",
 "ov9": "<b>韻図は既定で畳んである。</b>下の韻図は韻ごとに並べ、既定では韻目と統計だけを表示する。"
        "見出しを押せばその韻の図が開き、もう一度押せば畳まれる。全部を一度に開くには"
        "上の「{btn_expand}」を押す。",

 "rt_note": "「韻基」はその韻の主母音と韻尾。「呼位数」はその韻が四呼のうちいくつを占めるか。"
            "「小韻合計」はその韻が実際にもつ合法音節（声調込み）の数。"
            "「字数合計」はその韻に属する全漢字の重複を除いた総数。"
            "「類」欄：<b>陰</b>＝陰声韻、<b>陽</b>＝陽声韻、<b>入</b>＝入声韻、<b>特</b>＝特例韻。"
            "陰声韻と陽声韻はいずれも舒声韻に属する。各枠の「<b>N 小韻</b>」と「<b>N 字</b>」の"
            "ボタンはどちらも押せる。小韻数を押すとその呼位の小韻が並び（そのうち一つを押せば"
            "その小韻の全所属字が見られる）、字数を押すとその呼位の全漢字がそのまま並ぶ。",
 "ut_note": "各呼位を一条ずつ掲げる：韻目・呼・韻母・音価・小韻数・字数。"
            "「小韻数」と「字数」はどちらもボタンで、押すとそれぞれ小韻一覧と全漢字が見られる。",

 "cls_yin": "陰", "cls_yang": "陽", "cls_ru": "入", "cls_te": "特",
 "div_shu": "舒声韻　声調 1・2・3・5・6　平・上・去を分けず、同じ韻の平上去の字は同じ図にある",
 "div_ru": "入声韻　声調 7・8　喉塞尾 [ʔ] をもち、別に掲げる",
 "div_te": "特例の四韻　開合斉撮に分かれない（成節鼻音 m／n／ng と反舌母音 er）",
 "div_shu_short": "舒声韻", "div_ru_short": "入声韻", "div_te_short": "特例の四韻（四呼に分かれず）",

 "hu_kai": "開口", "hu_he": "合口", "hu_qi": "斉歯", "hu_cuo": "撮口", "hu_te": "特例",
 "hu_suffix": "呼",

 "yt_shu": "舒声韻", "yt_yin": "陰声韻", "yt_yang": "陽声韻",
 "yt_ru": "入声韻", "yt_te": "特例の四韻",
 "yt_shu_note": "舒声韻とは声調が 1・2・3・5・6 の字、つまり喉塞尾をもたない音節である。"
                "<b>同じ韻の平・上・去はもはや分けない</b>：下の各図は五つの舒声調を横に並べ、"
                "その韻の平上去の字をすべて同じ図に収める。各図の見出しにある「N 字」は押すことができ、"
                "その呼位に属する全漢字が表示される。",
 "yt_yin_note": "韻尾なし（開音節）", "yt_yang_note": "鼻音韻尾または鼻母音化",
 "yt_ru_note": "入声韻は舒声韻と分けて並べる。喉塞尾 <code>[ʔ]</code> をもち、"
               "図には陰入と陽入の二調だけを並べる。入声韻にも開・合・斉・撮の区別があるので、"
               "同じく一位ずつ図を描く。<code>iq</code>〔ɪʔ〕は<b>雪</b>韻（韻全体が斉歯）、"
               "<code>iuq</code>〔yɪʔ〕は<b>月</b>韻（韻全体が撮口）に属し、"
               "それぞれ別の韻とする。",
 "yt_te_note": "この四韻の声調は舒声（1・2・3・5・6）に属するが、母音が独自の体系をなし、"
               "介音もないため<b>開合斉撮に分かれず</b>、別の区として掲げる："
               "<code>m</code>〔m̩〕・<code>n</code>〔n̩〕・<code>ng</code>〔ŋ̩〕は成節鼻音、"
               "<code>er</code>〔əl〕は反舌母音である。四韻はいずれも呼位を一つだけもち、"
               "図には依然として五つの舒声調で字を並べる。",
 "rh_open": "展開", "rh_close": "畳む",
 "rh_label": "韻目取字", "rh_src": "中古の推定来源（参考のみ）",
 "yt_corner": "声母＼調",
 "grp_唇音": "唇音", "grp_舌音": "舌音", "grp_牙音": "牙音",
 "grp_腭音": "硬口蓋音", "grp_齒音": "歯音", "grp_喉音": "喉音",

 "lbl_core": "韻基", "lbl_hu": "呼位", "lbl_sys": "小韻", "lbl_chars": "字数",
 "word_rhyme": "韻", "word_sys": "小韻", "word_chars": "字", "word_char": "字",

 "bars_note": "字数の多い順に 24 の呼位。",

 "md_back": "‹ 小韻一覧に戻る", "md_close": "閉じる（Esc）",
 "md_hint_sys": "以下は「<b>{rhyme}{hu}</b>」（{fin}〔{ipa}〕）に属する小韻のすべて、"
                "全部で <b>{nsys} 個</b>。どの行を押しても、その小韻の全所属字が見られる。",
 "md_tone_head": "{name}<small>調 {no}（{val}）・小韻 {nsys} 個 ・計 {nchars} 字</small>",
 "md_rep": "代表字", "md_allchars": "全所属字",
 "md_sys_sub": "{fin} [{ipa}] ・ 計 {nchars} 字 ・ {nsys} 個の小韻"
               "（同じ字がこの呼位に二つの読みをもつ場合は別々に掲げる）",
 "md_direct_sub": "{nchars} 字 ・「小韻一覧に戻る」で一つ上の階層へ",
 "md_n_chars": "{n} 字",
 "md_allchars_head": "全所属字<small>計 {nchars} 字（{nsys} 個の小韻）</small>",
 "md_etc": "…ほか",

 "footer": "蘇滬混合腔韻図 ・ 分韻 {rhymes}、呼位 {units}、韻母 {finals}"
           " ・ 字音データは {link}（SiqYin）より同期",

 "n1": "<b>一、旧稿の「談韻」「歌韻」は韻目を誤っていた。</b>以前は「談」を −n 韻の韻目にしていたが、"
       "「談」は現在 <code>de6</code>〔dᴇ〕で「戴」「帶」「來」「海」と同じ韻（灰韻）に属し、"
       "名実が伴わない。そこで <code>an／uan／ian</code> の韻は「<b>陽</b>」を韻目とした："
       "陽は <code>yan2</code>〔iã〕で、ちょうどその斉歯の位にある。同様に「歌」は現在 "
       "<code>ku1</code>〔kuᵝ〕で模韻に属するため、〔o̝〕の韻は「<b>麻</b>」を韻目とし"
       "（麻は <code>mo2</code>）、〔uᵝ〕の韻は「<b>模</b>」を韻目とする（模は <code>mu2</code>）。",
 "n2": "<b>二、「支」と「資」を分ける理由。</b>「支」は <code>tsyu1</code>〔tsʮ〕、"
       "「資」は <code>tsy1</code>〔tsɿ〕で、主母音が一方は ʮ、他方は ɿ であり韻基が異なるため、"
       "それぞれ別の韻とする：支韻は全体が撮口、資韻は全体が斉歯である。同様に「微」〔iᶽ〕と"
       "「魚」〔y〕もそれぞれ独立した韻で、互いに包括関係にはない。",
 "n3": "<b>三、入声の六韻、および iq と iuq を分ける理由。</b>入声は別に掲げ、全部で六韻："
       "八〔aʔ〕・陌〔ɑʔ〕・質〔əʔ〕・雪〔ɪʔ〕・月〔yɪʔ〕・屋〔oʔ〕。"
       "<b><code>iq</code>〔iɪʔ〕は「雪」韻（韻全体が斉歯）に、"
       "<code>iuq</code>〔yɪʔ〕は独立して「月」韻（韻全体が撮口）とする。</b>"
       "理由は、この二つの韻母の主母音が <code>ɪ</code> であり、質韻の <code>eq</code>〔əʔ〕・"
       "<code>ueq</code>〔uəʔ〕（主母音は <code>ə</code>）とは明らかに異なるため、"
       "「韻基が同じものだけを同韻とする」原則から質韻に混ぜられないこと、"
       "そして iq は斉歯のみ、iuq は撮口のみであるため、それぞれ独立した韻とし、一韻に一呼位とする。"
       "韻目もよく合う：「雪」は <code>siq7</code>〔siɪʔ〕、「月」は <code>yuq8</code>〔yɪʔ〕。"
       "（<code>iuq</code> の音価は以前〔yeʔ〕と誤記していたが、現在は〔yɪʔ〕に訂正済み。）",
 "n4": "<b>四、陽韻斉歯位の iã／iɛ̃ は文白異読である。</b>陽韻斉歯の <code>ian</code> の位には、"
       "字典が〔iã〕と〔iɛ̃〕の二つの音価を併記している。たとえば「羊」は〔iã〕、"
       "「良」は〔liɛ̃〕。これは文読と白読の違いであり、韻基は変わっていないので、"
       "依然として同じ韻・同じ呼位である。",
 "n5": "<b>五、特例の四韻の由来。</b>嘸 <code>m</code>〔m̩〕・唔 <code>n</code>〔n̩〕・"
       "五 <code>ng</code>〔ŋ̩〕・而 <code>er</code>〔əl〕の四韻は、声調は舒声に属するが、"
       "母音が独自の体系をなし、介音もないため<b>開合斉撮に分かれず</b>、"
       "「特例」という別の類にまとめた。それぞれ呼位は一つだけで、四呼とは混ぜて並べない。",
 "n6": "<b>六、図に収めなかった少数の項目。</b>字典の <code>ba</code>「吧」・"
       "<code>kha</code>「快」・<code>don</code>「丼」の三条は声調の記載がなく、"
       "また「如何」「如何然」の二条は多音節語で、いずれも単音節の合法音節ではないため枠を設けない。"
       "残る <b>{syll} の合法音節はすべて図に収めてある</b>。",
 "n7": "<b>七、中古の来源は参考にすぎない。</b>各韻の「中古の推定来源」の欄は、"
       "伝統的な韻書と対照しやすくするために設けたものである。一つの韻はしばしば複数の韻摂の字を"
       "併せて収める（たとえば泰韻は麻韻の見系を兼ね、灰韻は止摂の合口を兼ねる）。"
       "本図の分韻はあくまで現代音の韻基を基準とし、中古の韻摂にはよらない。",
 "n8": "<b>八、本頁の字音はオンライン字音庫に追随する。</b>本頁は開いたときに"
       "「蘇滬混合腔字音検索」のデータファイル（<code>data/DB_suhu.json</code>）を即時に読み込み、"
       "ブラウザ内で分韻し直し、図を組み直す。したがって検索サイト側で字を追加したり読みを"
       "補ったりすれば、この頁を再読み込みするだけで最新の字が見られる。ネットワークに"
       "接続できない場合は、頁に内蔵されたオフラインスナップショット（<b>{chars}</b> 字）に"
       "切り替わり、上部にその旨を表示する。接続後は「オンライン字音庫を再同期」を押せばよい。",
 "n9": "<b>九、書体。</b>本頁は既定で<b>霞鶩文楷</b>（LXGW WenKai）で表示する。字典が多数の"
       "生僻字を収めており、一般的なシステム書体では表示できないためである。書体はサブセット化して"
       "頁と一緒に配信し、「核心字集」と「完全字集」の二段構えとしている。通常は前者（約 2 MB）"
       "のみをダウンロードする。",

 "lang_label": "言語", "lang_wu": "漢語", "lang_en": "English", "lang_ja": "日本語",
}

# 各韻的「中古可能的來源」逐韻譯文（順序與 scheme.json 的 rhymes 一致）
GLOSS = {
 "en": [
  "Xie group: 泰 佳 皆 夬 (open & closed) + Jia group: 麻 rhyme, velar series (spread) "
  "+ Guo group: 歌 rhyme, colloquial readings",
  "Jia group: 麻 rhyme, plain-grade readings; also takes Guo group 戈 rhyme",
  "Xie group: 咍 泰, grade I + Zhi group: closed readings, colloquial",
  "Xiao group: 豪 肴 宵 蕭",
  "Liu group: 侯 尤 幽",
  "Shan group: 寒 桓 + Xian group: 覃 談 + Zhi group: closed readings",
  "Yu group: 模 魚 虞, plain-grade readings + Guo group: 歌 戈",
  "Yu group: 魚 虞, fine-grade readings",
  "Zhi group: 支 脂 之, 知 照 日 series, fricated + Yu group: 魚 虞, 知 照 series",
  "Zhi group: 支 脂 之, 精 series, fricated",
  "Zhi group: 支 脂 之 微, open readings + Xie group: 齊 祭",
  "Xian group: 鹽 嚴 添 + Shan group: 仙 元 先, grades III–IV (nasal coda lost)",
  "Geng group: 庚 耕, colloquial + Dang group: 陽 唐, colloquial",
  "Dang group: 唐 陽 + Jiang group: 江",
  "Zhen group: 痕 魂 + 真 諄, 知 照 series + Zeng & Geng groups, grades I–II",
  "Shen group: 侵 + Zhen group: 真 + Zeng & Geng groups, grades III–IV",
  "Zhen group: 諄 文, closed readings, grade III, velar series",
  "Tong group: 東 冬 鍾",
  "Shan group: 曷 黠 鎋 薛 + Xian group: 合 盍 洽 狎 葉 帖",
  "Geng group: 陌 麥 + Dang group: 藥 鐸, grades II–III",
  "Zhen group: 質 術 物 + Zeng group: 德 職 + Geng group: 陌 麥, literary + Shen group: 緝",
  "Shan group: 屑 薛, fine-grade + Geng group: 錫 + Shen group: 緝, fine-grade (spread)",
  "Shan group: 月 屑 薛, fine-grade + Zhen group: 物 迄 + Geng group: 錫 (rounded)",
  "Tong group: 屋 沃 燭 + Dang group: 鐸",
  "Ming initial, colloquial reading; syllabic labial nasal",
  "Ni initial, colloquial reading; syllabic apical nasal",
  "Yi initial, colloquial reading; syllabic velar nasal",
  "Zhi group: 日 initial, 「兒 爾 二」 and the like; now a retroflex vowel",
 ],
 "ja": [
  "蟹摂 泰・佳・皆・夬（開合）＋仮摂 麻韻見系（斉歯）＋果摂 歌韻白読",
  "仮摂 麻韻の洪音；果摂 戈韻も兼収",
  "蟹摂 咍・泰の一等＋止摂の合口白読",
  "効摂 豪・肴・宵・蕭",
  "流摂 侯・尤・幽",
  "山摂 寒・桓＋咸摂 覃・談＋止摂の合口",
  "遇摂 模・魚・虞の洪音＋果摂 歌・戈",
  "遇摂 魚・虞の細音",
  "止摂 支・脂・之の知・照・日組（摩擦化）＋遇摂 魚・虞の知・照組",
  "止摂 支・脂・之の精組（摩擦化）",
  "止摂 支・脂・之・微の開口＋蟹摂 斉・祭",
  "咸摂 塩・厳・添＋山摂 仙・元・先の三四等（鼻音韻尾の脱落）",
  "梗摂 庚・耕の白読＋宕摂 陽・唐の白読",
  "宕摂 唐・陽＋江摂 江",
  "臻摂 痕・魂＋真・諄の知照組＋曾・梗摂の一二等",
  "深摂 侵＋臻摂 真＋曾・梗摂の三四等",
  "臻摂 諄・文の合口三等見系",
  "通摂 東・冬・鍾",
  "山摂 曷・黠・鎋・薛＋咸摂 合・盍・洽・狎・葉・帖",
  "梗摂 陌・麦＋宕摂 薬・鐸の二三等",
  "臻摂 質・術・物＋曾摂 徳・職＋梗摂 陌・麦の文読＋深摂 緝",
  "山摂 屑・薛の細音＋梗摂 錫＋深摂 緝の細音（斉歯）",
  "山摂 月・屑・薛の細音＋臻摂 物・迄＋梗摂 錫（撮口）",
  "通摂 屋・沃・燭＋宕摂 鐸",
  "明母の白読。成節唇鼻音",
  "泥母の白読。成節舌尖鼻音",
  "疑母の白読。成節舌根鼻音",
  "止摂 日母「兒・爾・二」など；現在は反舌母音",
 ],
}

I18N = {"wu": WU, "en": EN, "ja": JA}
