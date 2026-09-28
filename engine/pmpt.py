"""Post-Modern Portfolio Theory (PMPT) and Sortino Ratio Optimization Module.

This module implements the mathematical formulations of Sortino & van der Meer (1991)
and Sortino & Price (1994) for downside deviation and the Sortino ratio.
"""

from typing import Union, Sequence
import numpy as np


def calculate_downside_deviation(
    returns: Union[Sequence[float], np.ndarray],
    mar: float = 0.0,
    annualized: bool = True,
    periods_per_year: int = 252,
) -> float:
    """Calculate the Downside Deviation (Target Semivariance root) relative to MAR.

    Formula:
        DD = sqrt( (1 / T) * sum( min(0, R_t - MAR)^2 ) )

    Args:
        returns: Array-like sequence of periodic asset returns (e.g. daily simple returns).
        mar: Periodic Minimum Acceptable Return (default 0.0).
        annualized: Whether to annualize the downside deviation.
        periods_per_year: Number of trading periods in a year (e.g. 252 for daily).

    Returns:
        float: Downside deviation.

    Raises:
        ValueError: If returns array is empty or periods_per_year <= 0.
    """
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("Return series cannot be empty.")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive.")

    # Calculate negative deviations from MAR
    underperformance = np.minimum(0.0, arr - mar)
    target_semivariance = np.mean(underperformance ** 2)
    dd_periodic = np.sqrt(target_semivariance)

    if annualized:
        return float(dd_periodic * np.sqrt(periods_per_year))
    return float(dd_periodic)


def calculate_sortino_ratio(
    returns: Union[Sequence[float], np.ndarray],
    mar: float = 0.0,
    annualized_mar: bool = False,
    periods_per_year: int = 252,
) -> float:
    """Calculate the Sortino Ratio.

    Formula:
        Sortino = (R_p - MAR) / DownsideDeviation

    Args:
        returns: Array-like sequence of periodic asset returns (e.g. daily simple returns).
        mar: Minimum Acceptable Return (either periodic or annual depending on annualized_mar).
        annualized_mar: True if the input `mar` is already an annual rate (e.g., 0.03 for 3%).
        periods_per_year: Number of trading periods in a year (252 for daily).

    Returns:
        float: Sortino Ratio. Returns np.inf if there is zero downside deviation and positive excess return.
    """
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("Return series cannot be empty.")

    if annualized_mar:
        annual_mar = mar
        periodic_mar = (1.0 + mar) ** (1.0 / periods_per_year) - 1.0
    else:
        periodic_mar = mar
        annual_mar = (1.0 + mar) ** periods_per_year - 1.0

    mean_periodic_return = float(np.mean(arr))
    annualized_return = mean_periodic_return * periods_per_year

    annualized_dd = calculate_downside_deviation(
        arr, mar=periodic_mar, annualized=True, periods_per_year=periods_per_year
    )

    excess_return = annualized_return - annual_mar

    if annualized_dd == 0.0:
        if excess_return > 0.0:
            return float(np.inf)
        elif excess_return == 0.0:
            return 0.0
        else:
            return float(-np.inf)

    return float(excess_return / annualized_dd)
