# 第一章：核心哲學——後現代投資組合理論與索提諾比率

> 「投資組合的真正風險，絕非源於資產價格向上暴漲時帶來的波動，而是來自於資本永久性虧損與無法達成財務目標的下行衝擊。」  
> —— Frank A. Sortino (1994)

---

## 1.1 現代投資組合理論（MPT）與夏普比率的內在缺陷

自 Harry Markowitz 於 1952 年發表里程碑式的論文《Portfolio Selection》以來，現代投資組合理論（Modern Portfolio Theory, 簡稱 MPT）奠定了過去半個世紀學院派與華爾街資產配置的基石。Markowitz 框架建立於均值-變異數（Mean-Variance Optimization, MVO）之上，其核心假設可歸結為兩大公理：
1. 投資人為風險厭惡者（Risk-Averse），在給定預期回報下追求變異數極小化；或在給定變異數下追求預期回報極大化；
2. 資產回報率向量服從多元聯合常態分佈（Multivariate Normal Distribution），從而資產組合的分佈特徵可完全由前兩階動差——均值（Mean, $\mu$）與變異數（Variance, $\sigma^2$）——充分表徵。

基於此架構，William Sharpe 於 1966 年提出了廣為人知的夏普比率（Sharpe Ratio, 原名 Reward-to-Variability Ratio）：

$$\text{Sharpe Ratio} = \frac{\mathbb{E}[R_p] - R_f}{\sigma_p}$$

其中，$\mathbb{E}[R_p]$ 為投資組合預期報酬率，$R_f$ 為無風險利率（Risk-Free Rate），$\sigma_p = \sqrt{\mathrm{Var}(R_p)}$ 為投資組合總回報的標準差。

### 夏普比率的統計偏誤：將「獲利波動」視為懲罰因子

在數學公式中，分母 $\sigma_p$ 的定義為：

$$\sigma_p = \sqrt{\frac{1}{T-1} \sum_{t=1}^T \left( R_{p,t} - \bar{R}_p \right)^2}$$

這意味著無論個別時期的回報 $R_{p,t}$ 是遠高於均值（狂飆獲利）還是遠低於均值（慘重崩跌），在經過離均差平方 $(R_{p,t} - \bar{R}_p)^2$ 的計算後，皆被無差別地賦予正向懲罰。

> [!WARNING]
> **對稱風險懲罰的悖論**：  
> 假設存在兩組策略 A 與 B：
> - **策略 A**：每月穩定獲利 1%，波動極低（標準差 $\sigma_A \approx 0.1\%$），幾乎無暴賺亦無暴賠。
> - **策略 B**：在保持下行受控（從不單月虧損超過 1%）的前提下，經常出現單月 +15%、+25% 的非對稱暴賺。
> 
> 在 MPT 與 Sharpe Ratio 的計算中，策略 B 由於上行爆發力帶來極高的樣本總變異數 $\sigma_B$，其計算出的夏普比率可能遠遠低於平庸的策略 A。這在經濟學與真實投資心理上是荒謬的——**理性投資人從不畏懼資產向上暴漲帶來的「波動」，他們唯一恐懼的是資產跌破安全底線的「下行虧損」**。

---

## 1.2 金融肥尾與非對稱分佈：高斯假設的崩潰

Markowitz 框架的第二個致命盲點在於常態分佈假設。Benoit Mandelbrot (1963) 在對棉花期貨與資產價格變動的開創性研究中首次指出：金融資產價格回報絕非高斯分佈，而是呈現顯著的「列維穩定分佈（Lévy Stable Distribution）」或稱**厚尾/肥尾特性（Fat Tails, Leptokurtosis）**。Eugene Fama (1965) 隨後在股票市場的研究中進一步證實了極端值發生的頻率遠高於常態分佈預測。

### 常態分佈 vs 實際金融回報分佈之對比

