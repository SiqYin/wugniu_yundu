# -*- coding: utf-8 -*-
"""
苏沪混合腔 分韵构拟韵图 —— 数据构建脚本（第二版：严格按韵基分韵，四呼逐一列出）

数据源：https://siqyin.github.io/wugniu_zyinzozin/  (data/DB_suhu.json)
       https://github.com/SiqYin/wugniu_suwu     (wugniu_suwu.dict.yaml)

分韵原则
--------
1. 韵 = 韵基（主元音＋韵尾）。韵基不同者，即便中古同摄，亦分立为韵。
   例：an[ã]／ian[iã] 同韵基，为一韵之开・齐；en[ən]／in[in]／iun[yn] 分立三韵。
   入声六韵：八 aʔ、陌 ɑʔ、質 əʔ、雪 iɪʔ、月 yɪʔ、屋 oʔ；
   其中 iq[iɪʔ] 归雪韵、iuq[yɪʔ] 归月韵。
   注：本页的音标一律标【音值】（实际读音），不列音位；
   分韵说明只陈述事实，不拿音值去推理由。
2. 呼 = 介音或主元音之性质：有 u 介音或主元音为 u 者合口，i 介音或
   主元音为 i 者为齐齿，yu 介音或主元音为 yu（[y]）者为撮口，余为开口。
   擦化元音 [ɿ] 计作 i 之擦化（齐齿），[ʮ] 计作 [y] 之擦化（撮口）。
3. 一韵之内，四呼各占若干位；凡所占者，逐一列出。
4. 韵目取字，必取本韵内实际读音相符之字（脚本自动校验）。

输出：yuntu_data.json
"""
import json, re, collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "DB_suhu.json")

# ---------------- 音系定义 ----------------
FINALS = ("a ua ia o io y yu i u iu ie e ue au iau eu ieu oe uoe ioe "
          "an uan ian aon uaon iaon on ion en uen in iun "
          "aeq uaeq iaeq iuaeq aq iaq eq ueq iq iuq oq ioq er n m ng").split()

# 韵母音值（据字典 IPA 字段归纳；「~」示文白异读之异值）
IPA_OF_FINAL = {
    "a": "ɑ", "ua": "uɑ", "ia": "iɑ",
    "o": "o̝", "io": "io̝",
    "y": "ɿ", "yu": "ʮ",
    "i": "iᶽ", "u": "uᵝ", "iu": "y",
    "ie": "i",
    "e": "ᴇ", "ue": "uᴇ",
    "au": "ɔ", "iau": "iɔ",
    "eu": "ɤ", "ieu": "iɤ",
    "oe": "ø", "uoe": "uø", "ioe": "iø",
    "an": "ã", "uan": "uã", "ian": "iã~iɛ̃",
    "aon": "ɑ̃", "uaon": "uɑ̃", "iaon": "iɑ̃",
    "on": "oŋ", "ion": "ioŋ",
    "en": "ən", "uen": "uən", "in": "in", "iun": "yn",
    "aeq": "aʔ", "uaeq": "uaʔ", "iaeq": "iaʔ", "iuaeq": "yaʔ",
    "aq": "ɑʔ", "iaq": "iɑʔ",
    "eq": "əʔ", "ueq": "uəʔ", "iq": "iɪʔ", "iuq": "yɪʔ",
    "oq": "oʔ", "ioq": "ioʔ",
    "er": "əl", "n": "n̩", "m": "m̩", "ng": "ŋ̩",
}

