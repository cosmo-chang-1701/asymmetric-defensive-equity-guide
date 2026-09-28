---
description: 放寬停利與長期持有哲學：建立四階段漸進式移動停利架構（損益兩平、底層鎖定、長線均線護航、趨勢終結與基本面質變一票否決），全力捕捉正偏態超級肥尾。
---

# 4.3 放寬停利與長期持有：右偏肥尾捕捉與多層次移動停利

> **理論分類**: 非對稱期望值理論與動態離場機制 (Asymmetric Expectancy & Trailing Exits)  
> **核心概念**: 正偏態肥尾 (Positive Skewness)、R-倍數期望值、多層次移動停利 (Multi-Tiered Trailing Stop)  
> **關聯模組**: [`engine/risk.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/risk.py)  
> **單元測試**: [`tests/test_engine.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/tests/test_engine.py)

---

## 核心邏輯：捕捉正偏態肥尾，杜絕人為預設天花板

許多投資者在股票獲利 10% 或 20% 時便急於獲利了結，這種做法直接阻斷了資本捕捉 Bessembinder 所指出的 4% 超級大贏家（如 10 倍股、20 倍股）的可能性。

**真正的非對稱交易：下行虧損受限於** $-1 \times R$ ，**上行收益必須向** $+5R, +10R, +20R$ **完全敞開！**

```mermaid
flowchart LR
    subgraph AsymmetricPayoff["非對稱 R-倍數 分佈理想狀態"]
        direction LR
        Cut["96% 看錯部位<br/>被剛性截斷在 -1R 停損線 ✂️"]
        Wait["持平震盪部位<br/>損益兩平保全 (0R) 🛡️"]
        Win["4% 超級大贏家<br/>長線奔馳至 +10R ~ +20R 🚀"]
    end
    Cut --> Wait
    Wait --> Win
```

---

## 多層次漸進移動停利機制（Multi-Tiered Trailing Stop）

在放寬停利的架構下，只有在市場結構給出明確的「趨勢枯竭」或「公司基本面質變」訊號時，才進行獲利離場。

### 表 4-2: 多層次動態離場與停利機制規則表

| 階段位階 | 觸發條件 | 停利防線調整策略 | 離場比例 |
| :--- | :--- | :--- | :--- |
| **第一階段：損益兩平保全** | 浮動獲利達 $+2.0 \times \text{ATR}_{14}$ （約 $+1R$ ） | 將停損價提升至進場成本價（Breakeven Stop） | 0%（鎖定零風險） |
| **第二階段：鎖定底層收益** | 浮動獲利達 $+5.0 \times \text{ATR}_{14}$ （約 $+2R \sim +3R$ ） | 停損點移至「進場價 $+ 2.0 \times \text{ATR}$ 」或 20 日均線下方 | 0% ~ 20%（視市場流動性） |
| **第三階段：長線主升奔馳** | 股價進入主升段，穩健運行於均線之上 | 採用 **10 週均線（50-day SMA）** 移動防線，只要不跌破持續持有 | 0%（全力持有） |
| **第四階段：趨勢終結離場** | 週收盤價實質跌破 10 週均線達 2% 以上 | 執行技術面戰略停利，出清剩餘多頭部位 | **100% 全面平倉** |
| **基本面質變一票否決** | 季報顯示 FCF 轉負、Sloan 應計比率 $> 0.15$ 或 ROIC 永久性衰退 | 不論當前盈虧或技術形態，立即觸發「基本面平倉」 | **100% 全面平倉** |

---

## 🎯 本節核心要點 (Key Takeaways)

1. **不預設獲利目標價**：偉大的趨勢從不設限，過早獲利了結是摧毀非對稱期望值的頭號元兇。
2. **獲利推進自適應保護**：一旦獲利達 2x ATR 即刻將防線移至成本價，消除單筆持倉的本金下行風險。
3. **50 日 SMA 作為長線護航者**：只要標的價格尊重中長線上升趨勢線，就堅定持有，坐享複利滾雪球。

---

## 📚 相關文獻 (References)

- Bessembinder, H. (2018). Do stocks outperform Treasury bills? *Journal of Financial Economics*, 129(3), 440-457.
- Vince, R. (1990). *Portfolio Management Formulas: Mathematical Trading Methods for the Futures, Options, and Stock Markets*. John Wiley & Sons.

---
👉 **下一節**：閱讀 [4.4 風控與部位管理全生命週期矩陣](04-lifecycle-risk-matrix.md)
