# 第二章：標的挑選體系——基本面因子與技術面過濾

> 「價值投資與動能投資並非互斥的信仰，而是不同時間尺度下對基本面真實盈餘品質與價格傳導時滯的度量。」  
> —— Empirical Asset Pricing Insights

---

## 2.1 獲利品質與財務韌性：Sloan 應計、Piotroski F-Score 與 Altman Z-Score

在建構防禦型股票池時，首先面臨的挑戰是企業「會計報表的可信度」與「下行信用破產風險」。實證研究反覆證明，單純依賴歷史每股盈餘（EPS）或本益比（P/E）會掉入嚴重的「價值陷阱（Value Trap）」。本體系透過三道量化防火牆進行基本面初篩。

### 1. Sloan (1996) 應計利潤異象（Accrual Anomaly）

Richard Sloan 於 1996 年發表於 *The Accounting Review* 的經典論文指出：**會計盈餘由現金流與應計利潤（Accruals）兩大部分組成，應計利潤佔比過高的公司，其未來的盈餘持續性（Earnings Persistence）顯著低於以真實營業現金流主導的公司**。市場往往系統性地高估高應計公司的盈餘質量，導致其股價在隨後數期面臨均值回歸與負向超額回報。

#### 數學定義與標準化計算
採用資產負債表法（Balance Sheet Approach）或現金流量表法，資產負債表應計利潤總額定義為：

$$\text{Accruals}_t = (\Delta \text{CA}_t - \Delta \text{Cash}_t) - (\Delta \text{CL}_t - \Delta \text{STD}_t) - \text{Dep}_t$$

為消除公司規模效應，依據 Sloan 經典架構除以期初與期末總資產平均值 $\text{TotalAssets}_{\text{avg}}$：

$$\text{Sloan Accrual Ratio} = \frac{\text{Accruals}_t}{\text{TotalAssets}_{\text{avg}}}$$

其中：
- $\Delta \text{CA}$：流動資產變動額（Change in Current Assets）；
- $\Delta \text{Cash}$：現金及約當現金變動額（Change in Cash and Equivalents）；
- $\Delta \text{CL}$：流動負債變動額（Change in Current Liabilities）；
- $\Delta \text{STD}$：包含於流動負債之短期借款與應付票據變動額（Change in Short-Term Debt）；
- $\text{Dep}$：當期折舊與攤銷費用（Depreciation and Amortization Expense）。

> [!CAUTION]
> **應計利潤過濾門檻**：  
> 當企業的 $\text{Sloan Accrual Ratio} > 0.10$（即應計利潤超過總資產 10%）時，代表企業帳面利潤大量由未變現之應收帳款或存貨積壓灌水而成，該標的一律自選股池剔除。

---

### 2. Piotroski (2000) $F\text{-Score}$ 財務體質篩選模型

史丹佛大學會計學教授 Joseph Piotroski 於 2000 年提出 $F\text{-Score}$ 模型，透過 9 個二元變數（0 或 1）對公司的獲利能力（Profitability）、槓桿與流動性（Leverage, Liquidity and Source of Funds）以及營運效率（Operating Efficiency）進行全面體檢：

#### 表 2-1: Piotroski $F\text{-Score}$ 9 項評分指標拆解

| 維度 | 指標代號 | 財務指標與計算方式 | 評分條件（1分條件） | 經濟意義與審計目的 |
| :--- | :--- | :--- | :--- | :--- |
| **獲利能力 (Profitability)** | $F_1$ | 資產報酬率 $\text{ROA}_t = \frac{\text{Net Income}_t}{\text{Total Assets}_{t-1}}$ | $\text{ROA}_t > 0$ | 確保底層資產具備產生淨正收益能力 |
| | $F_2$ | 營業現金流量 $\text{CFO}_t$ | $\text{CFO}_t > 0$ | 杜絕無現金流入的虛胖帳面利潤 |
| | $F_3$ | $\text{ROA}$ 變動值 $\Delta \text{ROA} = \text{ROA}_t - \text{ROA}_{t-1}$ | $\Delta \text{ROA} > 0$ | 檢驗資本回報之邊際改善動能 |
| | $F_4$ | 盈餘品質（Cash Flow vs Accrual） | $\text{CFO}_t > \text{Net Income}_t$ | 確保現金流高於淨利（排除會計操縱） |
| **槓桿/流動性 (Leverage & Liquidity)** | $F_5$ | 長期槓桿率變動 $\Delta \text{LEV} = \text{LEV}_t - \text{LEV}_{t-1}$ | $\Delta \text{LEV} < 0$ | 長期負債比率下降，降低償債壓力 |
| | $F_6$ | 流動比率變動 $\Delta \text{CR} = \text{CR}_t - \text{CR}_{t-1}$ | $\Delta \text{CR} > 0$ | 短期流動性防禦能力提升 |
| | $F_7$ | 新增股本發行 $\text{EQ\_OFFER}_t$ | 無增發新股（Shares $\le 0$） | 避免每股盈餘被稀釋或透過增資續命 |
| **營運效率 (Operating Efficiency)** | $F_8$ | 毛利率變動 $\Delta \text{Margin} = \text{Margin}_t - \text{Margin}_{t-1}$ | $\Delta \text{Margin} > 0$ | 展現企業產品定價權與成本轉嫁能力 |
| | $F_9$ | 資產周轉率變動 $\Delta \text{Turn} = \text{Turn}_t - \text{Turn}_{t-1}$ | $\Delta \text{Turn} > 0$ | 資本配置效率與庫存銷售周轉提升 |

