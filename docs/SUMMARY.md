# Table of Contents

## 導讀與快速開始
* [前言與全書綱要](README.md)
* [量化引擎與實務實作導覽](05-engine-and-quickstart/README.md)
* [快速開始：Docker 環境與量化引擎](05-engine-and-quickstart/01-docker-and-environment.md)
* [系統架構與代碼導覽](05-engine-and-quickstart/02-engine-architecture.md)

## 第一部分：核心哲學與數學基礎
* [第一章：後現代投資組合理論與索提諾比率](01-core-philosophy/README.md)
  * [1.1 現代投資組合理論（MPT）與夏普比率的內在缺陷](01-core-philosophy/01-mpt-and-sharpe-flaws.md)
  * [1.2 金融肥尾與非對稱分佈：高斯假設的崩潰](01-core-philosophy/02-fat-tails-and-skewness.md)
  * [1.3 索提諾比率的數學嚴格推導與目標函數優化](01-core-philosophy/03-sortino-ratio-derivation.md)
  * [1.4 長線持有與非對稱收益輪廓的構建](01-core-philosophy/04-asymmetric-payoff-profile.md)

## 第二部分：標的挑選體系
* [第二章：基本面因子與技術面過濾](02-asset-selection/README.md)
  * [2.1 獲利品質與財務韌性：Sloan 應計、F-Score 與 Z-Score](02-asset-selection/01-accounting-quality-and-resilience.md)
  * [2.2 競爭優勢與資本回報：Fama-French、ROIC 與 FCF Yield](02-asset-selection/02-capital-return-and-moat.md)
  * [2.3 技術面輔助驗證：Weinstein 階段與 200 SMA 趨勢濾網](02-asset-selection/03-technical-filters-and-stages.md)
  * [2.4 多維度標的初篩決策矩陣與篩選管線](02-asset-selection/04-screening-matrix-and-pipeline.md)

## 第三部分：動態體制切換機制
* [第三章：雙向交易執行框架](03-regime-switching/README.md)
  * [3.1 市場宏觀狀態與趨勢體制識別](03-regime-switching/01-regime-identification-metrics.md)
  * [3.2 常態環境：右側動能突破交易](03-regime-switching/02-right-side-momentum-trading.md)
  * [3.3 極端壓力環境：左側逆向金字塔價值積累](03-regime-switching/03-left-side-contrarian-accumulation.md)
  * [3.4 雙向體制切換狀態機引擎與決策矩陣](03-regime-switching/04-state-machine-engine.md)

## 第四部分：非對稱風控系統
* [第四章：剛性停損與極限放寬停利](04-risk-management/README.md)
  * [4.1 為什麼必須嚴格停損？幾何數學、行為偏誤與 Bessembinder 實證](04-risk-management/01-empirical-case-for-stop-loss.md)
  * [4.2 剛性停損執行框架：Wilder ATR 吊燈停損與固定比例風險模型](04-risk-management/02-rigid-stop-loss-framework.md)
  * [4.3 放寬停利與長期持有：正偏態肥尾捕捉與多層次移動停利](04-risk-management/03-trailing-stop-and-fat-tail-capture.md)
  * [4.4 風控與部位管理綜合決策矩陣與全生命週期](04-risk-management/04-lifecycle-risk-matrix.md)

## 第五部分：實戰管線示範
* [實戰示範：端到端量化管線演練](05-engine-and-quickstart/03-e2e-pipeline-walkthrough.md)

## 第六部分：附錄與參考資源
* [附錄：數學推導與速查](06-appendix/README.md)
  * [附錄 A：下行偏差與偏動差（LPM）嚴格數學推導](06-appendix/01-mathematical-foundations.md)
  * [附錄 B：系統全流程量化參數與敏感度速查表](06-appendix/02-parameter-cheat-sheet.md)
  * [附錄 C：學術文獻與經典著作引用清單](06-appendix/03-bibliography.md)
