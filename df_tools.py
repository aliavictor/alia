from IPython.display import display, HTML
from .helpers import *


def reset(df):
    "Simply returns df.reset_index(drop=True)"
    return df.reset_index(drop=True)


def drop(df, cols):
    """
    Shortcut for df.drop([cols],axis=1). You can also pass a list as the df value
    and items in cols will be removed.
    """
    if type(cols) == str:
        if "," in cols:
            cols = [i.strip() for i in cols.split(",")]
        else:
            cols = [cols]
    if type(df) != list:
        cols = [i for i in cols if i in list(df.columns)]
        if not empty(cols):
            return df.drop(cols, axis=1)
        else:
            return df
    else:
        for c in cols:
            with supp(ValueError):
                df.remove(c)
        return df


def keep(df, cols):
    """Shortcut for df[[i for i in list(df.columns) if i in cols]]"""
    if type(cols) == str:
        if "," in cols:
            cols = [i.strip() for i in cols.split(",")]
        else:
            cols = [cols]
    return df[[i for i in list(df.columns) if i in cols]]


def set_none(df):
    "df.where(~pd.isnull(df),None)"
    return df.where(~pd.isnull(df), None)


def prettydf(df):
    """Returns a df where strings are shown as printable strings not raw strings"""
    return display(HTML(df.to_html().replace("\\n", "<br>")))


def dedupe(df, cols=None, ix=False):
    """
    Basically shortcut to df.drop_duplicates()/df.drop_duplicates(subset=cols)
    depending on if cols are passed. When ix=True original indexes are kept,
    otherwise they're reset.
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
    """Creates a dictionary/map from a df. ix = the column to group by (becomes the
    keys of the outputted dictionary)"""

    def merge(df, ix, cols):
        global dicts
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
        red("<b>ERROR:</b>\n{e}", ts=False)


def pdnull(series):
    """
    Essentially applies isnull() on a series and returns it
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


def unique(series, as_list=True, color=None):
    """
    Returns list(series.unique()) (e.g. list(df['uri'].unique())). When
    as_list=False nothing is returned and list is printed instead. Color should
    be the color print function to use, e.g. color='teal'.
    """
    if type(series) == pd.Series:
        out = list(series.unique())
    else:
        out_temp = set()
        out_add = out_temp.add
        out = [x for x in series.copy() if not (x in out_temp or out_add(x))]
    if as_list:
        return out
    else:
        if color:
            if type(color) == str:
                cmap = {
                    "teal": teal,
                    "light_teal": light_teal,
                    "blue": blue,
                    "pink": pink,
                    "purple": purple,
                    "violet": violet,
                    "red": red,
                    "dark_red": dark_red,
                    "green": green,
                    "orange": orange,
                }
                cmap[color]("\n".join(out), ts=False)
            else:
                pcolor("\n".join(out), color, ts=False)
        else:
            print("\n".join(out))
