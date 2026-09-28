# 第四章：非對稱風控系統——剛性停損與極限放寬停利

> 「如果你不能在虧損很小的時候將它截斷，遲早你將面對一個足以終結你職業生涯的巨大黑天鵝。」  
> —— Professional Risk Management Axiom

---

## 4.1 為什麼必須嚴格停損？實證與數學論證

在投資界，「停損（Stop-Loss）」常被散戶誤認為是承認失敗的痛苦行為，甚至有人寄望於「只要不賣就不算賠」的心理防衛機制。然而，在量化金融與實證資產定價的視角下，**剛性停損並非防禦手段，而是主動追求「正偏態肥尾回報」的數學先決條件**。

### 1. 幾何平均報酬率的對稱性破缺（Geometric Compounding Degradation）

資產組合的長期財富增長取決於回報率的幾何平均數（Geometric Mean），而非算術平均數（Arithmetic Mean）。當資產遭受虧損時，恢復初始本金所需的回報率呈現非線性的爆發式增長：

$$R_{\text{recovery}} = \frac{1}{1 - L} - 1 = \frac{L}{1 - L}$$

其中 $L \in (0, 1)$ 為虧損比例。

#### 表 4-1: 虧損幅度與本金回原所需漲幅對照

| 虧損幅度 ($L$) | 恢復本金所需之淨報酬率 ($R_{\text{recovery}}$) | 數學衝擊與組合意涵 |
| :---: | :---: | :--- |
| **-5%** | **+5.26%** | 極易透過常態波動修復 |
| **-10%** | **+11.11%** | 正常的市場修正幅度 |
| **-20%** | **+25.00%** | 需要一個強勢季度的超額回報 |
| **-30%** | **+42.86%** | 需要顯著的大牛市驅動 |
| **-50%** | **+100.00%** | 必須資產翻倍，資本已遭受永久性毀滅性打擊 |
| **-75%** | **+300.00%** | 幾乎無法在常規週期內回本 |
| **-90%** | **+900.00%** | 數學上的統計死局（Statistical Ruin） |

一旦個股跌幅達到 50% 以上，投資人就將自身置於極度脆弱的數學劣勢中。這證明了：**控制單筆最大虧損在極小幅度內，是維繫複利引擎運轉的最高公理**。

---

### 2. 行為金融學視角：Kahneman & Tversky (1979) 展望理論與處置效應

Daniel Kahneman 與 Amos Tversky 於 1979 年在 *Econometrica* 提出的**展望理論（Prospect Theory）**指出了人類非理性決策的兩大特徵：
1. **S 型價值函數（S-Shaped Value Function）**：人們對虧損的敏感度遠大於獲利（損失厭惡係數 $\lambda \approx 2.25$）；
2. **獲利區風險厭惡，虧損區風險尋求**：在面對獲利時，投資人傾向落袋為安（凹函數，Concave）；而在面對虧損時，投資人為了避免兌現痛苦，反而轉變為「風險尋求者（Risk-Seeking）」，傾向死扛套牢甚至盲目攤平（凸函數，Convex）。

Shefrin & Statman (1985) 將此現象定義為**處置效應（Disposition Effect）**：
> 「投資人過早賣出賺錢的贏家股票（Riding Losers and Selling Winners），卻長期死抱虧損的輸家股票。」

這種心理偏誤直接摧毀了投資組合的幾何複利，將策略塑造成「勝率雖高但偶爾大暴賠」的**負偏態（Negative Skewness）**結構。本體系藉由預先設定的剛性停損演算法，將決策權完全移交給代碼，徹底排除處置效應的心理干擾。

---

### 3. 實證文獻：Bessembinder (2018)《Do Stocks Outperform Treasury Bills?》

Hendrik Bessembinder 於 2018 年發表於 *Journal of Financial Economics* 的重磅論文，分析了美國股市自 1926 年至 2016 年長達 90 年間的 26,000 多檔上市個股。該研究得出震驚學界的實證結論：

