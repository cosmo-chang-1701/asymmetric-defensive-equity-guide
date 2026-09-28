# 附錄：數學推導與實務決策速查

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

## A.3 系統全流程量化參數速查表

| 參數模組 | 參數變數名稱 | 基準推薦值 | 敏感度安全區間 | 觸發意義 |
| :--- | :--- | :---: | :---: | :--- |
| **PMPT 目標** | 最小可接受報酬率 ($MAR$) | $3.0\%$ (年化) | $0.0\% \sim 5.0\%$ | 索提諾比率評估門檻 |
| **會計篩選** | Sloan 應計比率上限 | $\le 0.10$ | $\le 0.12$ | 高於此值判定盈餘操縱 |
| **信用防線** | Altman $Z\text{-Score}$ 門檻 | $> 2.99$ | $\ge 1.81$ | 低於 1.81 視為破產危險 |
| **體質評分** | Piotroski $F\text{-Score}$ (常態) | $\ge 7$ | $7 \sim 9$ | 常態多頭標的體質 |
| | Piotroski $F\text{-Score}$ (恐慌) | $\ge 8$ | $8 \sim 9$ | 左側抄底標的極致體質 |
| **護城河回報**| 3 年平均 $\text{ROIC}$ | $\ge 15.0\%$ | $\ge 12.0\%$ | 資本配置優越性 |
| | 自由現金流收益率 ($\text{FCF Yield}$) | $\ge 4.0\%$ | $\ge 2.0\%$ | 現金流安全墊 |
| **宏觀體制** | SPY vs 200 SMA | 現價 > 均線 | 均線上揚 | 多頭體制基本條件 |
| | VIX 恐慌指標分區 | $< 20$ / $> 30$ | $20 \sim 30$ 為過渡 | 決定動能突破或反向價值 |
| **動能進場** | 突破高點時間窗口 | 52 週 (252 日) | 20 週 $\sim$ 52 週 | 突破阻力位 |
| | 成交量放大倍數 | $\ge 1.5 \times \text{VolMA}_{50}$ | $\ge 1.3 \times$ | 量增價揚確認機構介入 |
| **風控停損** | ATR 吊燈停損倍數 ($K$) | $2.5 \times \text{ATR}_{14}$ | $2.0 \sim 3.0$ | 避免日常雜訊洗盤 |
| | 最大初始停損百分比上限 | $8.0\%$ | $6.0\% \sim 10.0\%$ | 跌幅硬性天花板 |
| **倉位風險** | 單筆實質風險 ($R\text{-Risk}$) | $1.25\%$ NAV | $1.0\% \sim 1.5\%$ | 單筆交易最大虧損額 |
| | 單檔股票部位價值上限 | $20.0\%$ NAV | $15.0\% \sim 25.0\%$ | 單一個股集中度上限 |
| **移動停利** | 趨勢保護線 | 10 週 (50 日 SMA) | 跌破 2% 離場 | 獲利奔馳之戰略離場點 |
