"""Asymmetric Risk Management Module.

Implements Wilder (1978) ATR, Chandelier Stop-Loss,
Fixed Fractional Risk Position Sizing (Vince 1990), and multi-tiered trailing stops.
"""

from dataclasses import dataclass
from typing import Sequence, Tuple, Union
import numpy as np


@dataclass(frozen=True)
class PositionSizeResult:
    """Output of position sizing computation."""
    shares: int
    entry_price: float
    stop_loss_price: float
    risk_dollars: float
    risk_percentage_nav: float
    position_value: float
    position_percentage_nav: float


def calculate_true_range(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
) -> np.ndarray:
    """Calculate Wilder's True Range (TR) series.

    Formula:
        TR_t = max(H_t - L_t, |H_t - C_{t-1}|, |L_t - C_{t-1}|)

    Args:
        high: Array of high prices.
        low: Array of low prices.
        close: Array of close prices.

    Returns:
        np.ndarray: True range series of length T.
    """
    h = np.asarray(high, dtype=np.float64)
    l = np.asarray(low, dtype=np.float64)
    c = np.asarray(close, dtype=np.float64)

    if not (len(h) == len(l) == len(c)):
        raise ValueError("High, Low, and Close price arrays must have identical length.")
    if len(h) < 2:
        raise ValueError("Price series must have at least 2 observations to calculate TR.")

    tr = np.zeros(len(h), dtype=np.float64)
    tr[0] = h[0] - l[0]

    for t in range(1, len(h)):
        hl = h[t] - l[t]
        hc = abs(h[t] - c[t - 1])
        lc = abs(l[t] - c[t - 1])
        tr[t] = max(hl, hc, lc)

    return tr


def calculate_atr(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    period: int = 14,
) -> float:
    """Calculate the latest Average True Range (ATR).

    Args:
        high: High prices.
        low: Low prices.
        close: Close prices.
        period: Lookback window (default 14).

    Returns:
        float: Latest ATR value.
    """
    tr = calculate_true_range(high, low, close)
    if len(tr) < period:
        raise ValueError(f"Need at least {period} observations for ATR calculation.")
    return float(np.mean(tr[-period:]))


def calculate_position_size(
    nav: float,
    entry_price: float,
    atr: float,
    k_multiplier: float = 2.5,
    risk_fraction: float = 0.0125,
    max_allocation_ratio: float = 0.20,
    max_stop_loss_pct: float = 0.08,
) -> PositionSizeResult:
    """Calculate fixed fractional risk position size with ATR chandelier stop.

    Formula:
        UnitRisk = k_multiplier * ATR
        EffectiveRiskDistance = min(UnitRisk, entry_price * max_stop_loss_pct)
        StopPrice = entry_price - EffectiveRiskDistance
        TargetRiskDollars = NAV * risk_fraction
        Shares = floor(TargetRiskDollars / EffectiveRiskDistance)
        PositionValue = Shares * entry_price <= NAV * max_allocation_ratio

    Args:
        nav: Total Net Asset Value of portfolio.
        entry_price: Purchase entry price per share.
        atr: Current 14-day Average True Range.
        k_multiplier: Chandelier multiple (default 2.5).
        risk_fraction: Maximum NAV risk per trade (default 0.0125 = 1.25%).
        max_allocation_ratio: Maximum portfolio capital allocated to one stock (default 0.20 = 20%).
        max_stop_loss_pct: Maximum allowable stop loss percentage (default 0.08 = 8%).

    Returns:
        PositionSizeResult dataclass.
    """
    if nav <= 0:
        raise ValueError("NAV must be strictly positive.")
    if entry_price <= 0:
        raise ValueError("Entry price must be strictly positive.")
    if atr <= 0:
        raise ValueError("ATR must be strictly positive.")
    if not (0 < risk_fraction <= 0.05):
        raise ValueError("Risk fraction must be between 0 and 0.05 (5%).")

    raw_distance = k_multiplier * atr
    max_distance = entry_price * max_stop_loss_pct
    effective_risk_distance = min(raw_distance, max_distance)

    stop_loss_price = max(0.01, entry_price - effective_risk_distance)
    target_risk_dollars = nav * risk_fraction

    shares_by_risk = int(np.floor(target_risk_dollars / effective_risk_distance))
    max_allowed_shares = int(np.floor((nav * max_allocation_ratio) / entry_price))

    final_shares = max(0, min(shares_by_risk, max_allowed_shares))
    position_value = final_shares * entry_price
    actual_risk_dollars = final_shares * effective_risk_distance

    return PositionSizeResult(
        shares=final_shares,
        entry_price=entry_price,
        stop_loss_price=stop_loss_price,
        risk_dollars=actual_risk_dollars,
        risk_percentage_nav=actual_risk_dollars / nav,
        position_value=position_value,
        position_percentage_nav=position_value / nav,
    )


def update_trailing_stop(
    current_price: float,
    entry_price: float,
    current_stop_loss: float,
    entry_atr: float,
    sma50: float,
) -> Tuple[float, bool, str]:
    """Evaluate multi-tiered trailing stop logic.

    Logic:
        1. If price <= current_stop_loss -> Exit (Hit Stop Loss)
        2. If profit >= 2 * ATR and stop < entry -> Lift stop to Breakeven (entry_price)
        3. If price < 0.98 * sma50 and profit >= 3 * ATR -> Exit (Trend exhaustion)

    Returns:
        Tuple[float, bool, str]: (new_stop_price, should_exit, action_reason)
    """
    if current_price <= current_stop_loss:
        return current_stop_loss, True, "STOP_LOSS_TRIGGERED"

    profit_atr = (current_price - entry_price) / entry_atr
    new_stop = current_stop_loss

    # Breakeven adjustment
    if profit_atr >= 2.0 and new_stop < entry_price:
        new_stop = entry_price

    # Trend trailing exit condition
    if profit_atr >= 3.0 and current_price < 0.98 * sma50:
        return new_stop, True, "TREND_TRAILING_EXIT_SMA50_BREACH"

    return new_stop, False, "HOLD"