```
美股近百年全市場 26,000+ 檔個股終身回報分佈 (Bessembinder, 2018)

       佔比
        ^
 58% -> |================================== (跑輸一個月期美國國債 T-Bills)
        |
 38% -> |======================== (跑贏國債，但貢獻淨財富為 0)
        |
  4% -> |=== (僅 4% 超級贏家! 創造自 1926 年以來全部淨超額財富: 35 兆美元!)
        +-------------------------------------------------------------->
```

#### Bessembinder 定理之核心啟示：
1. **極度右偏的分佈（Extreme Positive Skewness）**：美股個股回報分佈並非鐘形常態，而是極度右偏。
2. **大部分個股長期是平庸或毀滅財富的**：超過 58% 的美股在整個生命週期內的總回報率落後於 1 個月期美國國債；個股回報的中位數甚至為負。
3. **極少數超級贏家決定成敗**：整個美國股票市場自 1926 年以來產生的全部淨超額財富（Net Wealth Creation，約 35 萬億美元），**僅僅是由前 4% 的頂尖超級股票（如 Apple, Microsoft, ExxonMobil, Amazon 等）所貢獻**。

> [!CAUTION]
> **嚴格截斷的實證必然性**：  
> 由於你持有的任何一檔個股有超過 96% 的機率並不是那 4% 的超級贏家，**一旦個股價格結構轉弱並觸發停損，必須無條件立即斬斷！** 留著它只會讓平庸或走向衰亡的企業拖垮整體的資本淨值。反之，一旦有幸捕捉到那 4% 的超級贏家，必須極限放寬停利，讓複利乘數效應完全釋放。

---

## 4.2 剛性停損執行框架（Rigid Stop-Loss Rules）

### 1. 波動度調整停損：Wilder (1978) ATR 與吊燈停損法（Chandelier Exit）

傳統固定百分比停損（如「一律跌 5% 或 7% 停損」）忽略了不同標的與不同市場時期的波動率差異。一檔高 Beta 成長股的日常正常隨機雜訊可能就高達 4%，若設定 5% 停損將頻繁遭受「雜訊洗出場（Whipsaw）」；而對於低波動公用事業股，跌 5% 可能已代表重大的基本面破位。

因此，本體系採用 J. Welles Wilder (1978) 的**平均真實波幅（Average True Range, ATR）**進行波動度自適應校準。

#### 真實波幅（True Range, TR）與 ATR 計算：

$$\text{TR}_t = \max\left( \text{High}_t - \text{Low}_t, \, \left|\text{High}_t - \text{Close}_{t-1}\right|, \, \left|\text{Low}_t - \text{Close}_{t-1}\right| \right)$$

$$\text{ATR}_{14}(t) = \frac{1}{14} \sum_{i=0}^{13} \text{TR}_{t-i}$$

#### 初始剛性吊燈停損價位（Initial Chandelier Stop）：

$$\text{StopLoss}_{\text{initial}} = P_{\text{entry}} - K \times \text{ATR}_{14}(t_{\text{entry}})$$

在實務基準中，乘數取 $K = 2.5$。若 $2.5 \times \text{ATR}_{14}$ 的絕對跌幅超過進場價的 8%，則強制收緊至最大上限 8%（防止低波時期轉入極端暴跌時停損距離過寬）。

---

### 2. 組合單筆風險上限：固定比例風險模型（Fixed Fractional Risk Model）

Ralph Vince (1990) 指出，倉位管理的核心不在於單次買多少股，而在於**「這筆交易如果看錯停損，最多只允許損失整體組合 NAV 的多少百分比」**。這即是專業機構的 $R$-風險模型（$R$-Risk Model）。

#### 數學公式：

設投資組合當前總淨值為 $\text{NAV}$，單筆交易允許承擔的最大風險比例為 $R \in [1.0\%, 1.5\%]$：

$$\text{Capital at Risk} = \text{NAV} \times R$$

$$\text{Unit Risk} = P_{\text{entry}} - \text{StopLoss}_{\text{initial}} = K \times \text{ATR}_{14}$$