總評分定義為各子項之和：

$$F\text{-Score} = \sum_{i=1}^9 F_i, \quad F\text{-Score} \in \{0, 1, 2, \dots, 9\}$$

> [!NOTE]
> **選股閾值**：  
> - 常態體制（動能右側交易）：要求 $F\text{-Score} \ge 7$；  
> - 極端壓力體制（左側反向抄底）：要求 $F\text{-Score} \ge 8$（確保標的具備度過流動性寒冬的極致資產負債表韌性）。

---

### 3. Altman (1968) $Z\text{-Score}$ 破產風險過濾

Edward Altman 於 1968 年利用多元判別分析（Multiple Discriminant Analysis, MDA）建立的 $Z\text{-Score}$ 模型，是評估製造業與公用/一般企業違約風險的黃金標竿：

$$Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 0.999 X_5$$

其中：
- $X_1 = \frac{\text{營運資金 (Working Capital)}}{\text{總資產 (Total Assets)}}$：短期流動資本充足度；
- $X_2 = \frac{\text{保留盈餘 (Retained Earnings)}}{\text{總資產 (Total Assets)}}$：長期累積獲利與資本公積蓄積程度；
- $X_3 = \frac{\text{息稅前利潤 (EBIT)}}{\text{總資產 (Total Assets)}}$：真實資產營運獲利產出效率；
- $X_4 = \frac{\text{股票總市值 (Market Value of Equity)}}{\text{總負債 (Total Liabilities)}}$：股權價值對債務本金的緩衝覆蓋倍數；
- $X_5 = \frac{\text{營業收入 (Sales)}}{\text{總資產 (Total Assets)}}$：資產周轉倍數。

#### 判定分區與策略規則：
- **安全區（Safe Zone）**：$Z > 2.99$ —— 財務健全，破產機率極低（合規准入）；
- **灰色警戒區（Gray Zone）**：$1.81 \le Z \le 2.99$ —— 需進一步檢視現金流；
- **危險困境區（Distress Zone）**：$Z < 1.81$ —— **一票否決，嚴格禁止進入投資池**。

---

## 2.2 競爭優勢與資本回報：Fama-French 五因子、ROIC 與 FCF Yield

### 1. Fama & French (2015) 五因子模型之啟示

Eugene Fama 與 Kenneth French 於 2015 年在三因子基礎上擴充為五因子模型：

$$\mathbb{E}[R_{it}] - R_{ft} = \alpha_i + \beta_{i1} \text{MKT}_t + \beta_{i2} \text{SMB}_t + \beta_{i3} \text{HML}_t + \beta_{i4} \text{RMW}_t + \beta_{i5} \text{CMA}_t + \epsilon_{it}$$

其中核心貢獻為：
- **獲利因子（$\text{RMW}_t$, Robust Minus Weak）**：高營運獲利率（Robust Profitability）企業長期系統性跑贏低營運獲利率（Weak Profitability）企業；
- **投資因子（$\text{CMA}_t$, Conservative Minus Aggressive）**：保守再投資（Conservative Investment）企業長期系統性跑贏激進資本擴張（Aggressive Investment）企業。

實證結果清楚揭示：盲目進行低效併購與激進資本支出的企業會摧毀股東權益，而具備深厚經濟護城河、穩健再投資且具備優異獲利能力的公司，能持續產生超額阿爾法。

