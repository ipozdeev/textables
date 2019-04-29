import pandas as pd
import numpy as np

import textables as tex


def example_one():
    """
    """
    df_coef = pd.DataFrame(np.random.normal(size=(2, 2)),
                           index=["const", "beta"],
                           columns=["x1", "x2"])

    df_ts = pd.DataFrame(np.abs(np.random.normal(size=(2, 2))),
                         index=["const", "beta"],
                         columns=["x1", "x2"])

    df_r2 = pd.DataFrame(np.array([[0.5, 0.75]]),
                         index=["adj. R2"],
                         columns=["x1", "x2"])

    tbl_coef = tex.TexTable(df_coef, fmt="{:.4f}")
    tbl_ts = tex.TexTable(df_ts, fmt="({:.2f})")
    tbl_r2 = tex.TexTable(df_r2, fmt="{:.2f}")

    tbl = tex.concat((tbl_coef.intertwine(tbl_ts), tbl_r2), axis=0)

    tbl.with_dcolumn().to_tabularx(textwidth=0.75, x_column_loc=0,
                                   buf="temp.tex", column_format="XWW")


if __name__ == "__main__":
    example_one()