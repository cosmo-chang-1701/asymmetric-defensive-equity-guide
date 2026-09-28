---
description: 風控與部位管理全生命週期矩陣與演算法管線：貫通開倉前規模計算、持有期停損動態推進、均線趨勢追蹤至基本面一票否決平倉。
---

# 4.4 風控與部位管理綜合決策矩陣與全生命週期

> **理論分類**: 演算法風控工程與交易生命週期管理 (Risk Engineering & Trade Lifecycle Management)  
> **核心概念**: 部位生命週期、動態停損演算法、基本面質變熔斷  
> **關聯模組**: [`engine/risk.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/risk.py)  
> **單元測試**: [`tests/test_engine.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/tests/test_engine.py)

---

## 風控與部位管理全生命週期矩陣

在系統運作中，每筆交易均經歷五個嚴格的生命週期節點，所有狀態轉換皆受數學公式與條件式約束：

### 表 4-3: 風控與部位管理全生命週期矩陣（Risk & Lifecycle Matrix）

| 交易生命週期節點 | 核心監控變數 | 數學判斷式 / 規則 | 執行動作 |
| :--- | :--- | :--- | :--- |
| **建倉前（Pre-Trade）** | 總組合淨值與波動度 | $\text{UnitRisk} = 2.5 \times \text{ATR}_{14}$ | 計算精確股數 $S = \lfloor \frac{\text{NAV} \times 0.0125}{\text{UnitRisk}} \rfloor$ |
| **持有初（Early Post-Trade）** | 現價 vs 初始停損價 | $P_t \le \text{StopLoss}_{\text{initial}}$ | 剛性平倉市價單出清，鎖定最大虧損 $1.25\%$ NAV |
| **獲利推進（Advancement）** | 浮動收益倍數 | $P_t - P_{\text{entry}} \ge 2.0 \times \text{ATR}_{14}$ | $\text{StopLoss} = \max(\text{StopLoss}, P_{\text{entry}})$ |
| **長線趨勢保護（Trailing）** | 50 日均線位置 | $P_t < \text{SMA}_{50}(t) \times 0.98$ | 跌破中長線趨勢均線，執行趨勢性保護停利 |
| **基本面質變（Fundamental Breach）**| 財報發布更新 | $\text{Sloan} > 0.12 \lor \text{FCF} < 0 \lor F\text{-Score} < 5$ | 護城河受損，無論技術面如何，立刻市價平倉 |

---

## 風控與部位管理演算法偽代碼（Algorithm 4.1）

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

## Python 引擎對應實作

在 [`engine/risk.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/risk.py) 中，本模組提供高度強健的型別化介面：

```python
from engine.risk import (
    calculate_true_range,
    calculate_atr,
    calculate_position_size,
    update_trailing_stop
)

# 計算部位大小與停損價位
shares, stop_loss = calculate_position_size(
    nav=100000.0,
    entry_price=150.0,
    atr=4.0,
    risk_fraction=0.0125,
    max_allocation_ratio=0.20
)
```

可透過 Docker 容器執行單元測試：
```bash
docker run --rm asymmetric-engine pytest -v tests/test_engine.py -k "risk or atr or position or trailing"
```

---

## 🎯 本節核心要點 (Key Takeaways)

1. **生命週期全閉環**：從開倉前的風險金額反推股數，到持倉期隨獲利上調停損點，形成完整的風控閉環。
2. **基本面優先否決權**：技術走勢再漂亮，若基本面出現作帳或現金流枯竭，立即執行強制無條件離場。
3. **無人為情緒干擾**：所有離場動作皆具備清晰的數學條件，完全排除猶豫、僥倖與後悔心理。

---

## 📚 相關文獻 (References)

- Vince, R. (1990). *Portfolio Management Formulas: Mathematical Trading Methods for the Futures, Options, and Stock Markets*. John Wiley & Sons.
- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.

---
👉 **章節總結**：第四章完畢，接下來進入實務篇章 [第五部分：實戰示範——端到端量化管線演練](../05-engine-and-quickstart/03-e2e-pipeline-walkthrough.md) 或參閱 [量化引擎與環境導覽](../05-engine-and-quickstart/README.md)