### 2. 投入資本回報率（ROIC）與自由現金流收益率（FCF Yield）

為了精確量化 RMW 與 CMA 在微觀企業層級的表現，策略引入兩大核心門檻：

#### 投入資本回報率（Return on Invested Capital, ROIC）

$$\text{ROIC} = \frac{\text{NOPAT}}{\text{Invested Capital}} = \frac{\text{EBIT} \times (1 - \tau)}{(\text{Total Debt} + \text{Shareholders' Equity} - \text{Excess Cash})}$$

其中 $\tau$ 為邊際企業所得稅率。  
**選拔門檻**：近 3 年平均 $\text{ROIC} \ge 15\%$，且 $\text{ROIC} > \text{WACC}$（加權平均資本成本），確保公司處於真正的股東價值創造（Economic Value Added, EVA）區間。

#### 自由現金流收益率（Free Cash Flow Yield）

$$\text{FCF Yield} = \frac{\text{FCF}}{\text{Enterprise Value}} = \frac{\text{CFO} - \text{CapEx}}{\text{Market Cap} + \text{Net Debt}}$$

**選拔門檻**：持續 3 年 $\text{FCF} > 0$，且過去 12 個月（TTM）$\text{FCF Yield} \ge 4.0\%$（極端高成長板塊至少 $\text{FCF Yield} \ge 2.0\%$）。

---

## 2.3 技術面輔助驗證：Stan Weinstein 四階段與 200 SMA 趨勢濾網

純粹的基本面分析存在顯著的「時機鈍化」問題——優質公司可能在長達數年的時間內處於橫盤消化期或市場冷遇期。本架構以經典技術結構理論作為入場時機濾網。

### 1. Stan Weinstein (1988) 四階段市場週期分析（Stage Analysis）

Weinstein 將股票市場走勢劃分為四個本質截然不同的生命週期階段：

```
股價 P
  ^
  |                                        Stage 3: 做頭/分配期 (Distribution)
  |                                      /--------------------\
  |             Stage 2: 主升段         /                      \
  |             (Advancing Stage)      /                        \
  |                   /               /                          \  Stage 4: 主跌段
  |                  /               /                            \ (Declining Stage)
  |                 /               /                              \
  |                /               /                                \
  |  -------------+---------------+                                  \
  |  Stage 1: 打底期 (Basing)                                         \-------
  +----------------------------------------------------------------------------> 時間 t
      30-week / 200-day Moving Average (均線由走平轉為上揚)
```

| 階段名稱 | 均線走勢（200-day SMA / 30-week MA） | 交易量與結構特徵 | 策略執行動作 |
| :--- | :--- | :--- | :--- |
| **Stage 1: 打底期** | 長期均線走平，股價在均線上下窄幅震盪 | 交易量萎縮，買賣雙方趨於均衡 | 列入觀察名單，**嚴禁提前重倉進場** |
| **Stage 2: 主升段** | 均線明確向上傾斜，股價穩定站於均線之上 | 突破時伴隨顯著放大成交量，回測支撐不破 | **唯一的右側策略標準進場階段** |
| **Stage 3: 做頭期** | 均線再度走平，波動率劇增，頻現長上下影線 | 高檔爆量不漲，籌碼由機構流向散戶 | 嚴禁新開倉，收緊停利防線 |
| **Stage 4: 主跌段** | 均線向下傾斜，股價持續受制於均線下方 | 反彈皆為弱勢，持續破底 | **嚴禁任何買入操作，若持有無條件離場** |

### 2. Brock, Lakonishok, & LeBaron (1992) 200 日移動平均線（200-day SMA）

William Brock、Josef Lakonishok 與 Blake LeBaron 於 1992 年發表於 *The Journal of Finance* 的里程碑實證研究《Simple Technical Trading Rules and the Stochastic Properties of Stock Returns》，運用道瓊工業指數長達 90 年的數據，證實以 200 日移動平均線為代表的移動平均規則具備高度顯著的非隨機預測力。

#### 數學定義與操作鐵律：

$$\text{SMA}_{200}(t) = \frac{1}{200} \sum_{k=0}^{199} P_{t-k}$$

$$\text{Trend Filter Condition}: \quad P_t > \text{SMA}_{200}(t) \quad \text{AND} \quad \frac{d}{dt}\text{SMA}_{200}(t) > 0$$

> [!WARNING]
> **趨勢絕對濾網**：  
> 在常態多頭體制中，若標的股票現價 $P_t < \text{SMA}_{200}(t)$，無論其本益比多便宜、基本面評分多優異，**一律嚴禁建立右側多頭部位**，徹底排除「試圖在主跌浪中接飛刀」的人性弱點。

---

## 2.4 多維度標的初篩決策矩陣與演算法偽代碼

### 表 2-2: 全方位標的初篩綜合決策矩陣（Screening Decision Matrix）

| 檢驗層次 | 檢驗模組 | 指標名稱 | 嚴格准入條件 (Pass Criteria) | 違規處理動作 |
| :--- | :--- | :--- | :--- | :--- |
| **第一層：會計品質** | Sloan (1996) | 應計比率 (Accrual Ratio) | $\text{Accrual Ratio} \le 0.10$ | 剔除標的（盈餘操縱風險） |
| **第二層：信用韌性** | Altman (1968) | $Z\text{-Score}$ | $Z > 2.99$（極限寬限至 $Z \ge 1.81$） | $Z < 1.81$ 立即一票否決 |
| **第三層：經營體質** | Piotroski (2000) | $F\text{-Score}$ | 常態體制 $\ge 7$；恐慌體制 $\ge 8$ | 未達標則不予放行 |
| **第四層：資本回報** | Fama-French | $\text{ROIC}$ & $\text{FCF Yield}$ | 3 年均 $\text{ROIC} \ge 15\%$ 且 $\text{FCF} > 0$ | 剔除標的（缺乏護城河） |
| **第五層：市場階段** | Weinstein (1988) | Stage 週期分析 | 處於 Stage 2 突破或延續 | Stage 1 觀察，Stage 3/4 剔除 |
| **第六層：長線趨勢** | Brock et al. (1992) | 200-day SMA | $P_t > \text{SMA}_{200}$ 且斜率為正 | 違背則右側禁開倉 |

---

### 篩選演算法偽代碼（Algorithm 2.1: Multi-Factor Screening Pipeline）

```python
# 標的挑選多維過濾演算法 (Screening Pipeline)
Input: Universe_US_Equities, HistoricalFinancials, PriceSeries
Output: Approved_Universe_Regime1, Approved_Universe_Regime2

Function EvaluateAssetSelection(StockList):
    Approved_Regime1 = []
    Approved_Regime2 = []
    
    For Each Stock In StockList:
        # 1. 會計品質與破產風險初篩
        sloan_ratio = CalculateSloanAccrual(Stock)
        z_score = CalculateAltmanZScore(Stock)
        f_score = CalculatePiotroskiFScore(Stock)
        
        If sloan_ratio > 0.10 Or z_score < 1.81:
            Continue # 存在財務或破產威脅，跳過
            
        # 2. 資本回報與護城河檢驗
        roic_3y_avg = CalculateAvgROIC(Stock, years=3)
        fcf_positive = All(Stock.FCF[t] > 0 For t In Last3Years)
        
        If roic_3y_avg < 0.15 Or Not fcf_positive:
            Continue # 資本配置效率不足，跳過
            
        # 3. 體制一：常態多頭（右側進場）驗證
        sma_200 = MovingAverage(Stock.Close, window=200)
        is_above_200sma = (Stock.Close[-1] > sma_200[-1]) And (sma_200[-1] > sma_200[-20])
        is_stage_2 = DetectWeinsteinStage2(Stock.Close, sma_200)
        
        If f_score >= 7 And is_above_200sma And is_stage_2:
            Approved_Regime1.Append(Stock)
            
        # 4. 體制二：極端壓力（左側價值積累）候選清單
        # 極端價值條件：不要求突破 200 SMA，但要求 F-Score >= 8 且 Z-Score > 2.99
        If f_score >= 8 And z_score > 2.99:
            Approved_Regime2.Append(Stock)
            
    Return Approved_Regime1, Approved_Regime2
```

---

## 2.5 本章文獻清單（References）

- Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *The Journal of Finance*, 23(4), 589-609.
- Brock, W., Lakonishok, J., & LeBaron, B. (1992). Simple technical trading rules and the stochastic properties of stock returns. *The Journal of Finance*, 47(5), 1731-1764.
- Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1-22.
- Piotroski, J. D. (2000). Value investing: The use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38, 1-41.
- Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows about future earnings? *The Accounting Review*, 71(3), 289-315.
- Weinstein, S. (1988). *Stan Weinstein's Secrets for Profiting in Bull and Bear Markets*. McGraw-Hill.
