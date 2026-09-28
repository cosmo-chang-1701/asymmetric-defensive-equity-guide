---
description: 多維度標的初篩綜合決策矩陣與演算法管線（Pipeline）：整合六層檢驗邏輯，並對接 engine/screening.py 核心篩選程式碼模組。
---

# 2.4 多維度標的初篩決策矩陣與篩選管線

> **理論分類**: 量化選股管線與工程實作 (Quantitative Screening & Engineering Pipeline)  
> **核心概念**: 決策矩陣 (Decision Matrix)、多因子過濾管線、准入清單  
> **關聯模組**: [`engine/screening.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/screening.py)  
> **單元測試**: [`tests/test_engine.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/tests/test_engine.py)

---

## 全方位標的初篩綜合決策矩陣

本體系將六大檢驗層次統合成標準決策矩陣，所有進入回測或實盤監控的標的必須逐層審核：

### 表 2-3: 全方位標的初篩綜合決策矩陣（Screening Decision Matrix）

| 檢驗層次 | 檢驗模組 | 指標名稱 | 嚴格准入條件 (Pass Criteria) | 違規處理動作 |
| :--- | :--- | :--- | :--- | :--- |
| **第一層：會計品質** | Sloan (1996) | 應計比率 (Accrual Ratio) | $\text{Accrual Ratio} \le 0.10$ | 剔除標的（盈餘操縱風險） |
| **第二層：信用韌性** | Altman (1968) | $Z\text{-Score}$ | $Z > 2.99$ （極限寬限至 $Z \ge 1.81$ ） | $Z < 1.81$ 立即一票否決 |
| **第三層：經營體質** | Piotroski (2000) | $F\text{-Score}$ | 常態體制 $\ge 7$ ；恐慌體制 $\ge 8$ | 未達標則不予放行 |
| **第四層：資本回報** | Fama-French | $\text{ROIC}$ & $\text{FCF Yield}$ | 3 年均 $\text{ROIC} \ge 15\%$ 且 $\text{FCF} > 0$ | 剔除標的（缺乏護城河） |
| **第五層：市場階段** | Weinstein (1988) | Stage 週期分析 | 處於 Stage 2 突破或延續 | Stage 1 觀察，Stage 3/4 剔除 |
| **第六層：長線趨勢** | Brock et al. (1992) | 200-day SMA | $P_t > \text{SMA}_{200}$ 且斜率為正 | 違背則右側禁開倉 |

---

## 篩選演算法偽代碼（Algorithm 2.1）

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

## Python 引擎對應實作

在 [`engine/screening.py`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/engine/screening.py) 中，本選股管線由下列核心函式實現：

```python
from engine.screening import (
    calculate_sloan_accrual,
    calculate_piotroski_f_score,
    calculate_altman_z_score,
    check_weinstein_stage2,
    screen_asset
)

# 執行全流程多層次過濾
is_approved_r1, is_approved_r2 = screen_asset(stock_data)
```

讀者可透過 Docker 執行完整的單元測試套件以驗證篩選邏輯：
```bash
docker run --rm asymmetric-engine pytest -v tests/test_engine.py -k "screening or sloan or piotroski or altman or weinstein"
```

---

## 🎯 本節核心要點 (Key Takeaways)

1. **雙清單分類輸出**：演算法自動產出體制一（右側動能候選）與體制二（左側極值價值候選）兩大清單。
2. **階梯式一票否決**：前置會計與信用層只要觸發即刻中止，顯著節省計算資源。
3. **無縫整合量化引擎**：文檔中的所有公式與邏輯在 `engine/screening.py` 中皆有高純度、具備型別標註的 Python 實作。

---

## 📚 相關文獻 (References)

- Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *The Journal of Finance*, 23(4), 589-609.
- Brock, W., Lakonishok, J., & LeBaron, B. (1992). Simple technical trading rules and the stochastic properties of stock returns. *The Journal of Finance*, 47(5), 1731-1764.
- Piotroski, J. D. (2000). Value investing: The use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38, 1-41.
- Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows about future earnings? *The Accounting Review*, 71(3), 289-315.
- Weinstein, S. (1988). *Stan Weinstein's Secrets for Profiting in Bull and Bear Markets*. McGraw-Hill.

---
👉 **章節總結**：第二章完畢，接下來進入 [第三章：動態體制切換機制——雙向交易執行框架](../03-regime-switching/README.md)