| 分佈統計特徵 | 高斯常態分佈（MPT 假設） | 實際金融資產分佈（Empirical Reality） | 策略意義與潛在危害 |
| :--- | :--- | :--- | :--- |
| **偏態（Skewness, $S$）** | $S = 0$（嚴格左右對稱） | $S \neq 0$（美股個股偏右偏態，宏觀指數偏左偏態） | 對稱模型忽視了極端下行崩盤（Crash Risk）的衝擊 |
| **峰態（Kurtosis, $K$）** | $K = 3$（無超額峰度） | $K \gg 3$（超額厚尾 Leptokurtic） | 3 個標準差（$3\sigma$）以上的極端黑天鵝事件頻率高出理論值數百倍 |
| **二階動差充分性** | 均值與變異數即決定全部資訊 | 必須考量高階動差（偏態、峰度與下行半變異數） | 依賴變異數優化將導致組合在系統性危機中遭受毀滅性打擊 |

```
機率密度 f(R)
      ^
      |             /|           --- 實際金融回報（尖峰肥尾，Leptokurtic）
      |            / |           ... 常態高斯分佈（Normal Distribution）
      |          /   | \
      |         /  . | . \
      |        / .   |   . \
      |       / .    |    . \
      |     /  .     |     .  \
      |   /    .     |     .    \
  ____|_/______._____|_____.______\______> 回報率 R
    左尾極端虧損        均值        右尾極端暴利
  （黑天鵝頻發區）
```

當資產回報分佈偏離常態時，變異數失去了作為風險度量尺規的正當性。特別是在具備「嚴格停損、極度放寬停利」的非對稱交易體系中，回報分佈被人為地塑造成顯著的**正偏態（Positive Skewness）**。在此情境下，若沿用夏普比率評估策略績效，將導致嚴重的模型誤判與無效去槓桿。

---

## 1.3 索提諾比率的數學嚴格推導與目標函數優化

為了根除 MPT 與 Sharpe Ratio 的對稱性缺陷，Frank A. Sortino 與 Kees van der Meer (1991) 以及 Sortino & Price (1994) 正式確立了**後現代投資組合理論（Post-Modern Portfolio Theory, PMPT）**。

PMPT 提出兩項顛覆性革新：
1. 以投資人自訂的**最小可接受報酬率（Minimum Acceptable Return, 簡稱 $MAR$）**取代固定的無風險利率 $R_f$ 或歷史均值 $\bar{R}$；
2. 僅將報酬率低於 $MAR$ 的部分納入下行風險計算，定義為**下行偏差（Downside Deviation, $DD$）**或目標下半變異數（Target Semivariance）。

### 數學模型嚴格定義

設隨機變數 $R$ 為資產組合在持有期內的真實連續回報率，其機率密度函數為 $f(R)$。投資人設定的最小可接受報酬率為 $MAR$。

#### 1. 連續型下行偏差（Continuous Downside Deviation）
下行偏差實質上為低於目標門檻的二階下行偏動差（Lower Partial Moment of Order 2, $LPM_2$）的平方根：

$$LPM_2(MAR) = \int_{-\infty}^{MAR} (MAR - R)^2 f(R) \, dR$$

$$DD(MAR) = \sqrt{LPM_2(MAR)} = \sqrt{\int_{-\infty}^{MAR} (MAR - R)^2 f(R) \, dR}$$

#### 2. 離散型下行偏差（Discrete Downside Deviation）
在實際量化投資分析與歷史回測中，給定長度為 $T$ 的歷史回報觀測序列 $\{R_t\}_{t=1}^T$，下行偏差的離散無偏估計形式為：

$$DD = \sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min\left(0, R_t - MAR\right) \right]^2}$$

> [!NOTE]
> **分母自由度與樣本數的學術辨析**：  
> 在部分初階教材中，分母有時被寫為低於 $MAR$ 的期數 $N_{bad}$。但在 Sortino & Price (1994) 的正統 PMPT 理論中，**分母必須是總樣本期數 $T$**（或 $T-1$），而非僅僅是虧損期數。  
> 原因在於：若除以 $N_{bad}$，將無法反映「虧損發生的頻率」。若策略在 100 期中僅有 1 期發生虧損，其整體下行風險在除以總期數 $T$ 後會被顯著稀釋，這忠實體現了策略的高度安全性；反之若除以 $N_{bad}=1$，則完全忽略了策略在其他 99 期創造的資本保護能力。

#### 3. 索提諾比率（Sortino Ratio）公式

$$\text{Sortino Ratio} = \frac{R_p - MAR}{DD} = \frac{\mathbb{E}[R_p] - MAR}{\sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min\left(0, R_t - MAR\right) \right]^2}}$$