# 声母：字素 -> (五音, 中古字母, 音值)
INITIALS = {
    "":   ("喉", "影／喻", "∅"),
    "p":  ("唇", "幫", "p"),   "ph": ("唇", "滂", "pʰ"), "b": ("唇", "並", "b"),
    "m":  ("唇", "明", "m"),   "f":  ("唇", "非", "f"),  "v": ("唇", "奉", "v"),
    "t":  ("舌", "端", "t"),   "th": ("舌", "透", "tʰ"), "d": ("舌", "定", "d"),
    "n":  ("舌", "泥", "n"),   "l":  ("舌", "來", "l"),  "gn": ("舌", "日", "ɲ"),
    "k":  ("牙", "見", "k"),   "kh": ("牙", "溪", "kʰ"), "g":  ("牙", "群", "ɡ"),
    "ng": ("牙", "疑", "ŋ"),
    "ts": ("齒", "精／照", "ts"), "tsh": ("齒", "清／穿", "tsʰ"),
    "s":  ("齒", "心／審", "s"),  "z":   ("齒", "從／邪／澄／床／禪", "z"),
    "ci": ("腭", "見(細)", "tɕ"), "chi": ("腭", "溪(細)", "tɕʰ"),
    "ji": ("腭", "群(細)", "dʑ"), "shi": ("腭", "曉(細)", "ɕ"),
    "h":  ("喉", "曉", "h"),   "gh": ("喉", "匣", "ɦ"),
}

INITIAL_ORDER = ["", "p", "ph", "b", "m", "f", "v",
                 "t", "th", "d", "n", "l", "gn",
                 "k", "kh", "g", "ng",
                 "ci", "chi", "ji", "shi",
                 "ts", "tsh", "s", "z",
                 "h", "gh"]

PAL_MAP = {"": "i", "a": "ia", "aeq": "iaeq", "an": "ian", "aon": "iaon",
           "aq": "iaq", "au": "iau", "e": "ie", "eu": "ieu", "n": "in",
           "o": "io", "oe": "ioe", "on": "ion", "oq": "ioq", "q": "iq",
           "u": "iu", "un": "iun", "uq": "iuq"}

ZERO_MAP = {"ya": "ia", "yaeq": "iaeq", "yan": "ian", "yaon": "iaon",
            "yaq": "iaq", "yau": "iau", "ye": "ie", "yeu": "ieu",
            "yi": "i", "yin": "in", "yiq": "iq", "yo": "io", "yoe": "ioe",
            "yon": "ion", "yoq": "ioq", "yu": "iu", "yuaeq": "iuaeq",
            "yun": "iun", "yuq": "iuq",
            "wa": "ua", "waeq": "uaeq", "wan": "uan", "waon": "uaon",
            "we": "ue", "wen": "uen", "weq": "ueq", "woe": "uoe", "wu": "u"}

PLAIN = ["tsh", "gn", "kh", "ng", "gh", "ph", "ts", "th",
         "p", "b", "m", "f", "v", "t", "d", "n", "l", "k", "g", "h", "s", "z"]

# 音图行分组（唇舌牙腭齿喉）
GROUPS = [("唇音", ["p", "ph", "b", "m", "f", "v"]),
          ("舌音", ["t", "th", "d", "n", "l", "gn"]),
          ("牙音", ["k", "kh", "g", "ng"]),
          ("腭音", ["ci", "chi", "ji", "shi"]),
          ("齒音", ["ts", "tsh", "s", "z"]),
          ("喉音", ["", "h", "gh"])]

TONE_INFO = {
    "1": ("陰平", "44", "舒"), "2": ("陽平", "223", "舒"),
    "3": ("陰上", "51", "舒"), "5": ("陰去", "523", "舒"),
    "6": ("陽上去", "231", "舒"),
    "7": ("陰入", "43", "入"), "8": ("陽入", "23", "入"),
}
SHU_TONES = ["1", "2", "3", "5", "6"]
RU_TONES = ["7", "8"]

HU_ORDER = ["開", "合", "齊", "撮", "特"]
HU_DESC = {"開": "開口", "合": "合口", "齊": "齊齒", "撮": "撮口", "特": "特例"}

