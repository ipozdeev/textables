# textables
Generation of tex tables from pandas dataframes.

Slightly improves the functionality of `pandas.to_latex()` to ease creation of tables for academic publications. Might be a bit finance-centric.

## Installation
Clone the repo into `Lib/site-packages/` of your Python installation:
```
git clone https://github.com/ipozdeev/textables
```
and import with
```python
from textables.tables import TexTable
```

## Functionality
`TexTable(table)` takes a `pandas.DataFrame` as input and creates an instance of `TexTable`. From here, you can:
  * translate this table into [dcolumn](https://ctan.org/pkg/dcolumn?lang=en "LaTeX dcolumn package")-compatible table;
  * write to `tabular` or `tabularx`.
  
 There are convenience methods for:
   * generation of tables where cells are (coefficient, its standard error) pairs;
   
## Examples
Say, you have estimated two linear models, each with a constant and one coefficient, such that the coefficient estimates might look like:
```python
df_coef = pd.DataFrame(np.random.normal(size=(2, 2)),
                       index=["const", "beta"],
                       columns=["x1", "x2"])
```
and the standard errors might look like:
```python
df_coef = pd.DataFrame(np.random.normal(size=(2, 2)),
                       index=["const", "beta"],
                       columns=["x1", "x2"])
```
and the two R-squareds might look like:
```python
df_r2 = pd.DataFrame(np.array([[0.5, 0.75]]),
                     index=["adj. R2"],
                     columns=["x1", "x2"])
```
You can create the following table out of it, where t-stats are in parentheses below respective estimates, and all values are centered at the delimiter:

<img src="https://github.com/ipozdeev/textables/blob/master/examples/example_table.PNG" alt="example table" width="300">

with th efollowing code (check section `examples/`):
```python
import textables as tex

# construct TexTable instances
tbl_coef = tex.TexTable(df_coef, fmt="{:.4f}")
tbl_ts = tex.TexTable(df_ts, fmt="({:.2f})")
tbl_r2 = tex.TexTable(df_r2, fmt="{:.2f}")

# intertwine + concat to r-squareds
tbl = tex.concat((tbl_coef.intertwine(tbl_ts), tbl_r2), axis=0)

# output to tabularx with dcolumn
tbl.with_dcolumn().to_tabularx(textwidth=0.75, x_column_loc=0,
                               buf="temp.tex", column_format="XWW")
```
which would produce file temp.tex bound to work with:
```latex
\documentclass[a4paper, 12pt]{article}

% language
\usepackage[USenglish]{babel}

% tables
\usepackage{tabularx}
\usepackage{dcolumn}
\newcolumntype{W}{>{\raggedleft}D{.}{.}{4}}

\begin{document}

\input{temp.tex}

\end{document}
```
