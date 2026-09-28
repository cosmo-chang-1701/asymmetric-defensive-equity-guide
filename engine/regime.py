"""Dual-Regime Switching Engine Module.

Implements market regime identification (S&P 500 trend & VIX),
right-side momentum entry conditions (Jegadeesh & Titman 1993, Moskowitz et al. 2012),
and left-side contrarian value accumulation rules (De Bondt & Thaler 1985).
"""

from enum import Enum
from typing import Optional, Tuple


class MarketRegime(str, Enum):
    """Market regime classification."""
    REGIME_1_NORMAL_BULL = "REGIME_1_NORMAL_BULL"
    REGIME_TRANSITION_NEUTRAL = "REGIME_TRANSITION_NEUTRAL"
    REGIME_2_EXTREME_STRESS = "REGIME_2_EXTREME_STRESS"


def identify_market_regime(
    spy_price: float,
    spy_sma200: float,
    vix_level: float,
    breadth_ratio: Optional[float] = None,
) -> MarketRegime:
    """Identify market state based on S&P 500 trend, VIX, and breadth indicators.

    Logic:
        - Regime 2 (Extreme Stress): VIX > 30.0 or severe dislocation
        - Regime 1 (Normal Bull): SPY > 200 SMA and VIX < 22.0 (and Breadth >= 1.0 if given)
        - Transition / Neutral: All intermediate states

    Args:
        spy_price: Current closing price of SPY (S&P 500 benchmark).
        spy_sma200: Current 200-day simple moving average of SPY.
        vix_level: Current CBOE VIX index level.
        breadth_ratio: Ratio of 52-week new highs to new lows (optional).

    Returns:
        MarketRegime enum.
    """
    if vix_level > 30.0:
        return MarketRegime.REGIME_2_EXTREME_STRESS

    is_above_trend = spy_price > spy_sma200
    is_low_vol = vix_level < 22.0
    is_breadth_healthy = breadth_ratio is None or breadth_ratio >= 1.0

    if is_above_trend and is_low_vol and is_breadth_healthy:
        return MarketRegime.REGIME_1_NORMAL_BULL

    return MarketRegime.REGIME_TRANSITION_NEUTRAL


def can_execute_right_side_entry(
    current_price: float,
    high_52w: float,
    current_volume: float,
    avg_volume_50: float,
    f_score: int,
    is_above_200sma: bool,
) -> Tuple[bool, str]:
    """Validate right-side momentum breakout entry conditions.

    Conditions:
        1. Stock must be in Stage 2 (Above 200 SMA).
        2. Fundamental F-Score >= 7.
        3. Price breakout (current_price >= 52-week high, with 0.5% tolerance threshold).
        4. Volume expansion: current_volume >= 1.5 * 50-day average volume.

    Returns:
        Tuple[bool, str]: (is_valid, reason_message).
    """
    if not is_above_200sma:
        return False, "REJECTED: Price below 200 SMA (not in Stage 2 upward trend)."
    if f_score < 7:
        return False, f"REJECTED: F-Score {f_score} below minimum threshold of 7."
    if current_price < high_52w * 0.995:
        return False, f"REJECTED: Price {current_price:.2f} has not broken 52-week high {high_52w:.2f}."
    if current_volume < 1.5 * avg_volume_50:
        return False, f"REJECTED: Volume {current_volume} below 1.5x 50-day average volume {avg_volume_50}."

    return True, "APPROVED: Right-side momentum breakout criteria met."


def can_execute_left_side_entry(
    valuation_percentile: float,
    f_score: int,
    z_score: float,
    vix_level: float,
) -> Tuple[bool, str]:
    """Validate left-side contrarian value accumulation entry conditions.

    Conditions:
        1. Macro panic state: VIX >= 30.0.
        2. Extreme valuation discount: historical valuation percentile <= 0.05 (5th percentile).
        3. Pristine balance sheet resilience: Piotroski F-Score >= 8.
        4. Zero bankruptcy risk: Altman Z-Score > 2.99 (Safe zone).

    Returns:
        Tuple[bool, str]: (is_valid, reason_message).
    """
    if vix_level < 30.0:
        return False, f"REJECTED: VIX {vix_level:.2f} not in crisis panic state (>= 30.0)."
    if valuation_percentile > 0.05:
        return False, f"REJECTED: Valuation percentile {valuation_percentile:.2%} not in bottom 5%."
    if f_score < 8:
        return False, f"REJECTED: F-Score {f_score} below extreme quality threshold of 8."
    if z_score <= 2.99:
        return False, f"REJECTED: Altman Z-Score {z_score:.2f} not in pristine safe zone (> 2.99)."

    return True, "APPROVED: Left-side contrarian accumulation criteria met."
