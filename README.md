# 蘇滬混合腔韻圖

吳語（蘇州—上海混合腔）的**現代韻圖**。按今音韻基分韻，每韻再分開、合、齊、撮四呼，
一呼一位、一位一圖；每格為一個小韻（＝一個合法音節）。

線上瀏覽：<https://siqyin.github.io/wugniu_yuntu/>

## 分韻方案

以「韻基」（主元音 ＋ 韻尾）為唯一標準，不看中古韻攝。共 **28 韻 / 48 呼位**。

| 類 | 韻（韻基） |
|---|---|
| 陰聲 12 | 泰 ɑ（開合齊）・麻 o̝（開齊）・灰 ᴇ（開合）・豪 ɔ（開齊）・侯 ɤ（開齊）・寒 ø（開合齊）・模 u（合）・魚 y（撮）・支 ʮ（撮）・資 ɿ（齊）・微 iᶽ（齊）・仙 i（齊） |
| 陽聲 6 | 陽 ã（開合齊）・江 ɑ̃（開合齊）・真 ən（開合）・侵 in（齊）・雲 yn（撮）・東 oŋ（開齊） |
| 入聲 6 | 八 aʔ（開合齊撮）・陌 ɑʔ（開齊）・質 əʔ（開合）・雪 ɪʔ（齊）・月 yɪʔ（撮）・屋 oʔ（開齊） |
| 特例 4 | 嘸 m・唔 n・五 ng・而 er（不分開合齊撮） |

- **四呼判定**：介音或主元音為 `u` 者合口，為 `i` 者齊齒，為 `yu`／〔y〕者撮口，餘為開口。
  擦化元音按原型計——〔ɿ〕是〔i〕的擦化故歸齊齒，〔ʮ〕是〔y〕的擦化故歸撮口。
- **舒入分列**：舒聲韻＝聲調 1・2・3・5・6（內部不再分平上去）；
  入聲韻＝聲調 7・8，單獨列出。
- **韻目取字都經過核驗**：每個韻目字都在本韻內確實有該讀音（由 `build_data.py` 斷言）。

## 頁面用法

- **分韻總表**每一格就是一個呼位（如「泰合」「灰開」「豪齊」）。格內的**數字**是該呼位的
  轄字數，點下去會列出該呼位全部的字；再點其中一個小韻，就是該小韻的全部轄字。
- **韻圖**預設全部收合，點韻名才展開該韻的聲母／聲調圖，也可按「全部展開韻圖」一次開完。
- **語言**：右上角可切換 **漢語（繁體中文）／English／日本語**。首次來訪時會依 IP 所在
  地區自動選擇語言（中國大陸、香港、澳門、台灣 → 漢語；日本 → 日本語；其餘 → English），
  也接受 `?lang=wu|en|ja` 參數強制指定。選擇會記在 `localStorage`。
  只有介面文字會翻譯，**具體的字、音值、韻目一律不譯**。

## 檔案

```
index.html              線上頁面本體（資料驅動，開啟時即時抓取線上字音庫）
scheme.json             分韻方案與音節解析規則
snapshot.json           離線快照（抓不到線上字音庫時使用）
yuntu_data.json         韻圖／分韻總表用的整理資料
i18n_data.py            漢語・English・日本語三語介面詞表
firstpaint.txt          首屏會用到的字（由 measure_firstpaint.py 實測產生）
font_report.json        字型分片的 unicode-range 報告（由 make_font.py 產生）
build_data.py           由字典資料產生 scheme.json／snapshot.json／yuntu_data.json
generate_html.py        產生 index.html
make_font.py            產生 fonts/ 底下的字型子集
measure_firstpaint.py   用無頭 Chrome 實測首屏可見字，重寫 firstpaint.txt
fonts/                  霞鶩文楷子集（自託管）
```

重建流程：

```bash
python build_data.py          # 抓線上字音庫 → scheme/snapshot/yuntu_data
python generate_html.py       # → index.html
python make_font.py           # → fonts/*.woff2（輸入沒變會自動跳過）
python measure_firstpaint.py  # 版面或介面文字改過之後，重測首屏字表
```

`make_font.py` 依賴 `firstpaint.txt`；改了介面文字（`i18n_data.py`、頁面模板）之後，
建議照上面的順序再跑一遍 `measure_firstpaint.py` → `make_font.py` → `generate_html.py`。

## 字音資料同步