# ---------------- 分韵（28 韵 · 48 呼位） ----------------
# (韵目, 韵基, 韵目取字之读音, 中古大概来源（仅供参考）, {呼: [韵母]})
RHYME_TABLE = [
    # —— 陰聲韻（無韻尾）——
    ("泰", "ɑ",   "tha5",  "蟹攝泰佳皆夬（開合）＋假攝麻韻見系（齊齒）＋果攝歌韻白讀",
     {"開": ["a"], "合": ["ua"], "齊": ["ia"]}),
    ("麻", "o̝",   "mo2",   "假攝麻韻洪音；兼收果攝戈韻",
     {"開": ["o"], "齊": ["io"]}),
    ("灰", "ᴇ",   "hue1",  "蟹攝咍泰一等＋止攝合口白讀",
     {"開": ["e"], "合": ["ue"]}),
    ("豪", "ɔ",   "ghau2", "效攝豪肴宵蕭",
     {"開": ["au"], "齊": ["iau"]}),
    ("侯", "ɤ",   "gheu2", "流攝侯尤幽",
     {"開": ["eu"], "齊": ["ieu"]}),
    ("寒", "ø",   "ghoe2", "山攝寒桓＋咸攝覃談＋止攝合口",
     {"開": ["oe"], "合": ["uoe"], "齊": ["ioe"]}),
    ("模", "uᵝ",  "mu2",   "遇攝模魚虞洪音＋果攝歌戈",
     {"合": ["u"]}),
    ("魚", "y",   "yu2",   "遇攝魚虞細音",
     {"撮": ["iu"]}),
    ("支", "ʮ",   "tsyu1", "止攝支脂之知照日組擦化＋遇攝魚虞知照組",
     {"撮": ["yu"]}),
    ("資", "ɿ",   "tsy1",  "止攝支脂之精組擦化",
     {"齊": ["y"]}),
    ("微", "iᶽ",  "vi2",   "止攝支脂之微開口＋蟹攝齊祭",
     {"齊": ["i"]}),
    ("仙", "i",   "sie1",  "咸攝鹽嚴添＋山攝仙元先三四等（鼻尾脫落）",
     {"齊": ["ie"]}),
    # —— 陽聲韻（鼻尾／鼻化）——
    ("陽", "ã",   "yan2",  "梗攝庚耕白讀＋宕攝陽唐白讀",
     {"開": ["an"], "合": ["uan"], "齊": ["ian"]}),
    ("江", "ɑ̃",   "kaon1", "宕攝唐陽＋江攝江",
     {"開": ["aon"], "合": ["uaon"], "齊": ["iaon"]}),
    ("真", "ən",  "tsen1", "臻攝痕魂＋真諄知照組＋曾梗攝一二等",
     {"開": ["en"], "合": ["uen"]}),
    ("侵", "in",  "tshin1","深攝侵＋臻攝真＋曾梗攝三四等",
     {"齊": ["in"]}),
    ("雲", "yn",  "yun2",  "臻攝諄文合口三等見系",
     {"撮": ["iun"]}),
    ("東", "oŋ",  "ton1",  "通攝東冬鍾",
     {"開": ["on"], "齊": ["ion"]}),
    # —— 入聲韻（喉塞尾）——
    ("八", "aʔ",  "paeq7", "山攝曷黠鎋薛＋咸攝合盍洽狎葉帖",
     {"開": ["aeq"], "合": ["uaeq"], "齊": ["iaeq"], "撮": ["iuaeq"]}),
    ("陌", "ɑʔ",  "maq8",  "梗攝陌麥＋宕攝藥鐸二三等",
     {"開": ["aq"], "齊": ["iaq"]}),
    ("質", "əʔ",  "tseq7", "臻攝質術物＋曾攝德職＋梗攝陌麥文讀＋深攝緝",
     {"開": ["eq"], "合": ["ueq"]}),
    ("雪", "iɪʔ",  "siq7",  "山攝屑薛細音＋梗攝錫＋深攝緝細音（齊齒）",
     {"齊": ["iq"]}),
    ("月", "yɪʔ", "yuq8",  "山攝月屑薛細音＋臻攝物迄＋梗攝錫（撮口）",
     {"撮": ["iuq"]}),
    ("屋", "oʔ",  "oq7",   "通攝屋沃燭＋宕攝鐸",
     {"開": ["oq"], "齊": ["ioq"]}),
    # —— 特例四韻（不分開合齊撮）——
    ("嘸", "m̩",   "m2",    "明母白讀，成音節唇鼻音",
     {"特": ["m"]}),
    ("唔", "n̩",   "n6",    "泥母白讀，成音節舌尖鼻音",
     {"特": ["n"]}),
    ("五", "ŋ̩",   "ng6",   "疑母白讀，成音節舌根鼻音",
     {"特": ["ng"]}),
    ("而", "əl",  "er6",   "止攝日母「兒爾二」等；今讀捲舌元音",
     {"特": ["er"]}),
]