因此，該標的的**買入股數（Position Shares）**與**部位名目價值（Position Value）**被嚴格鎖定為：

$$\text{Position Shares} (S) = \left\lfloor \frac{\text{NAV} \times R}{P_{\text{entry}} - \text{StopLoss}_{\text{initial}}} \right\rfloor$$

$$\text{Position Value} = S \times P_{\text{entry}} \le \text{Max Allocation Limit} \quad (\text{通常上限為 } 20\% \text{ NAV})$$

> [!WARNING]
> **倉位逆向調節鐵律**：  
> 當標的波動度劇烈（$\text{ATR}$ 很大）時，$\text{Unit Risk}$ 變大，公式會**自動降低**可買入股數 $S$，從而限制總體風險暴露；當標的走勢平穩扎實（$\text{ATR}$ 較小）時，系統才允許分配較大名目部位。這確保了組合中每一筆交易對整體 NAV 的衝擊力是嚴格等權重的。

---

## 4.3 放寬停利與長期持有：右偏肥尾捕捉與多層次移動停利

### 1. 核心邏輯：捕捉正偏態肥尾，杜絕人為預設天花板

許多投資者在股票獲利 10% 或 20% 時便急於獲利了結，這種做法直接阻斷了資本捕捉 Bessembinder 所指出的 4% 超級大贏家（如 10 倍股、20 倍股）的可能性。

**真正的非對稱交易：下行虧損受限於 $-1 \times R$，上行收益必須向 $+5R, +10R, +20R$ 完全敞開！**

```
單筆交易 R-倍數 分佈理想狀態 (Asymmetric Payoff)
頻率
  ^
  |          | (絕大多數看錯交易被嚴厲截斷在 -1R 停損線)
  |          |
  |          |
  |          |                     .   .   . (少數超級大贏家奔馳至 +10R, +20R)
  +----------+----+-----+-----+----+---+---+---> R-倍數
           -1R   0   +1R   +2R  +3R   ... +10R ... +20R
```

### 2. 多層次漸進移動停利機制（Multi-Tiered Trailing Stop）

在放寬停利的架構下，只有在市場結構給出明確的「趨勢枯竭」或「公司基本面質變」訊號時，才進行獲利離場。

#### 表 4-2: 多層次動態離場與停利機制規則表

| 階段位階 | 觸發條件 | 停利防線調整策略 | 離場比例 |
| :--- | :--- | :--- | :--- |
| **第一階段：損益兩平保全** | 浮動獲利達 $+2.0 \times \text{ATR}_{14}$（約 $+1R$） | 將停損價提升至進場成本價（Breakeven Stop） | 0%（鎖定零風險） |
| **第二階段：鎖定底層收益** | 浮動獲利達 $+5.0 \times \text{ATR}_{14}$（約 $+2R \sim +3R$） | 停損點移至「進場價 $+ 2.0 \times \text{ATR}$」或 20 日均線下方 | 0% ~ 20%（視市場流動性） |
| **第三階段：長線主升奔馳** | 股價進入主升段，穩健運行於均線之上 | 採用 **10 週均線（50-day SMA）** 移動防線，只要不跌破持續持有 | 0%（全力持有） |
| **第四階段：趨勢終結離場** | 週收盤價實質跌破 10 週均線達 2% 以上 | 執行技術面戰略停利，出清剩餘多頭部位 | **100% 全面平倉** |
| **基本面質變一票否決** | 季報顯示 FCF 轉負、Sloan 應計比率 $> 0.15$ 或 ROIC 永久性衰退 | 不論當前盈虧或技術形態，立即觸發「基本面平倉」 | **100% 全面平倉** |

---

## 4.4 風控與部位管理綜合決策矩陣與偽代碼

### 表 4-3: 風控與部位管理全生命週期矩陣（Risk & Lifecycle Matrix）

