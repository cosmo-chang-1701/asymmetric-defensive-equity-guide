---
description: 快速上手指南：透過 Docker 容器化技術隔離依賴與環境，執行 13 項核心演算法單元測試，並使用 Makefile 快捷指令無痛驅動策略管線。
---

# 快速開始：Docker 環境與量化引擎

> **環境目標**: 100% 容器化隔離、可重現量化執行環境  
> **基礎環境**: Docker 20.10+ / Python 3.12-slim  
> **核心工具**: Docker, Makefile, pytest

---

## 為什麼必須使用 Docker 容器？

量化交易程式對依賴函式庫版本（如數值精確度、浮點運算行為、日期處理）具有極高的敏感性。「在我的機器上可以跑（Works on my machine）」是量化工程交付中的大忌。

本專案奉行嚴格的工業級規範：**所有核心演算法、單元測試與演示管線皆已容器化打包，確保在任何環境下皆具備 100% 確定性的執行結果**。

---

## 快捷 Makefile 指令集

專案根目錄附帶有 [`Makefile`](file:///home/cosmo_chang/Projects/asymmetric-defensive-equity-guide/Makefile)，封裝了最常用的容器建置與測試指令：

| 指令 | 說明 | 內部執行動作 |
| :--- | :--- | :--- |
| `make docker-build` | 建置 Docker 映像檔 | 讀取 `engine/Dockerfile` 建置標籤為 `asymmetric-engine` 的映像檔 |
| `make docker-test` | 於容器內執行完整測試 | 建置映像檔並啟動容器執行 `pytest -v tests/` |
| `make docker-demo` | 於容器內執行端到端管線 | 建置映像檔並執行 `python3 examples/pipeline_demo.py` |
| `make clean` | 清理本地暫存快取 | 清理 `__pycache__`、`.pytest_cache` 及各項構建殘留產物 |

---

## 1. 執行 Docker 單元測試（推薦）

只需在終端機執行一行命令，系統將自動完成編譯、依賴安裝與測試：

```bash
make docker-test
```

您將看到 13 項涵蓋 PMPT、選股、體制切換與風控的測試全部通過：
```text
tests/test_engine.py::test_downside_deviation_basic PASSED               [  7%]
tests/test_engine.py::test_downside_deviation_zero_downside PASSED       [ 15%]
tests/test_engine.py::test_downside_deviation_empty_error PASSED         [ 23%]
tests/test_engine.py::test_sortino_ratio_calculation PASSED              [ 30%]
tests/test_engine.py::test_sloan_accrual PASSED                          [ 38%]
tests/test_engine.py::test_piotroski_f_score_perfect PASSED              [ 46%]
tests/test_engine.py::test_altman_z_score PASSED                         [ 53%]
tests/test_engine.py::test_weinstein_stage2_check PASSED                 [ 61%]
tests/test_engine.py::test_regime_identification PASSED                  [ 69%]
tests/test_engine.py::test_right_side_entry_validation PASSED            [ 76%]
tests/test_engine.py::test_left_side_entry_validation PASSED             [ 84%]
tests/test_engine.py::test_atr_and_position_size PASSED                  [ 92%]
tests/test_engine.py::test_trailing_stop PASSED                          [100%]

============================== 13 passed in 0.19s ==============================
```

### 原生 Docker 命令（無 make 環境時）
若系統未安裝 `make` 工具，可直接透過原生 Docker CLI 執行：

```bash
# 1. 建置映像檔
docker build -t asymmetric-engine -f engine/Dockerfile .

# 2. 執行容器測試
docker run --rm asymmetric-engine pytest -v tests/
```

---

## 2. 執行端到端完整策略演示

若想在受控沙盒環境中直觀體驗策略管線如何挑選標的、判定體制並試算部位風險：

```bash
make docker-demo
```

或使用 Docker 指令：
```bash
docker run --rm asymmetric-engine python3 examples/pipeline_demo.py
```

---

## 3. 本地原生 Python 環境配置（可選開發模式）

若您需要在 IDE（如 VS Code、Cursor 等）中進行代碼開發或偵錯，亦可建立本地虛擬環境：

```bash
# 建立 Python 3.12 虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝專案依賴與套件 (Editable Mode)
pip install -r engine/requirements.txt
pip install -e .

# 執行本地測試
pytest -v tests/
```

---

## 🎯 本節核心要點 (Key Takeaways)

1. **容器化環境優先**：一律優先在 Docker 容器內執行測試與策略示範，消除環境不一致風險。
2. **極致輕量與快速**：映像檔基於 `python:3.12-slim`，建置耗時少於 2 秒，測試執行僅需 0.2 秒。
3. **CI/CD 自動化守護**：專案透過 GitHub Actions 在每次 Pull Request 與 Push 時自動執行上述容器測試。

---
👉 **下一單元**：閱讀 [5.2 系統架構與代碼導覽](02-engine-architecture.md)
