---
description: 索提諾比率（Sortino Ratio）的嚴格數學推導，包含下行偏動差（LPM）、離散/連續型下行偏差（DD）與分母自由度樣本數辨析，並對應 Python 模組實作。
---

# 1.3 索提諾比率的數學嚴格推導與目標函數優化

> **理論分類**: 後現代投資組合理論 (Post-Modern Portfolio Theory, PMPT)  
> **核心概念**: 最小可接受報酬率 ($MAR$)、二階下行偏動差 ($LPM_2$)、下行偏差 ($DD$)、索提諾比率  
> **關聯模組**: [`engine/pmpt.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/pmpt.py)  
> **單元測試**: [`tests/test_engine.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/tests/test_engine.py)

---

## PMPT 的兩大革新

為了根除 MPT 與 Sharpe Ratio 的對稱性缺陷，Frank A. Sortino 與 Kees van der Meer (1991) 以及 Sortino & Price (1994) 正式確立了**後現代投資組合理論（Post-Modern Portfolio Theory, PMPT）**。

PMPT 提出兩項顛覆性革新：
1. **最小可接受報酬率（Minimum Acceptable Return, MAR）**：取代固定的無風險利率 $R_f$ 或歷史均值 $\bar{R}$ ，讓風險錨定於投資人具體的負債端或目標回報。
2. **下行偏差（Downside Deviation, DD）**：僅將報酬率低於 $MAR$ 的部分納入下行風險計算，排除獲利波動對績效評估的無效懲罰。

---

## 數學模型嚴格定義

設隨機變數 $R$ 為資產組合在持有期內的真實連續回報率，其機率密度函數為 $f(R)$ 。投資人設定的最小可接受報酬率為 $MAR$ 。

### 1. 連續型下行偏差（Continuous Downside Deviation）

下行偏差實質上為低於目標門檻的二階下行偏動差（Lower Partial Moment of Order 2, $LPM_2$ ）的平方根：

$$LPM_2(MAR) = \int_{-\infty}^{MAR} (MAR - R)^2 f(R) \, dR$$

$$DD(MAR) = \sqrt{LPM_2(MAR)} = \sqrt{\int_{-\infty}^{MAR} (MAR - R)^2 f(R) \, dR}$$

### 2. 離散型下行偏差（Discrete Downside Deviation）

在實際量化投資分析與歷史回測中，給定長度為 $T$ 的歷史回報觀測序列 $\{R_t\}_{t=1}^T$ ，下行偏差的離散無偏估計形式為：

$$DD = \sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min\left(0, R_t - MAR\right) \right]^2}$$

> [!NOTE]
> **分母自由度與樣本數的學術辨析**：  
> 在部分初階教材中，分母有時被寫為低於 $MAR$ 的期數 $N_{bad}$ 。但在 Sortino & Price (1994) 的正統 PMPT 理論中，**分母必須是總樣本期數** $T$ （或 $T-1$ ），而非僅僅是虧損期數。  
> 原因在於：若除以 $N_{bad}$ ，將無法反映「虧損發生的頻率」。若策略在 100 期中僅有 1 期發生虧損，其整體下行風險在除以總期數 $T$ 後會被顯著稀釋，這忠實體現了策略的高度安全性；反之若除以 $N_{bad}=1$ ，則完全忽略了策略在其他 99 期創造的資本保護能力。

### 3. 索提諾比率（Sortino Ratio）公式

$$\text{Sortino Ratio} = \frac{R_p - MAR}{DD} = \frac{\mathbb{E}[R_p] - MAR}{\sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min\left(0, R_t - MAR\right) \right]^2}}$$

其中：
- $R_p$ ：投資組合在評估期間內的複合年化報酬率或算術預期報酬率；
- $MAR$ ：基準門檻（在實務防禦型美股策略中，通常設為 0%、美國 3 個月短期國債殖利率，或長期通膨率 3%）；
- $DD$ ：以該 $MAR$ 為基準的年化下行標準差。

---

## 程式碼實現：Python 核心演算法

本數學模型在專案核心引擎 [`engine/pmpt.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/pmpt.py) 中的對應實作如下：

```python
import math
from typing import Sequence

def downside_deviation(returns: Sequence[float], mar: float = 0.0) -> float:
    """計算下行偏差 (Downside Deviation / Target Semivariance)
    
    公式: sqrt( (1 / T) * sum( min(0, R_t - MAR)^2 ) )
    """
    if not returns:
        raise ValueError("回報率序列不可為空")
    
    underperform_sq = [min(0.0, r - mar) ** 2 for r in returns]
    return math.sqrt(sum(underperform_sq) / len(returns))

def sortino_ratio(returns: Sequence[float], mar: float = 0.0) -> float:
    """計算索提諾比率 (Sortino Ratio)
    
    公式: (Mean(R) - MAR) / DownsideDeviation
    """
    if not returns:
        raise ValueError("回報率序列不可為空")
    
    dd = downside_deviation(returns, mar)
    mean_return = sum(returns) / len(returns)
    excess_return = mean_return - mar
    
    if dd == 0.0:
        return float('inf') if excess_return > 0 else 0.0
        
    return excess_return / dd
```

---

## 🎯 本節核心要點 (Key Takeaways)

1. **下行偏差是真正風險**：僅將低於 $MAR$ 的二階下行偏動差（ $LPM_2$ ）納入計算，獲利部分完全不計入風險。
2. **總樣本數 $T$ 是關鍵**：分母除以總樣本期數 $T$ 能夠正確認識低頻虧損策略的安全價值。
3. **極限無下行風險處理**：當策略在觀測期內完全無下行虧損時（ $DD=0$ 且超額為正），索提諾比率趨於無限大（ $\infty$ ）。

---

## 📚 相關文獻 (References)

- Sortino, F. A., & van der Meer, R. (1991). Downside risk. *The Journal of Portfolio Management*, 17(4), 27-31.
- Sortino, F. A., & Price, L. N. (1994). Performance measurement in a downside risk framework. *The Journal of Investing*, 3(3), 59-64.

---
👉 **下一節**：閱讀 [1.4 長線持有與非對稱收益輪廓的構建](04-asymmetric-payoff-profile.md)
