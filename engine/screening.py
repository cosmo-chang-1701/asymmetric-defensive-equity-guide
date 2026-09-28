"""Fundamental and Technical Screening Module.

Implements Sloan (1996) Accrual Anomaly, Piotroski (2000) F-Score,
Altman (1968) Z-Score, and Weinstein (1988) Stage 2 & 200 SMA filters.
"""

from dataclasses import dataclass
from typing import Dict, Any, Sequence, Tuple
import numpy as np


@dataclass(frozen=True)
class FinancialStatement:
    """Snapshot of financial metrics for a single period."""
    net_income: float
    operating_cash_flow: float
    total_assets: float
    total_assets_prev: float
    long_term_debt: float
    current_assets: float
    current_liabilities: float
    shares_outstanding: float
    gross_margin: float
    revenue: float


def calculate_sloan_accrual(
    delta_current_assets: float,
    delta_cash: float,
    delta_current_liabilities: float,
    delta_short_term_debt: float,
    depreciation: float,
    avg_total_assets: float,
) -> float:
    """Calculate Sloan (1996) Balance Sheet Accrual Ratio.

    Formula:
        Accruals = (delta_CA - delta_Cash) - (delta_CL - delta_STD) - Dep
        Accrual_Ratio = Accruals / avg_total_assets

    Args:
        delta_current_assets: Change in current assets.
        delta_cash: Change in cash and cash equivalents.
        delta_current_liabilities: Change in current liabilities.
        delta_short_term_debt: Change in short term debt included in current liabilities.
        depreciation: Depreciation and amortization expense.
        avg_total_assets: Average total assets ((Assets_t + Assets_{t-1}) / 2).

    Returns:
        float: Normalized Sloan accrual ratio.

    Raises:
        ValueError: If avg_total_assets <= 0.
    """
    if avg_total_assets <= 0:
        raise ValueError("Average total assets must be strictly positive.")

    accruals = (
        (delta_current_assets - delta_cash)
        - (delta_current_liabilities - delta_short_term_debt)
        - depreciation
    )
    return float(accruals / avg_total_assets)


def calculate_piotroski_f_score(
    current: FinancialStatement,
    previous: FinancialStatement,
) -> Tuple[int, Dict[str, int]]:
    """Calculate Piotroski (2000) 9-point fundamental financial health F-Score.

    Criteria:
        Profitability:
            F1: ROA > 0
            F2: CFO > 0
            F3: delta_ROA > 0
            F4: CFO > Net Income (Accrual check)
        Leverage, Liquidity, & Source of Funds:
            F5: delta_LongTermDebtRatio <= 0
            F6: delta_CurrentRatio > 0
            F7: Shares_t <= Shares_{t-1} (No dilutive offering)
        Operating Efficiency:
            F8: delta_GrossMargin > 0
            F9: delta_AssetTurnover > 0

    Args:
        current: FinancialStatement of the current period.
        previous: FinancialStatement of the prior period.

    Returns:
        Tuple[int, Dict[str, int]]: Total score (0-9) and individual component scores.
    """
    if current.total_assets_prev <= 0 or previous.total_assets_prev <= 0:
        raise ValueError("Prior total assets must be strictly positive to calculate ROA.")

    # Profitability signals
    roa_current = current.net_income / current.total_assets_prev
    roa_previous = previous.net_income / previous.total_assets_prev
    delta_roa = roa_current - roa_previous

    f1 = 1 if roa_current > 0 else 0
    f2 = 1 if current.operating_cash_flow > 0 else 0
    f3 = 1 if delta_roa > 0 else 0
    f4 = 1 if current.operating_cash_flow > current.net_income else 0

    # Leverage and Liquidity signals
    lev_current = current.long_term_debt / current.total_assets if current.total_assets > 0 else 0.0
    lev_previous = previous.long_term_debt / previous.total_assets if previous.total_assets > 0 else 0.0
    delta_lev = lev_current - lev_previous

    cr_current = (
        current.current_assets / current.current_liabilities
        if current.current_liabilities > 0
        else 1.0
    )
    cr_previous = (
        previous.current_assets / previous.current_liabilities
        if previous.current_liabilities > 0
        else 1.0
    )
    delta_cr = cr_current - cr_previous

    f5 = 1 if delta_lev <= 0 else 0
    f6 = 1 if delta_cr > 0 else 0
    f7 = 1 if current.shares_outstanding <= previous.shares_outstanding else 0

    # Operating Efficiency signals
    delta_margin = current.gross_margin - previous.gross_margin

    turnover_current = current.revenue / current.total_assets_prev
    turnover_previous = previous.revenue / previous.total_assets_prev
    delta_turnover = turnover_current - turnover_previous

    f8 = 1 if delta_margin > 0 else 0
    f9 = 1 if delta_turnover > 0 else 0

    components = {
        "F1_PositiveROA": f1,
        "F2_PositiveCFO": f2,
        "F3_DeltaROA": f3,
        "F4_AccrualQuality": f4,
        "F5_LowerLeverage": f5,
        "F6_HigherCurrentRatio": f6,
        "F7_NoEquityDilution": f7,
        "F8_HigherGrossMargin": f8,
        "F9_HigherTurnover": f9,
    }

    total_score = sum(components.values())
    return total_score, components


