"""Comprehensive unit tests for the PMPT Quantitative Engine.

Verifies:
1. PMPT Sortino Ratio and Downside Deviation calculations.
2. Sloan Accruals, Piotroski F-Score, Altman Z-Score, and Weinstein Stage 2.
3. Market Regime Identification and Dual-Regime Execution rules.
4. ATR Chandelier Stop, Fixed Fractional Position Sizing, and Trailing Stops.
"""

import math
import pytest
import numpy as np

from engine.pmpt import calculate_downside_deviation, calculate_sortino_ratio
from engine.screening import (
    FinancialStatement,
    calculate_sloan_accrual,
    calculate_piotroski_f_score,
    calculate_altman_z_score,
    check_trend_and_stage2,
)
from engine.regime import (
    MarketRegime,
    identify_market_regime,
    can_execute_right_side_entry,
    can_execute_left_side_entry,
)
from engine.risk import (
    calculate_true_range,
    calculate_atr,
    calculate_position_size,
    update_trailing_stop,
)


# ==============================================================================
# 1. PMPT & Sortino Tests
# ==============================================================================
def test_downside_deviation_basic():
    # Returns with known downside deviations
    # returns: [-0.02, 0.03, -0.01, 0.04, 0.00]
    # MAR = 0.0
    # underperformance: [-0.02, 0, -0.01, 0, 0]
    # squares: [0.0004, 0, 0.0001, 0, 0] -> sum = 0.0005, mean = 0.0001
    # sqrt(0.0001) = 0.01
    returns = [-0.02, 0.03, -0.01, 0.04, 0.00]
    dd_periodic = calculate_downside_deviation(returns, mar=0.0, annualized=False)
    assert pytest.approx(dd_periodic, rel=1e-5) == 0.01

    dd_annual = calculate_downside_deviation(returns, mar=0.0, annualized=True, periods_per_year=252)
    assert pytest.approx(dd_annual, rel=1e-5) == 0.01 * math.sqrt(252)


def test_downside_deviation_zero_downside():
    returns = [0.01, 0.02, 0.03, 0.04]
    dd = calculate_downside_deviation(returns, mar=0.0, annualized=False)
    assert dd == 0.0

    sortino = calculate_sortino_ratio(returns, mar=0.0, annualized_mar=False, periods_per_year=252)
    assert math.isinf(sortino) and sortino > 0


def test_downside_deviation_empty_error():
    with pytest.raises(ValueError, match="Return series cannot be empty"):
        calculate_downside_deviation([])


def test_sortino_ratio_calculation():
    # Symmetric vs Asymmetric returns with equal mean
    # Strategy A (symmetrical): [-0.02, 0.02] -> mean 0
    # Strategy B (asymmetric): [-0.01, 0.03] -> mean +0.01
    returns_b = [-0.01, 0.03]
    sortino_b = calculate_sortino_ratio(returns_b, mar=0.0, annualized_mar=False, periods_per_year=252)
    assert sortino_b > 0


# ==============================================================================
# 2. Fundamental & Technical Screening Tests
# ==============================================================================
def test_sloan_accrual():
    # delta_CA = 200, delta_Cash = 50, delta_CL = 80, delta_STD = 20, Dep = 40, AvgAssets = 1000
    # Accruals = (200 - 50) - (80 - 20) - 40 = 150 - 60 - 40 = 50
    # Sloan Ratio = 50 / 1000 = 0.05 (Passes <= 0.10)
    ratio = calculate_sloan_accrual(
        delta_current_assets=200.0,
        delta_cash=50.0,
        delta_current_liabilities=80.0,
        delta_short_term_debt=20.0,
        depreciation=40.0,
        avg_total_assets=1000.0,
    )
    assert pytest.approx(ratio, rel=1e-5) == 0.05

    with pytest.raises(ValueError):
        calculate_sloan_accrual(10, 5, 2, 0, 1, avg_total_assets=0.0)


def test_piotroski_f_score_perfect():
    current = FinancialStatement(
        net_income=100.0,
        operating_cash_flow=150.0,
        total_assets=1000.0,
        total_assets_prev=900.0,
        long_term_debt=200.0,
        current_assets=400.0,
        current_liabilities=200.0,
        shares_outstanding=100.0,
        gross_margin=0.45,
        revenue=1200.0,
    )
    previous = FinancialStatement(
        net_income=80.0,
        operating_cash_flow=100.0,
        total_assets=900.0,
        total_assets_prev=850.0,
        long_term_debt=250.0,  # debt was higher in past -> lower leverage now (F5=1)
        current_assets=300.0,
        current_liabilities=200.0,  # CR past = 1.5, now = 2.0 (F6=1)
        shares_outstanding=100.0,  # no new shares (F7=1)
        gross_margin=0.40,  # margin improved (F8=1)
        revenue=1000.0,  # turnover past = 1000/850 = 1.176, now = 1200/900 = 1.333 (F9=1)
    )

    total_score, comps = calculate_piotroski_f_score(current, previous)
    assert total_score == 9
    assert all(v == 1 for v in comps.values())


