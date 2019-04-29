import numpy as np
import pandas as pd
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


def to_diagonal(ser):
    """Make diagonal table with na off-diagonal.

    Parameters
    ----------
    ser : pandas.Series

    Returns
    -------

    """
    assert isinstance(ser, pd.Series)

    # place `ser` on the diagonal main
    df = pd.DataFrame(data=np.diag(ser),
                      index=ser.index,
                      columns=ser.index)

    # put na off-diagonal
    mask = pd.DataFrame(data=np.diag(np.ones((len(ser)))),
                        index=ser.index,
                        columns=ser.index).replace(0.0, np.nan).notnull()

    df = df.where(mask)

    return df
