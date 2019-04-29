import pandas as pd

from textables.tables import TexTable


def concat(tup, axis=0, merge_columns=True):
    """

    Parameters
    ----------
    tup : list-like
        of instances of `TexTable`
    axis
    merge_columns

    Returns
    -------
    res : TexTable

    """
    if not merge_columns:
        raise NotImplementedError("Not yet implemented.")

    new_tbl = pd.concat([t.table for t in tup], axis=axis)

    res = TexTable(new_tbl, fmt="{}")

    return res