def test_altman_z_score():
    # Safe zone company
    z = calculate_altman_z_score(
        working_capital=300.0,
        retained_earnings=400.0,
        ebit=200.0,
        market_cap=2000.0,
        sales=1500.0,
        total_assets=1000.0,
        total_liabilities=400.0,
    )
    # Z = 1.2*(0.3) + 1.4*(0.4) + 3.3*(0.2) + 0.6*(5.0) + 0.999*(1.5)
    #   = 0.36 + 0.56 + 0.66 + 3.0 + 1.4985 = 6.0785
    assert z > 2.99


def test_weinstein_stage2_check():
    # Generate 250 bars of trending upward prices
    np.random.seed(42)
    prices = [100.0 + i * 0.5 for i in range(250)]
    passed, curr_price, curr_sma = check_trend_and_stage2(prices, sma_window=200, slope_window=20)
    assert passed is True
    assert curr_price > curr_sma


# ==============================================================================
# 3. Dynamic Regime-Switching Tests
# ==============================================================================
def test_regime_identification():
    # Normal Bull
    regime = identify_market_regime(spy_price=500.0, spy_sma200=470.0, vix_level=14.5, breadth_ratio=2.5)
    assert regime == MarketRegime.REGIME_1_NORMAL_BULL

    # Extreme Stress
    regime_stress = identify_market_regime(spy_price=420.0, spy_sma200=470.0, vix_level=35.0)
    assert regime_stress == MarketRegime.REGIME_2_EXTREME_STRESS

    # Transition
    regime_trans = identify_market_regime(spy_price=465.0, spy_sma200=470.0, vix_level=24.0)
    assert regime_trans == MarketRegime.REGIME_TRANSITION_NEUTRAL


def test_right_side_entry_validation():
    # Valid breakout
    ok, msg = can_execute_right_side_entry(
        current_price=105.0,
        high_52w=104.0,
        current_volume=2000000.0,
        avg_volume_50=1000000.0,
        f_score=8,
        is_above_200sma=True,
    )
    assert ok is True
    assert "APPROVED" in msg

    # Low volume rejection
    ok_fail, _ = can_execute_right_side_entry(
        current_price=105.0,
        high_52w=104.0,
        current_volume=1200000.0,
        avg_volume_50=1000000.0,
        f_score=8,
        is_above_200sma=True,
    )
    assert ok_fail is False


def test_left_side_entry_validation():
    # Valid contrarian
    ok, msg = can_execute_left_side_entry(
        valuation_percentile=0.03,
        f_score=9,
        z_score=3.5,
        vix_level=34.0,
    )
    assert ok is True

    # Reject if VIX not in panic
    ok_fail, _ = can_execute_left_side_entry(
        valuation_percentile=0.03,
        f_score=9,
        z_score=3.5,
        vix_level=18.0,
    )
    assert ok_fail is False


# ==============================================================================
# 4. Asymmetric Risk Management Tests
# ==============================================================================
def test_atr_and_position_size():
    highs = [102.0, 104.0, 105.0, 103.0, 106.0] * 5
    lows = [98.0, 99.0, 101.0, 100.0, 102.0] * 5
    closes = [100.0, 103.0, 104.0, 101.0, 105.0] * 5

    atr14 = calculate_atr(highs, lows, closes, period=14)
    assert atr14 > 0.0

    nav = 1_000_000.0
    entry_price = 100.0
    result = calculate_position_size(
        nav=nav,
        entry_price=entry_price,
        atr=2.0,
        k_multiplier=2.5,
        risk_fraction=0.01,  # 1% risk = $10,000
    )
    # Unit risk = 2.5 * 2.0 = $5.0 (5% of 100 <= max 8%)
    # Target risk dollars = $10,000
    # Shares = 10,000 / 5 = 2000 shares
    assert result.shares == 2000
    assert result.stop_loss_price == 95.0
    assert result.risk_dollars == 10000.0
    assert result.risk_percentage_nav == 0.01


def test_trailing_stop():
    entry_price = 100.0
    stop_loss = 95.0
    atr = 2.0
    sma50 = 102.0

    # Case 1: Hit stop loss
    _, should_exit, reason = update_trailing_stop(94.5, entry_price, stop_loss, atr, sma50)
    assert should_exit is True
    assert reason == "STOP_LOSS_TRIGGERED"

    # Case 2: Lift to breakeven after +2 ATR gain (price = 105)
    new_stop, should_exit, _ = update_trailing_stop(105.0, entry_price, stop_loss, atr, sma50)
    assert should_exit is False
    assert new_stop == entry_price  # lifted to 100.0

    # Case 3: Trend trailing exit when deep below SMA50
    _, should_exit, reason = update_trailing_stop(107.0, entry_price, 100.0, atr, sma50=115.0)
    assert should_exit is True
    assert reason == "TREND_TRAILING_EXIT_SMA50_BREACH"
