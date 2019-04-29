import unittest
import pandas as pd
import numpy as np
import re
import os

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

        self.temp_filename = "temp.tex"
        self.df_coef = df_coef
        self.df_tstat = df_tstat
        self.fmt_coef = fmt_coef

    def tearDown(self):
        """
        """
        try:
            os.remove(self.temp_filename)
        except FileNotFoundError:
            pass

    def test_textable(self):
        """Test [0, 0] element is ' ' (space)."""
        tbl = TexTable(table=self.df_coef)

        self.assertEqual(tbl.table_fmt.iloc[0, 0], ' ')

    def test_to_tabular(self):
        """Test formatting to tabular."""
        tbl = TexTable(table=self.df_coef)
        tbl_str = tbl.to_tabular(buf=None)

        self.assertTrue(re.search("begin{tabular}", tbl_str))

    def test_to_tabular_output(self):
        """Test formatting to tabular."""
        tbl = TexTable(table=self.df_coef)
        tbl.to_tabular(buf=self.temp_filename)

        self.assertTrue(self.temp_filename in os.listdir('./'))

    def test_to_tabularx(self):
        """Test formatting to tabularx."""
        tbl = TexTable(table=self.df_coef)
        tbl_str = tbl.to_tabularx(buf=None)

        self.assertTrue(re.search("begin{tabularx}{1.0\\\\textwidth}",
                                  tbl_str))

    def test_intertwine(self):
        """Test nrows = 2*nrows of df_coef, tstats in parentheses."""
        tbl_1 = TexTable(self.df_coef, fmt="{:3.2f}")
        tbl_2 = TexTable(self.df_tstat, fmt="({:3.2f})")

        tbl = tbl_1.intertwine(tbl_2)

        self.assertEqual(tbl.table_fmt.shape[0], self.df_coef.shape[0] * 2)
        self.assertEqual(tbl.table_fmt.iloc[3, 0][0], '(')

    def test_with_dcolumn(self):
        """Test the empty cell is a multicolumn now."""
        tbl = TexTable(table=self.df_coef)
        res = tbl.with_dcolumn(delim='.', delim_index=True)

        self.assertEqual(res.table_fmt.iloc[0, 0], "\multicolumn{1}{c}{ }")

        res.to_tabular(buf="temp.tex", escape=False)


if __name__ == "__main__":
    unittest.main()
