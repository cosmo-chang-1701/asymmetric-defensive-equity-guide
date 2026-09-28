---
description: 附錄 A：下行偏差、下行偏動差（LPM）與幾何平均複利損耗之嚴格數學推導，揭示波動率拖累定理（Volatility Drag）之幾何本質。
---

# 附錄 A：下行偏差與偏動差（LPM）嚴格數學推導

> **理論分類**: 測度機率論與隨機金融數學 (Probability Measures & Mathematical Finance)  
> **核心概念**: 下行偏動差 ($LPM_n$)、目標下半變異數、幾何平均二階泰勒展開、波動率拖累定理  
> **關聯模組**: [`engine/pmpt.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/pmpt.py)

---

## A.1 下行偏差（Downside Deviation）與偏動差（LPM）之嚴格數學推導

在一般化的動差理論中，任何階數 $n$ 的下行偏動差（Lower Partial Moment of Order $n$, $LPM_n$）以目標報酬率 $\tau$（即最小可接受報酬率 $MAR$）為基準，定義於隨機變數 $R \sim f(R)$ 之概率空間：

$$LPM_n(\tau) = \mathbb{E}\left[ \max(0, \tau - R)^n \right] = \int_{-\infty}^{\tau} (\tau - R)^n f(R) \, dR$$

### 階數經濟意義解析：
- **$n = 0$**：$LPM_0(\tau) = \int_{-\infty}^{\tau} f(R) \, dR = F(\tau) = \mathbb{P}(R < \tau)$，即未達標機率（Shortfall Probability）；
- **$n = 1$**：$LPM_1(\tau) = \int_{-\infty}^{\tau} (\tau - R) f(R) \, dR$，即預期未達標幅度（Expected Shortfall / Target Shortfall）；
- **$n = 2$**：$LPM_2(\tau) = \int_{-\infty}^{\tau} (\tau - R)^2 f(R) \, dR$，即目標下半變異數（Target Semivariance）。

### 索提諾下行偏差（Downside Deviation, $DD$）
定義為二階偏動差的開方：

$$DD(\tau) = \sqrt{LPM_2(\tau)}$$

當離散採樣 $t = 1, 2, \dots, T$ 且各觀測值獨立同分佈（i.i.d.）時，其樣本估計量為：

$$DD = \sqrt{\frac{1}{T} \sum_{t=1}^T \left[ \min(0, R_t - \tau) \right]^2}$$

---

## A.2 幾何平均收益與複利損耗推導

設投資組合在第 $t$ 期的簡單報酬率為 $R_t$。若初始本金為 $W_0$，經過 $T$ 期後的終值 $W_T$ 為：

$$W_T = W_0 \prod_{t=1}^T (1 + R_t)$$

其幾何平均報酬率（Compound Annual Growth Rate, CAGR）定義為：

$$R_G = \left( \prod_{t=1}^T (1 + R_t) \right)^{1/T} - 1$$

透過二階泰勒展開式（Taylor Expansion），設算術平均值為 $\mu = \frac{1}{T}\sum R_t$，樣本變異數為 $\sigma^2$：

$$\ln(1 + R_t) \approx R_t - \frac{1}{2} R_t^2$$

對兩邊取期望值：

$$\mathbb{E}[\ln(1 + R_t)] \approx \mu - \frac{1}{2} (\sigma^2 + \mu^2) \approx \mu - \frac{1}{2} \sigma^2$$

從而幾何平均報酬率近似為：

$$R_G \approx \mu - \frac{1}{2} \sigma^2$$

> [!NOTE]
> **波動率拖累（Volatility Drag）定理**：  
> 幾何複利回報等於算術平均回報減去**變異數的一半（$\frac{1}{2}\sigma^2$）**。這從根本上解釋了為何一次 -50% 的暴跌會永久性摧毀長達數年的複利積累：因為下行極端負收益會極度膨脹變異數 $\sigma^2$，直接把 $R_G$ 拖入負值深淵。

---

## 🎯 本節核心要點 (Key Takeaways)

1. **二階偏動差是數學本體**：索提諾比率的下行偏差不是經驗統計指標，而是堅實的 $LPM_2$ 機率測度。
2. **波動率拖累是財富殺手**：變異數 $\sigma^2$ 的一半直接從幾何回報中扣除，證明防範大跌比追求暴賺更能積累財富。

---
👉 **下一單元**：查閱 [附錄 B：系統全流程量化參數與敏感度速查表](02-parameter-cheat-sheet.md)