# 韻類四分（陰聲／陽聲／入聲／特例）
CLASS_OF = {}
for _n, _c, _r, _s, _h in RHYME_TABLE:
    if "特" in _h:
        CLASS_OF[_n] = "特例韻"
    elif any(f.endswith("q") for f in sum(_h.values(), [])):
        CLASS_OF[_n] = "入聲韻"
    elif _c in ("ã", "ɑ̃", "ən", "in", "yn", "oŋ"):
        CLASS_OF[_n] = "陽聲韻"
    else:
        CLASS_OF[_n] = "陰聲韻"
CLASS_ORDER = ["陰聲韻", "陽聲韻", "入聲韻", "特例韻"]


def parse_syllable(syl):
    """把拼音音节切成 (声母, 韵母)。返回 None 表示非单音节合法音节。"""
    if syl in ("m", "n", "ng"):
        return ("", syl)
    for p in ("chi", "shi", "ci", "ji"):
        if syl.startswith(p):
            return (p, PAL_MAP.get(syl[len(p):], syl[len(p):]))
    for p in PLAIN:
        if syl.startswith(p):
            return (p, syl[len(p):])
    if syl in ZERO_MAP:
        return ("", ZERO_MAP[syl])
    if syl in FINALS:
        return ("", syl)
    return None


