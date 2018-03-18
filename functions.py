import numpy as np
import re


def deem_empty(cell):
    """

    Parameters
    ----------
    cell

    Returns
    -------

    """
    if type(cell) == str:
        return bool(re.match("^ +$", cell)) or (cell == '')
    elif cell is None:
        return True
    else:
        try:
            return np.isnan(cell)
        except TypeError:
            return False
