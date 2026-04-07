import numpy as np
import statsmodels.api as sm
import pandas as pd
from scipy.stats import f

def detect_trend(da):
    """
    Detect a linear trend in a 1D xarray DataArray, ignoring NaNs.

    Parameters
    ----------
    da : xarray.DataArray
        1D array with a 'time' coordinate. NaNs are ignored.

    Returns
    -------
    trend : list of tuple
        List of (intercept, slope_per_year) for each segment. Currently returns
        a single segment.

    Example
    -------
    >>> detect_trend(da)
    [(intercept, slope_per_year)]
    """
    t = pd.to_datetime(da.time.values)
    x = (t - t[0]).days / 365.25
    y = da.values
    N = len(y)
    
    # Mask NaNs
    mask = ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]
    index_map = np.where(mask)[0]  # map back to original indices

    trend = []
    best_rss = np.inf
    
    # --- 1 segment
    X = sm.add_constant(x_clean)
    model = sm.OLS(y_clean, X).fit()
    rss = np.sum(model.resid**2)
    best_rss = rss
    trend = [(model.params[0], model.params[1])]
    
    return trend

def detect_trend_segments(da, max_segments=3):
    """
    Detect piecewise linear trends in a 1D xarray DataArray, ignoring NaNs.

    Parameters
    ----------
    da : xarray.DataArray
        1D array with a 'time' coordinate. NaNs are ignored.
    max_segments : int, optional
        Maximum number of linear segments to detect (default is 3).

    Returns
    -------
    break_idx : list of int
        Indices in the original array where trend changes occur.
    trends : list of tuple
        List of (intercept, slope_per_year) for each segment.

    Example
    -------
    >>> breaks, trends = detect_trend_segments(da, max_segments=2)
    >>> breaks
    [5]
    >>> trends
    [(intercept1, slope1), (intercept2, slope2)]
    """
    t = pd.to_datetime(da.time.values)
    x = (t - t[0]).days / 365.25
    y = da.values
    N = len(y)
    
    # Mask NaNs
    mask = ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]
    index_map = np.where(mask)[0]  # map back to original indices

    best_breaks = []
    best_trends = []
    best_rss = np.inf
    
    # --- 1 segment
    X = sm.add_constant(x_clean)
    model = sm.OLS(y_clean, X).fit()
    rss = np.sum(model.resid**2)
    best_rss = rss
    best_trends = [(model.params[0], model.params[1])]
    best_breaks = []
    
    # --- 2 segments
    for split in range(len(y_clean)//10, len(y_clean)-len(y_clean)//10):
        # split indices in cleaned array
        X1 = sm.add_constant(x_clean[:split])
        y1 = y_clean[:split]
        X2 = sm.add_constant(x_clean[split:])
        y2 = y_clean[split:]
        if len(y1) < 2 or len(y2) < 2:
            continue
        model1 = sm.OLS(y1, X1).fit()
        model2 = sm.OLS(y2, X2).fit()
        rss_total = np.sum(model1.resid**2) + np.sum(model2.resid**2)
        if rss_total < best_rss:
            best_rss = rss_total
            best_breaks = [index_map[split]]  # map to original index
            best_trends = [(model1.params[0], model1.params[1]),
                           (model2.params[0], model2.params[1])]
    
    # # --- 3 segments
    # for i in range(len(y_clean)//10, len(y_clean)-2*len(y_clean)//10):
    #     for j in range(i+len(y_clean)//10, len(y_clean)-len(y_clean)//10):
    #         X1 = sm.add_constant(x_clean[:i])
    #         X2 = sm.add_constant(x_clean[i:j])
    #         X3 = sm.add_constant(x_clean[j:])
    #         y1 = y_clean[:i]
    #         y2 = y_clean[i:j]
    #         y3 = y_clean[j:]
    #         if len(y1)<2 or len(y2)<2 or len(y3)<2:
    #             continue
    #         model1 = sm.OLS(y1, X1).fit()
    #         model2 = sm.OLS(y2, X2).fit()
    #         model3 = sm.OLS(y3, X3).fit()
    #         rss_total = np.sum(model1.resid**2) + np.sum(model2.resid**2) + np.sum(model3.resid**2)
    #         if rss_total < best_rss:
    #             best_rss = rss_total
    #             best_breaks = [index_map[i], index_map[j]]
    #             best_trends = [(model1.params[0], model1.params[1]),
    #                            (model2.params[0], model2.params[1]),
    #                            (model3.params[0], model3.params[1])]
    
    return best_breaks, best_trends

def test_breakpoint_significance(da, break_idx):
    """
    Test if a proposed breakpoint significantly improves a linear fit.

    Parameters
    ----------
    da : xarray.DataArray
        1D time series with a 'time' coordinate.
    break_idx : int
        Index of the proposed breakpoint in the series.

    Returns
    -------
    dict
        Dictionary with statistics comparing 1-segment vs 2-segment fits:
        - rss_1seg, rss_2seg : float
            Residual sum of squares for 1- and 2-segment models.
        - F_stat : float
            F-statistic for improvement in fit.
        - p_value : float
            P-value for the F-test.
        - aic_1seg, aic_2seg : float
            Akaike Information Criterion for 1- and 2-segment models.
        - bic_1seg, bic_2seg : float
            Bayesian Information Criterion for 1- and 2-segment models.

    Raises
    ------
    ValueError
        If `break_idx` is outside the valid range of the series.

    Example
    -------
    >>> stats = test_breakpoint_significance(da, break_idx=5)
    >>> stats['p_value']
    0.03
    """
    # Prepare data
    t = pd.to_datetime(da.time.values)
    x = (t - t[0]).days / 365.25
    y = da.values
    mask = ~np.isnan(y)
    x = x[mask]
    y = y[mask]
    
    n = len(y)
    
    # --- 1-segment model
    X1 = sm.add_constant(x)
    model1 = sm.OLS(y, X1).fit()
    rss1 = np.sum(model1.resid**2)
    p1 = len(model1.params)
    aic1 = model1.aic
    bic1 = model1.bic
    
    # --- 2-segment model
    # Ensure breakpoint is inside valid range
    if break_idx <= 0 or break_idx >= n:
        raise ValueError("break_idx must be within the series length")
    
    X2_1 = sm.add_constant(x[:break_idx])
    y2_1 = y[:break_idx]
    X2_2 = sm.add_constant(x[break_idx:])
    y2_2 = y[break_idx:]
    
    model2_1 = sm.OLS(y2_1, X2_1).fit()
    model2_2 = sm.OLS(y2_2, X2_2).fit()
    
    rss2 = np.sum(model2_1.resid**2) + np.sum(model2_2.resid**2)
    p2 = len(model2_1.params) + len(model2_2.params)
    
    # F-test
    F_stat = ((rss1 - rss2) / (p2 - p1)) / (rss2 / (n - p2))
    p_value = 1 - f.cdf(F_stat, dfn=p2 - p1, dfd=n - p2)
    
    # AIC/BIC for 2-segment model
    # Use log-likelihood approximation
    sigma2 = rss2 / n
    loglik2 = -n/2 * np.log(2 * np.pi * sigma2) - rss2 / (2*sigma2)
    aic2 = -2*loglik2 + 2*p2
    bic2 = -2*loglik2 + p2*np.log(n)
    
    return {
        "rss_1seg": rss1,
        "rss_2seg": rss2,
        "F_stat": F_stat,
        "p_value": p_value,
        "aic_1seg": aic1,
        "bic_1seg": bic1,
        "aic_2seg": aic2,
        "bic_2seg": bic2
    }
