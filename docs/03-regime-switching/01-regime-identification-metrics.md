---
description: 建立多維宏觀體制量化指標體系：整合標普 500 基準趨勢、CBOE VIX 隱含波動率分區與市場寬度指標（Market Breadth），精準識別市場狀態。
---

# 3.1 市場宏觀狀態與趨勢體制識別（Regime Identification）

> **理論分類**: 宏觀金融計量與市場微觀結構 (Macro Financial Econometrics & Microstructure)  
> **核心概念**: 體制識別 (Regime Identification)、波動率體制 (Volatility Regime)、市場寬度 (Market Breadth)  
> **關聯模組**: [`engine/regime.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/regime.py)  
> **單元測試**: [`tests/test_engine.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/tests/test_engine.py)

---

## 市場非平穩性與單一策略之困境

金融市場不具備平穩性（Non-Stationary）。一個單一靜態策略（例如純動能或純深度價值）必然會經歷長期難以承受的回撤期：動能策略在市場流動性踩踏或反轉崩盤時會遭遇劇烈的「動能崩潰（Momentum Crash）」，而逆勢價值策略在長期強勢趨勢中則過早賣出或在陰跌行情中過早耗盡子彈。

為克服單一策略的死角，本架構引入**雙向體制切換引擎（Regime-Switching Engine）**，將市場量化拆解為三大狀態：
1. **體制一：常態/多頭趨勢環境（Regime 1: Normal / Bull Trend）**；
2. **過渡/中性觀望環境（Transition / Neutral Zone）**；
3. **體制二：極端壓力/恐慌環境（Regime 2: Crisis / Extreme Stress）**。

---

## 宏觀與微觀結構量化指標體系

### 1. 基準指數長期趨勢（Benchmark Trend）

以標普 500 指數 ETF（SPY）作為市場錨點：

$$\text{Regime}_{\text{Trend}} = \begin{cases} 
\text{Bullish (1)}, & \text{if } P_{\text{SPY}, t} > \text{SMA}_{200}(t) \text{ and } \text{SMA}_{200}(t) \ge \text{SMA}_{200}(t-10) \\
\text{Bearish (0)}, & \text{otherwise}
\end{cases}$$

### 2. CBOE 波動率指數隱含狀態（VIX Volatility Regime）

芝加哥期權交易所波動率指數（VIX）代表標普 500 期權的 30 天隱含波動率，被廣泛視為市場的「恐慌指標」：
- **低波常態區（Low-Vol Stability）**： $\text{VIX} < 20$
- **過渡震盪區（Elevated Volatility）**： $20 \le \text{VIX} \le 30$
- **極端恐慌區（Crisis Stress / Liquidity Shock）**： $\text{VIX} > 30$ （若 $\text{VIX} > 40$ ，標誌歷史級別踩踏）

### 3. 美股市場寬度（Market Breadth）

以全市場或標普 500 成分股的淨 52 週新高指標（Net New Highs - Net New Lows, NNH-NNL）作為內生結構動能的深度量度：

$$\text{Breadth Ratio} = \frac{\sum_{i=1}^M \mathbb{I}(P_{i,t} \ge \text{High}_{52W, i})}{\sum_{i=1}^M \mathbb{I}(P_{i,t} \le \text{Low}_{52W, i}) + \epsilon}$$

當 $\text{Breadth Ratio} > 2.0$ 時代表廣度極為健康；當 $\text{Breadth Ratio} < 0.2$ 且創 52 週新低家數爆發時，代表市場進入全面去槓桿期。

---

## 🎯 本節核心要點 (Key Takeaways)

1. **三態劃分消除死角**：市場非二元對立，透過「常態多頭」、「過渡觀望」與「極端恐慌」建立動態因應機制。
2. **SPY 200 SMA 與 VIX 雙核驗證**：價格趨勢與期權隱含波動率相互校驗，防範虛假突破與黑天鵝踩踏。
3. **市場寬度作為內部體質儀表板**：觀察創新高與創新低家數比率，提早察覺指數失真的市場分化現象。

---

## 📚 相關文獻 (References)

- Schwert, G. W. (1989). Why does stock market volatility change over time? *The Journal of Finance*, 44(5), 1115-1153.
- Whaley, R. E. (2000). The investor fear gauge. *The Journal of Portfolio Management*, 26(3), 12-17.

---
👉 **下一節**：閱讀 [3.2 常態環境：右側動能突破交易](02-right-side-momentum-trading.md)
