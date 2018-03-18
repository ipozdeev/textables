import unittest
import pandas as pd
import numpy as np

from textables.tables import TexTable


class TestTables(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        df_coef = pd.DataFrame(np.eye(2) * 3, index=["alpha", "beta"],
                               columns=["model_1", "model_2"])
        #
        df_coef.iloc[0, 0] = None

        df_tstat = pd.DataFrame(np.eye(2), index=["alpha", "beta"],
                               columns=["model_1", "model_2"])
        df_tstat.iloc[0, 0] = None

        fmt_coef = '{:3.2f}'

        self.df_coef = df_coef
        self.df_tstat = df_tstat
        self.fmt_coef = fmt_coef

    def test_textable(self):
        """Test [0, 0] element is ' ' (space)."""
        tbl = TexTable(table=self.df_coef)

        self.assertEqual(tbl.table_fmt.iloc[0, 0], ' ')

    def test_from_model_fit(self):
        """Test nrows = 2*nrows of df_coef, tstats in parentheses."""
        tbl = TexTable.from_model_fit(self.df_coef, self.df_tstat,
                                      fmt_inference="({:3.2f})")

        self.assertEqual(tbl.table_fmt.shape[0], self.df_coef.shape[0] * 2)
        self.assertEqual(tbl.table_fmt.iloc[3,0][0], '(')

    def test_with_dcolumn(self):
        """Test the empty cell is a multicolumn now."""
        tbl = TexTable(table=self.df_coef)
        res = tbl.with_dcolumn(delim='.', delim_index=True)

        self.assertEqual(res.table_fmt.iloc[0, 0], "\multicolumn{1}{c}{ }")


if __name__ == "__main__":
    unittest.main()