def main():
    db = json.load(open(DB, encoding="utf-8"))

    inst = collections.defaultdict(lambda: {"ipa": set(), "chars": []})
    raw_syllables = set()
    bad = []

    for rec in db:
        ch = rec["character"]
        for m in rec["meaning"]:
            mm = re.match(r"^(.*?)([0-9])$", m[0])
            if not mm:
                bad.append((ch, m[0], "非單音節條目"))
                continue
            syl, tone = mm.group(1), mm.group(2)
            p = parse_syllable(syl)
            if p is None:
                bad.append((ch, m[0], "無法解析"))
                continue
            ini, fin = p
            if fin not in FINALS:
                bad.append((ch, m[0], "韵母不在表内: " + fin))
                continue
            raw_syllables.add(syl)
            inst[(ini, fin, tone)]["ipa"].add(m[1])
            inst[(ini, fin, tone)]["chars"].append((ch, syl))

    # ---- 全部读音串的口径统计（供页面说明用） ----
    # 字典里的读音串去重后分三类：①单音节且带调（＝图里的小韵格位）
    # ②单音节但没标声调（入不了按声调排的格子）③不是单音节（多音节词）
    str_chars = collections.defaultdict(set)
    for rec in db:
        for m in rec["meaning"]:
            str_chars[m[0]].add(rec["character"])

    def _splits(s):
        mm = re.match(r"^(.*?)([0-9])$", s)
        if not mm:
            return None
        p = parse_syllable(mm.group(1))
        return p if (p and p[1] in FINALS) else False

    str_tones, str_untone, str_words = [], [], []
    for s in sorted(str_chars):
        if _splits(s) is None:
            str_untone.append(s)
        elif _splits(s) is False:
            str_words.append(s)
        else:
            str_tones.append(s)
    assert len(str_tones) == len(inst), (len(str_tones), len(inst))

    def _pair(s):
        return [s, "".join(sorted(str_chars[s]))]

    # 韵母 -> (韵目, 呼)
    fin_slot = {}
    for name, core, ref, src, hus in RHYME_TABLE:
        for hu, fl in hus.items():
            for f in fl:
                fin_slot[f] = (name, hu)
    missing = [f for f in FINALS if f not in fin_slot]
    assert not missing, missing

    # ---- 校验韵目取字确在本韵之内 ----
    lab_check = []
    for name, core, ref, src, hus in RHYME_TABLE:
        ok = False
        for rec in db:
            for m in rec["meaning"]:
                if m[0] != ref:
                    continue
                p = parse_syllable(re.match(r"^(.*?)([0-9])$", m[0]).group(1))
                if p and fin_slot.get(p[1], (None,))[0] == name:
                    ok = True
        lab_check.append((name, ref, ok))
        if not ok:
            print("!! 韵目取字不在本韵内：", name, ref, file=sys.stderr)

    # ---- 构建韵图结构 ----
    by_rhyme = collections.OrderedDict()
    for name, core, ref, src, hus in RHYME_TABLE:
        by_rhyme[name] = {"name": name, "core": core, "label_read": ref,
                          "src": src, "cls": CLASS_OF[name],
                          "hus": collections.OrderedDict()}
        for hu in HU_ORDER:
            if hu not in hus:
                continue
            entry = {"hu": hu, "desc": HU_DESC[hu], "finals": []}
            for f in hus[hu]:
                entry["finals"].append({"final": f, "ipa": IPA_OF_FINAL[f]})
            by_rhyme[name]["hus"][hu] = entry

    for (ini, fin, tone), v in inst.items():
        name, hu = fin_slot[fin]
        h = by_rhyme[name]["hus"][hu]
        for fe in h["finals"]:
            if fe["final"] == fin:
                fe.setdefault("cells", []).append({
                    "ini": ini, "tone": tone,
                    "ipa": "/".join(sorted(v["ipa"])),
                    "chars": [c for c, s in v["chars"]],
                    "syl": sorted({s + tone for c, s in v["chars"]}),
                })
                break

    # 统计
    stats = {
        "chars": len(db),
        "records": sum(len(r["meaning"]) for r in db),
        "distinct_tone_syllables": len(inst),
        "distinct_base_syllables": len({(i, f) for (i, f, t) in inst}),
        "rhymes": len(RHYME_TABLE),
        "hu_units": sum(len(h) for _, _, _, _, h in RHYME_TABLE),
        "finals": len(FINALS),
        "initials": len(INITIALS),
        "strings_all": len(str_chars),
        "strings_syllable": len(str_tones),
        "strings_untone": [_pair(s) for s in str_untone],
        "strings_word": [_pair(s) for s in str_words],
        "single_total": len(str_tones) + len(str_untone),
        "bad": bad,
    }
    assert len(str_tones) + len(str_untone) + len(str_words) == len(str_chars)

    # ---- 校验：舒声韵只含 1/2/3/5/6，入声韵只含 7/8 ----
    tone_violation = []
    for rh in by_rhyme.values():
        tones = set()
        for h in rh["hus"].values():
            for fe in h["finals"]:
                for c in fe.get("cells", []):
                    tones.add(c["tone"])
        if rh["cls"] == "入聲韻":
            if tones - set(RU_TONES):
                tone_violation.append((rh["name"], "入聲韻含舒聲調", sorted(tones)))
        else:
            if tones & set(RU_TONES):
                tone_violation.append((rh["name"], "舒聲韻含入聲調", sorted(tones)))
    stats["tone_violation"] = tone_violation

    # ---- 代表字 ----
    all_cells = []
    for rh in by_rhyme.values():
        for h in rh["hus"].values():
            for fe in h["finals"]:
                for c in fe.get("cells", []):
                    all_cells.append(c)
    used = set()
    for c in sorted(all_cells, key=lambda x: len(x["chars"])):
        rep = next((ch for ch in c["chars"] if ch not in used), c["chars"][0])
        c["rep"] = rep
        used.add(rep)
    for c in all_cells:
        c.setdefault("rep", c["chars"][0])

    cells_seen = sum(len(fe.get("cells", []))
                     for rh in by_rhyme.values()
                     for h in rh["hus"].values() for fe in h["finals"])
    stats["cells_built"] = cells_seen
    assert cells_seen == len(inst), (cells_seen, len(inst))

    # ---- 呼位一览（韵 × 呼，逐条列出） ----
    hu_units = []
    for name, core, ref, src, hus in RHYME_TABLE:
        rh = by_rhyme[name]
        for hu in HU_ORDER:
            if hu not in hus:
                continue
            fe_list = rh["hus"][hu]["finals"]
            n = sum(len(fe.get("cells", [])) for fe in fe_list)
            hu_units.append({
                "rhyme": name, "core": core, "cls": CLASS_OF[name],
                "hu": hu, "desc": HU_DESC[hu],
                "finals": [fe["final"] for fe in fe_list],
                "ipa": [fe["ipa"] for fe in fe_list],
                "count": n,
            })

    out = {
        "meta": {
            "source": ["https://siqyin.github.io/wugniu_zyinzozin/",
                       "https://github.com/SiqYin/wugniu_suwu"],
            "initials": INITIALS, "initial_order": INITIAL_ORDER,
            "finals": FINALS, "ipa_of_final": IPA_OF_FINAL,
            "tone_info": TONE_INFO, "shu_tones": SHU_TONES, "ru_tones": RU_TONES,
            "hu_order": HU_ORDER, "hu_desc": HU_DESC,
            "class_order": CLASS_ORDER,
            "stats": stats,
        },
        "rhymes": list(by_rhyme.values()),
        "hu_units": hu_units,
        "label_check": lab_check,
    }
    json.dump(out, open(os.path.join(HERE, "yuntu_data.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))

    # ---- 供网页使用的两部分：分韵方案（静态）+ 紧凑字音快照（离线兜底） ----
    scheme = {
        "initials": INITIALS, "initial_order": INITIAL_ORDER, "groups": GROUPS,
        "tone_info": TONE_INFO, "shu_tones": SHU_TONES, "ru_tones": RU_TONES,
        "hu_order": HU_ORDER, "hu_desc": HU_DESC, "class_order": CLASS_ORDER,
        "finals": FINALS, "ipa_of_final": IPA_OF_FINAL,
        "zero_map": ZERO_MAP, "pal_map": PAL_MAP, "plain": PLAIN,
        "rhymes": [{"name": n, "core": c, "cls": CLASS_OF[n], "label_read": r, "src": s,
                    "hus": [{"hu": hu, "finals": [{"final": f, "ipa": IPA_OF_FINAL[f]}
                                                  for f in hus[hu]]}
                            for hu in HU_ORDER if hu in hus]}
                   for n, c, r, s, hus in RHYME_TABLE],
        "live_url": "https://siqyin.github.io/wugniu_zyinzozin/data/DB_suhu.json",
        "dict_url": "https://siqyin.github.io/wugniu_zyinzozin/",
    }
    json.dump(scheme, open(os.path.join(HERE, "scheme.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))

    snap_cells = []
    for rh in by_rhyme.values():
        for h in rh["hus"].values():
            for fe in h["finals"]:
                for c in fe.get("cells", []):
                    seen_c, chars = set(), []
                    for ch in c["chars"]:
                        if ch not in seen_c:
                            seen_c.add(ch)
                            chars.append(ch)
                    snap_cells.append([c["ini"], fe["final"], c["tone"], c["ipa"],
                                       "".join(chars)])
    snapshot = {
        "source": "builtin",
        "chars": stats["chars"], "records": stats["records"],
        "syllables": stats["distinct_tone_syllables"],
        "strings": len(str_chars),
        "untone": [_pair(s) for s in str_untone],
        "words": [_pair(s) for s in str_words],
        "cells": snap_cells,
    }
    json.dump(snapshot, open(os.path.join(HERE, "snapshot.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))

    print("字符数           :", stats["chars"])
    print("读音条目         :", stats["records"])
    print("合法音节(带调)   :", stats["distinct_tone_syllables"])
    print("合法音节(不带调) :", stats["distinct_base_syllables"])
    print("分韵数           :", stats["rhymes"], " / 呼位数:", stats["hu_units"],
          " / 韵母:", stats["finals"])
    print("构拟格位         :", stats["cells_built"])
    print("读音串(去重)     :", stats["strings_all"],
          "= 单音节带调", stats["strings_syllable"],
          "+ 单音节无调", len(str_untone),
          "+ 非单音节", len(str_words))
    print("  无调单音节     :", [_pair(s) for s in str_untone])
    print("  非单音节       :", [_pair(s) for s in str_words])
    print("无法归韵/非单音节:", len(bad))
    for b in bad[:15]:
        print("   ", b)
    print("韵目取字校验:")
    for n, r, ok in lab_check:
        print("   ", n, r, "OK" if ok else "FAIL")


if __name__ == "__main__":
    main()
