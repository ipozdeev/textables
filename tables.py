import pandas as pd
pd.set_option("display.max_colwidth", 100)

import numpy as np
import re

from textables.functions import deem_empty


class TexTable:
    """
    Parameters
    ----------
    table : pandas.DataFrame
    fmt : str
        valid format string, such as '{:3.2f}'; for formatting to work
        properly, `table` must be of correct type, e.g. '{:3.2f}' applied
        to a table containing strings will result in a TypeError

    """
    def __init__(self, table, fmt="{}"):
        """
        """
        self._table_orig = table.copy()
        self.ncol, self.nrow = table.shape

        # deal with missing values ------------------------------------------
        # missing (either as None or np.nan) values need to be replaced
        mask_empty = table.applymap(deem_empty)

        # apply formatting
        tbl = table.applymap(fmt.format)

        # substitute empty cells with spaces
        tbl = tbl.mask(mask_empty, ' ')

        self.mask_empty = mask_empty
        self.table_fmt = tbl

    def intertwine(self, other):
        """Zip table rows with rows of another table.

        No multirow is created for the index.

        Parameters
        ----------
        other : TexTable

        Returns
        -------
        res : TexTable

        """
        tbl_up = self.table_fmt
        tbl_down = other.table_fmt.reindex(columns=tbl_up.columns)

        # zip rows of two tables (as iteration is perfomed on rows)
        table_zipped = np.vstack(zip(tbl_up.values, tbl_down.values))

        # zip index: the new index is the index of self intertwined with spaces
        new_idx = np.hstack(zip(tbl_up.index.tolist(),
                                [' ', ] * len(tbl_down.index)))

        # columns are unchanged
        new_col = tbl_up.columns

        # there goes the new table
        tbl_new = pd.DataFrame(table_zipped, index=new_idx, columns=new_col)

        return TexTable(table=tbl_new)

    @property
    def T(self):
        """Transpose table."""
        return TexTable(self.table_fmt.T, fmt="{}")

    @classmethod
    def from_model_fit(cls, coef, inference, good_of_fit=None, fmt_coef="{}",
                       fmt_inference="{}", orient_exog="columns"):
        """

        Parameters
        ----------
        coef : pandas.DataFrame
        inference : pandas.DataFrame
        good_of_fit : pandas.DataFrame or pandas.Series
        fmt_coef : str
            valid format string
        fmt_inference : str
            valid format string

        Returns
        -------

        """
        # init two tables
        tbl_coef = TexTable(table=coef, fmt=fmt_coef)
        tbl_infr = TexTable(table=inference, fmt=fmt_inference)

        # intertwine
        tbl_new = tbl_coef.intertwine(tbl_infr).table_fmt

        # add a (bottom) row for a measure of the goodness of fit
        if good_of_fit is not None:
            if orient_exog == "columns":
                axis = 0
            else:
                axis = 1
            tbl_new = pd.concat((tbl_new,
                                 good_of_fit.applymap(fmt_coef.format)),
                                axis=axis)

        return cls(table=tbl_new, fmt="{}")

    def with_dcolumn(self, delim='.', delim_index=None):
        """

        Returns
        -------

        """
        # function
        def mask_not_delimited(x):
            # discriminate between pandas.Index and pandas.DataFrame ('else')
            fmap = getattr(x, "map" if isinstance(x, pd.Index) else "applymap")
            fmsk = getattr(x, "putmask" if isinstance(x, pd.Index) else "mask")

            # format function
            ffmt = r"\multicolumn{{1}}{{c}}{{{}}}".format

            # get mask (True where there is no delimiter)
            no_delim_mask = fmap(lambda cell: delim not in cell)

            # result is \multicolumn... where no delimiter is present
            res = fmsk(no_delim_mask, fmap(ffmt))

            return res

        # copy, add all the multicolumns
        tbl = mask_not_delimited(self.table_fmt.copy())

        # columns cannot but fail to be delimited
        # columns_to_row = pd.Series(data=tbl.columns, index=tbl.columns)\
        #     .to_frame().T
        # tbl = pd.concat((columns_to_row, tbl), axis=0)
        tbl.columns = mask_not_delimited(tbl.columns)

        # if the index is delimited too, need to extract it as a column
        if delim_index:
            tbl.index = mask_not_delimited(tbl.index)

        # mask cells with no delimiters
        # TODO: handle cases with cell like '...'

        res = TexTable(table=tbl, fmt="{}")

        return res

    @classmethod
    def from_model_fit_diagonal(cls, individ, joint, orient_joint="column"):
        """

        Parameters
        ----------
        individ
        joint
        orient_joint

        Returns
        -------

        """
        raise NotImplementedError('')

        # create diagonal matrix
        b_d = pd.DataFrame(
            data=np.vstack((np.diag(individ.loc["beta", :]),
                            individ.loc[["const"], :].values)),
            index=list(individ.columns) + ["const"],
            columns=individ.columns).replace(0.0, np.nan)

        # add column with the joint model
        tbl = pd.concat((b_d, joint.rename("joint")), axis=1)

        # swap columns to ensure diagonal look
        tbl = tbl.loc[list(individ.columns) + ["const"],
                      list(individ.columns) + ["joint"]]

        res = cls(table=tbl)

        return res

    def to_tabular(self, **kwargs):
        """Format table for tabular environment.

        Keyword arguments of `pandas.to_latex` are preserved.

        Parameters
        ----------
        kwargs

        Returns
        -------
        res : str or None

        """
        # pop buf is it exists in `kwargs` to avoid duplicates in .to_latex()
        buf_old = kwargs.pop("buf", None)

        tex_tbl_str = self.table_fmt.to_latex(**kwargs)

        # now, stick to the actually provided `buf`
        if buf_old is not None:
            # mimic the case when `buf` was something rather than None
            with open(buf_old, mode='w') as fname:
                fname.write(tex_tbl_str)
        else:
            # mimic the case of `buf`=None - just return the string
            return tex_tbl_str

        return

    def to_tabularx(self, textwidth=1.0, x_column_loc=0, **kwargs):
        """Format table for tabularx environment.

        The environment is distinguished by having 'tabularx' instead of
        'tabular' in \begin and \end and the setting \textwidth right after
        \begin. Keyword arguments of `pandas.to_latex` are preserved.

        Parameters
        ----------
        textwidth : float
            \textwidth argument to tabularx environment
        kwargs

        Returns
        -------
        res : str or None

        """
        # pop buf is it exists in `kwargs` to avoid duplicates in .to_latex()
        buf_old = kwargs.pop("buf", None)

        # change a specific column to 'X'
        # if column_format is part of `kwargs`, use it and substitute the X
        #   column, else construct a new column_format from right-ragged
        #   columns and the X-column placed in front
        column_format = kwargs.pop("column_format",
                                   'l'*(self.table_fmt.index.nlevels +
                                        self.table_fmt.shape[1]))
        column_format = column_format[:x_column_loc] + 'X' + \
            column_format[x_column_loc:][1:]
        kwargs.update({"column_format": column_format})

        # move table to string to replace stuff
        tex_tbl_str = self.table_fmt.to_latex(buf=None, **kwargs)

        # replace with tabularx isntead of tabular
        tex_tbl_str = re.sub(
            'begin{tabular}',
            'begin{tabularx}{%s\\\\textwidth}' % (textwidth),
            tex_tbl_str)
        tex_tbl_str = re.sub('end{tabular}', 'end{tabularx}', tex_tbl_str)

        # now, stick to the actually provided `buf`
        if buf_old is not None:
            # mimic the case when `buf` was something rather than None
            with open(buf_old, mode='w') as fname:
                fname.write(tex_tbl_str)
        else:
            # mimic the case of `buf`=None - just return the string
            return tex_tbl_str


if __name__ == "__main__":
    pass
