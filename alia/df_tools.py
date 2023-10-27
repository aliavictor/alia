from IPython.display import display, HTML
from .tools import *


def reset(df):
    """
    Resets the index of a DataFrame (shortcut for `df.reset_index(drop=True)`).

    Args:
        df (pd.DataFrame): DataFrame to reference

    Returns:
        pd.DataFrame: The passed DataFrame with its indexes reset
    """
    return df.reset_index(drop=True)


def drop(df, cols):
    """
    Drops given columns from a DataFrame (shortcut for `df.drop([cols],axis=1)`). Also works on lists.

    Args:
        df (pd.DataFrame, list): DataFrame or list to reference
        cols (list): Columns/items to drop

    Returns:
        pd.DataFrame: The passed dataFrame/list with the given columns/items removed

    Example:
        Given a dataframe `df`:

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  1 | dog      | Biscuit |     3 |
        |  2 | cat      | Binx    |     5 |
        ```

        >>> drop(df, cols=["age"])

        ```
        |    | animal   | name    |
        |----|----------|---------|
        |  0 | dog      | Fido    |
        |  1 | dog      | Biscuit |
        |  2 | cat      | Binx    |
        ```
    """
    if isinstance(cols, str):
        if "," in cols:
            cols = [i.strip() for i in cols.split(",")]
        else:
            cols = [cols]
    if type(df) != list:
        cols = [i for i in cols if i in list(df.columns)]
        if not is_empty(cols):
            return df.drop(cols, axis=1)
        else:
            return df
    else:
        for c in cols:
            with supp(ValueError):  # suppresses ValueErrors
                df.remove(c)
        return df


def keep(df, cols):
    """
    Shortcut for `df[[i for i in list(df.columns) if i in cols]]`.

    Args:
        df (pd.DataFrame): DataFrame to reference
        cols (list): Columns to keep

    Returns:
        pd.DataFrame: The given dataframe with only the passed columns

    Example:
        Given a dataframe `df`:

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  1 | dog      | Biscuit |     3 |
        |  2 | cat      | Binx    |     5 |
        ```

        >>> keep(df, cols=["animal", "name"])

        ```
        |    | animal   | name    |
        |----|----------|---------|
        |  0 | dog      | Fido    |
        |  1 | dog      | Biscuit |
        |  2 | cat      | Binx    |
        ```
    """
    if type(cols) == str:
        if "," in cols:
            cols = [i.strip() for i in cols.split(",")]
        else:
            cols = [cols]

    return df[[i for i in list(df.columns) if i in cols]]


def set_none(df):
    """
    Shortcut for `df.where(~pd.isnull(df), None)`.

    Args:
        df (pd.DataFrame): DataFrame to reference

    Returns:
        pd.DataFrame: `df.where(~pd.isnull(df), None)`
    """
    return df.where(~pd.isnull(df), None)


def prettydf(df):
    """
    Makes raw strings in a DataFrame printable strings.

    Args:
        df (pd.DataFrame): DataFrame to reference

    Returns:
        pd.DataFrame: A dataframe where strings are shown as printable strings not raw strings
    """
    return display(HTML(df.to_html().replace("\\n", "<br>")))


def dedupe(df, cols=None, ix=False):
    """
    Shortcut for `df.drop_duplicates(subset=cols)`.

    Args:
        df (pd.DataFrame): DataFrame to reference
        cols (list): Subset of columns to dedupe by
        ix (bool): If `True` original dataframe indexes are kept, otherwise they're reset

    Returns:
        pd.DataFrame: A dataframe deduped based on the given columns

    Examples:
        Given a dataframe `df`:

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  1 | dog      | Fido    |     3 |
        |  2 | cat      | Binx    |     5 |
        |  3 | dog      | Biscuit |     6 |
        ```

        >>> dedupe(df, cols=["animal", "name"])

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  1 | cat      | Binx    |     5 |
        |  2 | dog      | Biscuit |     6 |
        ```

        >>> dedupe(df, cols=["animal", "name"], ix=True)

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  2 | cat      | Binx    |     5 |
        |  3 | dog      | Biscuit |     6 |
        ```
    """
    if cols is not None:
        if type(cols) == str:
            split_str = bool(contains(",", cols) is not None and cols.strip() != ",")
            if split_str:
                cols = [i.strip() for i in cols.split(",")]
            else:
                cols = [cols]
        if ix:
            return df.drop_duplicates(subset=cols)
        else:
            return reset(df.drop_duplicates(subset=cols))
    else:
        if ix:
            return df.drop_duplicates()
        else:
            return reset(df.drop_duplicates())


