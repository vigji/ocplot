import numpy as np


def get_pval_stars(test_result):
    """Get number of stars or n.s. from p-values. Convention:
        - p < 0.001: ***
        - p < 0.01: **
        - p < 0.5: *
        - p > 0.5: n.s.

    Parameters
    ----------
    test_result : float or scipy stats Result with pval attribute
        Number or test to label with stars

    Returns
    -------
    str
        string describing the result.

    """
    if type(test_result) not in [float, np.float64]:
        test_result = test_result.pvalue

    if test_result <= 0.0001:
        return "****"
    if test_result <= 0.001:
        return "***"
    elif test_result <= 0.01:
        return "**"
    elif test_result <= 0.05:
        return "*"
    else:
        return "n.s."