def calculate_altman_z_score(
    working_capital: float,
    retained_earnings: float,
    ebit: float,
    market_cap: float,
    sales: float,
    total_assets: float,
    total_liabilities: float,
) -> float:
    """Calculate Altman (1968) Z-Score for bankruptcy risk screening.

    Formula:
        Z = 1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 0.999 * X5

    Safe Zone: Z > 2.99
    Grey Zone: 1.81 <= Z <= 2.99
    Distress Zone: Z < 1.81

    Args:
        working_capital: Current Assets - Current Liabilities.
        retained_earnings: Cumulative retained earnings on balance sheet.
        ebit: Earnings before interest and taxes.
        market_cap: Total market capitalization (Price * Shares).
        sales: Total revenue.
        total_assets: Total assets.
        total_liabilities: Total liabilities (Current + Long-term debt).

    Returns:
        float: Z-Score.
    """
    if total_assets <= 0:
        raise ValueError("Total assets must be strictly positive.")
    if total_liabilities <= 0:
        raise ValueError("Total liabilities must be strictly positive.")

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_cap / total_liabilities
    x5 = sales / total_assets

    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5
    return float(z)


def check_trend_and_stage2(
    close_prices: Sequence[float],
    sma_window: int = 200,
    slope_window: int = 20,
) -> Tuple[bool, float, float]:
    """Check Brock et al. (1992) 200-day SMA trend filter and Weinstein Stage 2 conditions.

    Conditions:
        1. Current price > 200-day SMA.
        2. 200-day SMA slope is non-negative (SMA_t >= SMA_{t-slope_window}).

    Args:
        close_prices: Historical series of daily closing prices.
        sma_window: Window for the long-term moving average (default 200).
        slope_window: Lookback period for testing SMA slope direction (default 20).

    Returns:
        Tuple[bool, float, float]: (is_stage2_or_bullish, current_price, current_sma).
    """
    prices = np.asarray(close_prices, dtype=np.float64)
    if prices.size < sma_window + slope_window:
        raise ValueError(
            f"Close price series must have at least {sma_window + slope_window} bars."
        )

    # Compute SMA
    sma = np.convolve(prices, np.ones(sma_window) / sma_window, mode="valid")
    current_price = float(prices[-1])
    current_sma = float(sma[-1])
    prev_sma = float(sma[-slope_window])

    is_above = current_price > current_sma
    is_rising = current_sma >= prev_sma

    passed = is_above and is_rising
    return passed, current_price, current_sma