頁面開啟時會即時讀取
[蘇滬混合腔字音查詢](https://siqyin.github.io/wugniu_zyinzozin/) 的
`data/DB_suhu.json`，在瀏覽器裡重新分韻、重新排圖。
**字音查詢那邊新增字或補上讀音之後，重新整理本頁就會看到最新的字**，不必重新發布。
連不上網路時自動改用頁面內建的離線快照，並顯示提示。

## 字型

頁面用**霞鶩文楷**（LXGW WenKai，SIL OFL 1.1）顯示，因為字典收錄了大量生僻字。
字型由 `make_font.py` 子集化為 woff2 自託管，分三片：

| 檔案 | 內容 | 大小 | 什麼時候下載 |
|---|---|---|---|
| `fonts/wk-ui.woff2` | 首屏會用到的字（介面文字、三語詞表、音系總覽、分韻總表、註釋） | ≈ 0.13 MB | **每次開頁** |
| `fonts/wk-dict.woff2` | 展開韻圖、打開彈窗之後才出現的字典用字 | ≈ 1.95 MB | 第一次展開某個韻時 |
| `fonts/wk-ext.woff2` | 霞鶩文楷收的全部 CJK 字形 | ≈ 7.4 MB | 只有出現前兩片沒有的字時（正常瀏覽不會） |

前兩片共用同一個 `font-family`（`LXGW WenKai`），第三片叫 `LXGW WenKai Fallback`，
排在字型棧後面。

**為什麼首屏只要 0.13 MB**：韻圖預設收合，而收合的內容是 `display:none`，瀏覽器不會為
它抓字型；`firstpaint.txt` 就是分別用 `?lang=wu/en/ja` 載入頁面、走訪「可見」文字節點
實測出來的並集（約 826 字）。展開韻圖時才需要 `wk-dict`，於是首屏不必等 2 MB 的字型。

**精確 unicode-range**：三片的 `unicode-range` 不是整塊 CJK 區段，而是各自 cmap 裡真實
存在的碼位壓縮而成。霞鶩文楷 v1.522 其實缺了本頁的 **104 個擴展 B 區生僻字**（例如
𠞈 𠢍 𠦌 𠩫，多為字典收的罕用字）、2 個上游字典的 PUA 佔位字（`U+E07B`、`U+E0B4`），
以及 `ᵝ U+1D5D`、`ᶽ U+1DBD` 兩個 IPA 修飾字母。因為範圍精確，瀏覽器一遇到這些字就知道
回退字型也幫不上忙，會直接交給系統字型 —— 不會白白下載 6 MB 的 `wk-ext`。

- 那 104 個擴展 B 字：字型棧裡排了幾個專門收擴展 B 的系統字型名稱
  （`SimSun-ExtB`、`MingLiU-ExtB`、`MiSans L3`、`I.Ming`、`HanaMinB`、`BabelStone Han`），
  Windows 使用者通常能直接顯示。
- `ᵝ`／`ᶽ`：頁面在渲染時改寫成上標的 `β`／`ʐ`（`β`、`ʐ` 霞鶩文楷有）。
- 兩個 PUA 字：來自上游字典，任何字型都沒有，維持原樣。

用 `font-display: swap`，字型未到時先以系統字顯示，不會卡住頁面。
字型版權見 `fonts/OFL.txt`。

字庫若新增了生僻字，重跑 `python measure_firstpaint.py && python make_font.py` 即可。

## 發佈

線上網址：**<https://siqyin.github.io/wugniu_yundu/>**

本站以 GitHub Pages 發佈，來源是 **`main` 分支根目錄**（分支模式）。也就是說
**每次 push 到 `main` 就是直接上線**，不需要再跑任何建置步驟。

> `.github/workflows/pages.yml` 是**備用**通道，平時不會自動觸發。
> 只有在想改用 Actions 發佈時，才到 Actions 頁面手動 Run 一次；
> 它會把 Pages 來源切成「GitHub Actions」。分支模式下若讓它在 push 時自動跑，
> `actions/deploy-pages` 會因為來源不符而失敗，所以它只登記了 `workflow_dispatch`。

若要從本機重新發布：

```bash
export GITHUB_TOKEN=ghp_xxx      # classic token，勾 repo + workflow
python publish.py --name wugniu_yundu
```

若倉庫已建好，只想推送（不呼叫 API）：

```bash
python publish.py --no-api --name wugniu_yundu
```

推送預設走 `git@github.com`；若 SSH 不可用，也可直接用權杖經 HTTPS 推送：

```bash
git -c credential.helper= push \
  "https://x-access-token:${GITHUB_TOKEN}@github.com/SiqYin/wugniu_yundu.git" main:main
```

`publish.py` 只從環境變數讀取權杖，不寫入任何檔案，也不會把權杖存進
`.git/config`（remote 一律留 `git@github.com`）。用完請到
<https://github.com/settings/tokens> 撤銷該權杖。

## 授權

- 程式碼與韻圖資料：依原字典專案
- 字型：SIL Open Font License 1.1（見 `fonts/OFL.txt`）
