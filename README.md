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