| 交易生命週期節點 | 核心監控變數 | 數學判斷式 / 規則 | 執行動作 |
| :--- | :--- | :--- | :--- |
| **建倉前（Pre-Trade）** | 總組合淨值與波動度 | $\text{UnitRisk} = 2.5 \times \text{ATR}_{14}$ | 計算精確股數 $S = \lfloor \frac{\text{NAV} \times 0.0125}{\text{UnitRisk}} \rfloor$ |
| **持有初（Early Post-Trade）** | 現價 vs 初始停損價 | $P_t \le \text{StopLoss}_{\text{initial}}$ | 剛性平倉市價單出清，鎖定最大虧損 $1.25\%$ NAV |
| **獲利推進（Advancement）** | 浮動收益倍數 | $P_t - P_{\text{entry}} \ge 2.0 \times \text{ATR}_{14}$ | $\text{StopLoss} = \max(\text{StopLoss}, P_{\text{entry}})$ |
| **長線趨勢保護（Trailing）** | 50 日均線位置 | $P_t < \text{SMA}_{50}(t) \times 0.98$ | 跌破中長線趨勢均線，執行趨勢性保護停利 |
| **基本面質變（Fundamental Breach）**| 財報發布更新 | $\text{Sloan} > 0.12 \lor \text{FCF} < 0 \lor F\text{-Score} < 5$ | 護城河受損，無論技術面如何，立刻市價平倉 |

---

### 風控與部位管理演算法偽代碼（Algorithm 4.1: Asymmetric Risk Engine）

```python
# 非對稱部位管理與離場演算法
Function CalculatePositionSize(NAV, EntryPrice, ATR14, RiskFraction=0.0125, MaxAllocationRatio=0.20):
    unit_risk = 2.5 * ATR14
    max_stop_distance = EntryPrice * 0.08
    effective_risk_distance = Min(unit_risk, max_stop_distance)
    
    stop_loss_price = EntryPrice - effective_risk_distance
    target_risk_dollars = NAV * RiskFraction
    
    # 計算買入股數
    shares = Floor(target_risk_dollars / effective_risk_distance)
    
    # 檢查是否超過單檔股票最高資金佔比上限 (例如 20% NAV)
    max_allowed_shares = Floor((NAV * MaxAllocationRatio) / EntryPrice)
    final_shares = Min(shares, max_allowed_shares)
    
    Return final_shares, stop_loss_price

Function ManageOpenPosition(Position, CurrentBar, Financials):
    # 1. 優先檢查基本面是否出現不可逆質變
    If Financials.SloanAccrual > 0.12 Or Financials.TTM_FCF < 0 Or Financials.FScore < 5:
        ExecuteCloseOrder(Position, Reason="FUNDAMENTAL_DETERIORATION")
        Return
        
    current_price = CurrentBar.Close
    
    # 2. 檢查是否觸犯剛性停損
    If current_price <= Position.CurrentStopLoss:
        ExecuteCloseOrder(Position, Reason="RIGID_STOP_LOSS")
        Return
        
    # 3. 檢查移動停損與停利進階更新
    unrealized_profit_atr = (current_price - Position.EntryPrice) / Position.EntryATR
    
    If unrealized_profit_atr >= 2.0 And Position.CurrentStopLoss < Position.EntryPrice:
        # 損益兩平保全
        Position.CurrentStopLoss = Position.EntryPrice
        
    # 4. 檢查長線趨勢均線 (50-day / 10-week SMA) 是否跌破
    sma_50 = CurrentBar.SMA50
    If current_price < 0.98 * sma_50 And unrealized_profit_atr > 3.0:
        ExecuteCloseOrder(Position, Reason="TREND_TRAILING_EXIT")
        Return
```

---

## 4.5 本章文獻清單（References）

- Bessembinder, H. (2018). Do stocks outperform Treasury bills? *Journal of Financial Economics*, 129(3), 440-457.
- Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.
- Shefrin, H., & Statman, M. (1985). The disposition to sell winners too early and ride losers too long: Theory and evidence. *The Journal of Finance*, 40(3), 777-790.
- Vince, R. (1990). *Portfolio Management Formulas: Mathematical Trading Methods for the Futures, Options, and Stock Markets*. John Wiley & Sons.
- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.