def todict(df, ix, cols=None):
    """
    Creates a dictionary/map from a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to reference
        ix (str): The column to group by (becomes the keys of the returned dictionary
        cols (list): Columns of the DataFrame to include in the retuned dictionary

    Returns:
        dict: Dictionary created from the passed DataFrame grouping on the given `ix` value

    Examples:
        Given a dataframe `df`:

        ```
        |    | animal   | name    |   age |
        |----|----------|---------|-------|
        |  0 | dog      | Fido    |     2 |
        |  1 | cat      | Binx    |     5 |
        |  2 | dog      | Biscuit |     6 |
        ```

        >>> todict(df, "animal")

        ```
        {'name': {'dog': 'Biscuit', 'cat': 'Binx'}, 'age': {'dog': 6, 'cat': 5}}
        ```

        >>> todict(df, "animal", cols=["name"])

        ```
        {'dog': 'Biscuit', 'cat': 'Binx'}
        ```
    """
    def merge(df, ix, cols):
        dicts = []
        for c in cols:
            exec(f"temp = df.set_index('{ix}')['{c}'].to_dict()")
            dicts.append({k: {c: v} for k, v in locals()["temp"].items()})
        dd = {}
        for d in dicts:
            for k, v in d.items():
                if k not in keys(dd):
                    dd[k] = {}
                for y, z in v.items():
                    dd[k][y] = z
        return dd

    try:
        if cols:
            if type(cols) == str and cols.lower() == "all":
                return merge(df, ix=ix, cols=[i for i in list(df.columns) if i != ix])
            if type(cols) != list:
                cols = [i.strip() for i in cols.split(",")]
            if len(cols) == 1:
                return df.set_index(ix)[cols[0]].to_dict()
            else:
                return merge(df, ix=ix, cols=cols)
        else:
            return df.set_index(ix).to_dict()
    except AttributeError:
        pass
    except Exception as e:
        red(f"<b>ERROR:</b>\n{e}", ts=False)


def pdnull(series):
    """
    Checks for null values in a series.

    Args:
        series (pd.Series): Series to be reference

    Returns:
        pd.Series: A series of booleans indicating if the value of that index is null
    """
    if type(series) == pd.DataFrame:
        return (series.isnull()) | (
            series.isin(["", None, "nan", "NaN", "None", "NaT", pd.NaT])
        )
    else:
        fm = lambda x: pd.isnull(x) or x in [
            "",
            None,
            "nan",
            "NaN",
            "None",
            "NaT",
            pd.NaT,
        ]
        return series.apply(fm)


def unique(series, as_list=True):
    """
    Dedupes a given series or list.

    Args:
        series (pd.Series, list): Series or list to reference
        as_list (bool): If `False` the output is printed instead of returned

    Returns:
        list: A list containing unique values from the given series/list

    Example:
        Given a series `animals`:

        ```
        |    | animal   |
        |----|----------|
        |  0 | dog      |
        |  1 | cat      |
        |  2 | dog      |
        ```

        >>> unique(animals)

        ```
        ['dog', 'cat']
        ```
    """
    if isinstance(series, pd.Series):
        out = list(series.unique())
    else:
        out_temp = set()
        out_add = out_temp.add
        out = [x for x in series.copy() if not (x in out_temp or out_add(x))]
    if as_list:
        return out
    else:
        print("\n".join(out))