其中：
- $R_p$ 為投資組合在評估期間內的複合年化報酬率或算術預期報酬率；
- $MAR$ 為基準門檻（在實務防禦型美股策略中，通常設為 0%、美國 3 個月短期國債殖利率，或長期通膨率 3%）；
- $DD$ 為以該 $MAR$ 為基準的年化下行標準差。

---

## 1.4 目標函數：長線買入持有與非對稱收益輪廓的構建

在傳統投資實務中，「買入並持有（Buy and Hold, B&H）」策略常被批評為缺乏防禦性，因其完全暴露於大盤系統性崩盤（如 1929、2000、2008 年）的深淵之中；而「高頻主動交易」則因高昂的換手成本（Turnover Costs）、滑點（Slippage）以及繳稅摩擦，長期損耗幾何複利。

本書提出的架構旨在透過後現代投資組合優化，將**長線持有的低摩擦優勢**與**下行截斷的非對稱性**融合。

### 資產配置的最優化目標函數

對於由 $N$ 檔美股構成的投資權重向量 $\mathbf{w} = [w_1, w_2, \dots, w_N]^T$，傳統 Markowitz 的目標函數為：

$$\max_{\mathbf{w}} \quad \mathbf{w}^T \boldsymbol{\mu} - \frac{\lambda}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} \quad \text{s.t.} \quad \sum_{i=1}^N w_i = 1, \; w_i \ge 0$$

而後現代非對稱防禦型架構的目標函數定義為：

$$\max_{\mathbf{w}} \quad \text{Sortino}(\mathbf{w}; MAR) = \frac{\mathbf{w}^T \boldsymbol{\mu} - MAR}{\sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min\left(0, \mathbf{w}^T \mathbf{R}_t - MAR\right) \right]^2}}$$

$$\text{Subject to:} \quad \sum_{i=1}^N w_i \le 1, \quad 0 \le w_i \le w_{\max}, \quad \forall i$$

```
收益輪廓對比 (Payoff Profile)
組合收益
  ^
  |                                       / (非對稱防禦策略: 捕捉正偏態肥尾)
  |                                      /
  |                                     /
  |                                    /  . (傳統對稱均值-變異數組合)
  |                                   / .
  |                                  /.
  |                                 /
  |--------------------------------+----------------------------> 市場基準收益
  |                              / |
  |                             /  |
  | (剛性停損截斷左側極端虧損)    /   |
  |=============================   |
  |                                |
  |                                |
  v
```

### 非對稱收益的分佈特徵：工程實現途徑

要使得投資組合的實證分佈具備上述「左側截斷、右側無限肥尾」的正偏態幾何特徵，系統必須依賴三個有機鏈結的模組協同運作：
1. **優質資產過濾（Chapter 2）**：挑選出具備定價權、極高投入資本回報率（ROIC）與真實真實現金流支撐的頂級企業，確保資產在長期持有時內生價值持續增長；
2. **體制切換引擎（Chapter 3）**：在市場趨勢健康時順勢捕捉動能，在極端黑天鵝降臨時不盲目割肉，而是切入左側價值積累；
3. **剛性與放寬風控（Chapter 4）**：一旦個股判斷錯誤跌破波動度防護罩，立即嚴厲停損（Truncate Left Tail）；一旦趨勢確立，絕不預設天花板，放任獲利奔馳（Let Profits Run）。

---

## 1.5 本章文獻清單（References）

- Fama, E. F. (1965). The behavior of stock-market prices. *The Journal of Business*, 38(1), 34-105.
- Mandelbrot, B. (1963). The variation of certain speculative prices. *The Journal of Business*, 36(4), 394-419.
- Markowitz, H. (1952). Portfolio selection. *The Journal of Finance*, 7(1), 77-91.
- Sharpe, W. F. (1966). Mutual fund performance. *The Journal of Business*, 39(1), 119-138.
- Sortino, F. A., & van der Meer, R. (1991). Downside risk. *The Journal of Portfolio Management*, 17(4), 27-31.
- Sortino, F. A., & Price, L. N. (1994). Performance measurement in a downside risk framework. *The Journal of Investing*, 3(3), 59-64.
