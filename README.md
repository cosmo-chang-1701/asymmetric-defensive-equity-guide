# 非對稱防禦型美股策略指南：索提諾比率優化與雙向體制交易框架
### Asymmetric Defensive US Equity Strategy Guide

[![License: CC BY-NC 4.0](https://img.shields.io/badge/Docs%20License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](engine/Dockerfile)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen.svg)](tests/)
[![GitBook](https://img.shields.io/badge/GitBook-Online%20Docs-3884FF?logo=gitbook&logoColor=white)](https://semantic-cosmos.gitbook.io/asymmetric-defensive-equity-guide/)

> **Framework**: 後現代投資組合理論（PMPT）與實證資產定價（Empirical Asset Pricing）  
> **Target Audience**: 專業投資機構經理人、量化交易員、高階個人投資者  

---

## 專案簡介（Overview）

傳統均值-變異數理論（Markowitz MVO, 1952）將向上賺錢的波動與向下虧損的波動等同視為風險懲罰。然而，真實金融時間序列存在普遍的肥尾效應（Fat Tails）與負偏態（Negative Skewness）。

本專案全面轉向以**後現代投資組合理論（Post-Modern Portfolio Theory, PMPT）**為核心基石，結合工業級 Python 核心量化引擎，實現兼具強大下行防禦與右偏超額報酬的交易體系：

1. **索提諾比率優化（Sortino Ratio Optimization）**：以最小可接受報酬率（MAR）為基準，專注極小化下行偏差（Downside Deviation）。
2. **多維度選股管線（Screening Pipeline）**：結合 Sloan 應計利潤異象、Piotroski F-Score、Altman Z-Score 及 Stan Weinstein 階段分析。
3. **雙向體制切換引擎（Dual-Regime Switching）**：在常態多頭執行右側動能突破（Right-Side Momentum）；在極端恐慌時執行左側金字塔分批建倉（Left-Side Value Accumulation）。
4. **非對稱剛性風控（Asymmetric Risk Management）**：結合固定比例風險模型（Fixed Fractional Risk）與 ATR 吊燈停損（Chandelier Exit），單筆虧損嚴格截斷於 1%~1.5%，並極限放寬停利擁抱贏家複利。

---

## 目錄導覽（Book Contents）

> 📖 **GitBook 在線閱覽連結**: [https://semantic-cosmos.gitbook.io/asymmetric-defensive-equity-guide/](https://semantic-cosmos.gitbook.io/asymmetric-defensive-equity-guide/)

完整教材文檔位於 [`docs/`](docs/) 目錄，可配合 [`docs/SUMMARY.md`](docs/SUMMARY.md) 循序研讀：

- [前言與全書綱要](docs/README.md)
- [快速開始：Docker 環境與量化引擎](docs/05-engine-and-quickstart/01-docker-and-environment.md)
- [第一章：核心哲學——後現代投資組合理論與索提諾比率](docs/01-core-philosophy/README.md)
- [第二章：標的挑選體系——基本面因子與技術面過濾](docs/02-asset-selection/README.md)
- [第三章：動態體制切換機制——雙向交易執行框架](docs/03-regime-switching/README.md)
- [第四章：非對稱風控系統——剛性停損與極限放寬停利](docs/04-risk-management/README.md)
- [實戰示範：端到端量化管線演練](docs/05-engine-and-quickstart/03-e2e-pipeline-walkthrough.md)
- [附錄：數學推導與實務決策速查](docs/06-appendix/README.md)

---

## 量化引擎架構（Engine Architecture）

```
asymmetric-defensive-equity-guide/
├── gitbook-docs.yaml           # GitBook Site-Level Git Sync 配置設定檔
├── .gitbook.yaml               # GitBook Space-Level Git Sync 配置設定檔
├── docs/                       # 教材手冊與學術理論文檔 (CC BY-NC 4.0)
│   ├── .gitbook.yaml           # GitBook Space 目錄配置
│   ├── SUMMARY.md              # 書籍章節索引 (GitBook & mdBook 相容)
│   ├── README.md               # 教材導讀 Landing Page
│   ├── 01-core-philosophy/     # 第一章：後現代投資組合與索提諾比率
│   ├── 02-asset-selection/     # 第二章：標的挑選六層漏斗
│   ├── 03-regime-switching/    # 第三章：動態雙向體制切換
│   ├── 04-risk-management/     # 第四章：非對稱剛性風控
│   ├── 05-engine-and-quickstart/ # 第五章：量化引擎與實戰導覽
│   └── 06-appendix/            # 第六章：數學推導、參數與文獻清單
├── engine/                     # 純 Python 核心量化引擎 (MIT)
│   ├── __init__.py
│   ├── pmpt.py                 # 下行偏差與索提諾比率計算
│   ├── regime.py               # 體制辨識與雙向進場判斷
│   ├── screening.py            # 基本面 (F/Z-Score, Sloan) 與 Weinstein 技術篩選
│   ├── risk.py                 # ATR 停損、部位規模與移動停利
│   ├── requirements.txt        # 依賴清單
│   └── Dockerfile              # 容器化建置環境
├── tests/                      # 模組單元測試套件
│   ├── __init__.py
│   └── test_engine.py          # 13 項核心演算法測試
├── examples/                   # 實戰端到端整合範例
├── .github/workflows/          # GitHub Actions CI 自動化工作流
├── Makefile                    # 快捷建置與測試指令
├── book.toml                   # mdBook 靜態書籍設定檔
├── pyproject.toml              # 現代化 Python 打包配置
└── LICENSE                     # 雙授權條款 (CC BY-NC 4.0 + MIT)
```

---

## 快速開始（Quick Start）

本專案遵循工業級標準，所有量化模組均已容器化，推薦使用 Docker 執行以確保環境一致性：

### 使用 Docker 執行測試（推薦）

```bash
# 建置 Docker 映像檔並執行全部單元測試
make docker-test

# 或直接使用 Docker 指令：
docker build -t asymmetric-engine -f engine/Dockerfile .
docker run --rm asymmetric-engine
```

### 執行端到端完整策略演示

```bash
# 在 Docker 容器內執行全流程範例
make docker-demo
```

### 本地環境安裝（可選）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pytest -v tests/
```

---

## 📄 授權條款 (License)

> 本作品內容由 AI 輔助全面生成，並由專案發起人進行架構設計與彙整發布。本作品採用 創用 CC 姓名標示-非商業性 4.0 國際授權條款 (CC BY-NC 4.0) 與 MIT 授權條款釋出。

本書採用**雙授權（Dual-Licensing）模式**：
- **電子書與教學內容**：位於 [`docs/`](docs/) 中之全書章節、數學推導與策略教學手冊，採用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hant)（創用 CC 姓名標示-非商業性 4.0 國際授權條款）釋出。歡迎自由閱讀、分享與非商業改作，但**未經原作者書面授權，嚴禁任何形式之商業營利、付費轉載或集結出版**。
- **範例代碼、量化引擎與配置**：位於 [`engine/`](engine/)、[`tests/`](tests/) 與 [`examples/`](examples/) 中之程式碼及設定檔，均採用寬鬆的 [MIT License](LICENSE) 授權，讀者可自由在個人或企業內部專案中無痛引用與部署。

### ⚠️ 免責與商標聲明
- **投資與技術免責**：本手冊所載之量化模型、因子回測、體制切換演算法與部位管理代碼範例僅供學習參考與學術研究，投入實盤交易或生產環境前請務必於沙盒環境充分測試。作者與貢獻者不承擔任何直接或間接之投資損益或營運業務損失責任。
- **商標與引用聲明**：文中所提及之指數標的（如 `SPY`、`VIX`）及金融學術模型（如 Markowitz、Sortino、Piotroski、Altman 等），其商標、商號或學術智慧財產權均屬原持有人或機構所有。本書為獨立研發之開源學習手冊，非任何金融機構或交易所官方贊助、附屬或背書之專案。

### 📖 引用本手冊 (Citation)
若您在文章、教材或專案中引用本書內容，請依 CC 規範標註出處：
> Cosmo Chang, *非對稱防禦型美股策略指南：索提諾比率優化與雙向體制交易框架*, 2026. GitHub: https://github.com/cosmo-chang-1701/asymmetric-defensive-equity-guide

