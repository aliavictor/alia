from datetime import datetime, date, timedelta
import difflib
from dotenv import load_dotenv, dotenv_values
import os
import pandas as pd
import pyperclip
from dateutil.parser import parse
import calendar
from .colors import *


def clipboard(x):
    """Copies text to clipboard so it can be pasted anywhere."""
    pyperclip.copy(x)
    green("Copied to clipboard", ts=False)


def tformat(date_obj, style=None):
    """
    When style is None default datetime format is %Y-%m-%d %H:%M:%S
    and default date format is %Y-%m-%d.
    """
    if type(date_obj) not in [datetime, date]:
        if ":" in date_obj:
            date_obj = todt(date_obj)
        else:
            date_obj = todt(date_obj, as_date=True)
    if style is None:
        if type(date_obj) == datetime:
            style = "%Y-%m-%d %H:%M:%S"
        elif type(date_obj) == date:
            style = "%Y-%m-%d"
    return date_obj.strftime(style)


def todt(dt_str=None, as_date=False):
    """
    Takes a datetime string and converts it to an actual datetime object.
    When as_date=True a date - not datetime - object is returned.
    """
    if dt_str is None:
        dt_str = now()
    elif "_" in dt_str:
        dt_str = dt_str.replace("_", "-")

    if as_date:
        return parse(dt_str).date()
    else:
        return parse(dt_str)


def now(style="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(style)


def monthdays(month, year=todt(now()).year):
    """Returns total days in a given month."""
    if type(month) == str:
        if len(month) == 4:
            try:
                out = calendar.monthrange(
                    year, datetime.strptime(month[:3], "%b").month
                )
            except:
                red(
                    "If passing a month abbreviation, it must be a <b>3 letter</b> abbreviation",
                    ts=False,
                )
                return None
        elif len(month) == 3:
            out = calendar.monthrange(year, datetime.strptime(month, "%b").month)
        elif len(month) > 4:
            try:
                out = calendar.monthrange(year, datetime.strptime(month, "%B").month)
            except:
                red(
                    "Can't parse passed month string; try passing month as an integer",
                    ts=False,
                )
                return None
    elif type(month) == int:
        out = calendar.monthrange(year, month)
    return out[1]


def bomonth(month=todt(now()).month, year=todt(now()).year, offset=0, style="%Y-%m-%d"):
    """Returns the first of the given month (current month is default)."""
    if type(month) == str:
        if len(month) == 4:
            try:
                month = datetime.strptime(month[:3], "%b").month
            except:
                red(
                    "If passing a month abbreviation, it must be a <b>3 letter</b> abbreviation",
                    ts=False,
                )
                return None
        elif len(month) == 3:
            month = datetime.strptime(month, "%b").month
        elif len(month) > 4:
            try:
                month = datetime.strptime(month, "%B").month
            except:
                red(
                    "Can't parse passed month string; try passing month as an integer",
                    ts=False,
                )
                return None
    if offset != 0:
        if month <= 2:
            month = 13 + offset
            year = todt(dt_int(-60)).year
        else:
            month = month + offset
    rawdate = todt(f"{year}-{month}-01")
    return tformat(rawdate, style=style)


def eomonth(month=todt(now()).month, year=todt(now()).year, offset=0, style="%Y-%m-%d"):
    """Returns the last day of the given month (current month is default)."""
    if type(month) == str:
        if len(month) == 4:
            try:
                month = datetime.strptime(month[:3], "%b").month
            except:
                red(
                    "If passing a month abbreviation, it must be a <b>3 letter</b> abbreviation",
                    ts=False,
                )
                return None
        elif len(month) == 3:
            month = datetime.strptime(month, "%b").month
        elif len(month) > 4:
            try:
                month = datetime.strptime(month, "%B").month
            except:
                red(
                    "Can't parse passed month string; try passing month as an integer",
                    ts=False,
                )
                return None
    if offset != 0:
        month = month + offset
    last_day = monthdays(month)
    rawdate = todt(f"{year}-{month}-{last_day}")
    return tformat(rawdate, style=style)


def utcdt(x):
    """
    Returns timezone-converted timestamp from PostgreSQL/UTC
    (x example: '2019-11-25 14:14:36.822062+00')
    """
    if type(x) not in [pd._libs.tslibs.timestamps.Timestamp, datetime, date]:
        localized = pd.to_datetime(todt(x)).tz_convert("US/Eastern").tz_localize(None)
    else:
        localized = x.tz_convert("US/Eastern").tz_localize(None)
    return pd.to_datetime(localized.strftime("%Y-%m-%d %H:%M:%S"))


def dt_int(num, start=None, metric="days", style="%Y-%m-%d"):
    """
    Returns formatted date with subtracted/added days. Make days negative to
    subtract days. Metric options are days, minutes or hours.
    """
    if start is None:
        start = datetime.now()
    elif type(start) == str:
        if " " in start:
            start = todt(start)
        else:
            start = todt(start, as_date=True)
    opts = ["days", "minutes", "hours"]
    actual = difflib.get_close_matches(metric.lower(), opts, cutoff=0.7)
    if len(actual) == 1:
        metric = actual[0]
    else:
        if len(actual) > 1:
            orange(
                f"Multiple metric options found ({', '.join(actual)}). Which did you mean?",
                ts=False,
            )
        elif len(actual) == 0:
            red("Metric value seems to be incorrect, try again", ts=False)
        print("")
        metric = str(input("days, minutes or hours? "))
        actual = difflib.get_close_matches(metric.lower(), opts, cutoff=0.7)
        if len(actual) == 1:
            metric = actual[0]
        else:
            red("Having trouble recognizing metric")
            return None
    if metric != "days":
        t_check = [i for i in ["%H", "%-H", "%I", "%-I"] if i in style]
        if len(t_check) == 0:
            style = f"{style} %H:%M:%S"
    if metric == "days":
        out = (start + timedelta(days=num)).strftime(style)
    elif metric == "hours":
        out = (start + timedelta(hours=num)).strftime(style)
    elif metric == "minutes":
        out = (start + timedelta(minutes=num)).strftime(style)
    return out


def daydiff(start, stop=None):
    """Returns number of days between two date strings. When stop=None default is current day"""
    start = todt(str(start))
    if stop is None:
        stop = todt(now())
    else:
        stop = todt(str(stop))
    return (stop - start).days


def elapsed(start, stop=None, full=False, metric="minutes"):
    """
    Pass a datetime.datetime object and return elapsed time from then to now. Metric opts:
    seconds, minutes, hours. When full=True elapsed time is returned as H:M:S.
    """
    opts = ["minutes", "hours", "seconds"]
    actual = difflib.get_close_matches(metric.lower(), opts, cutoff=0.7)
    if len(actual) == 1:
        metric = actual[0]
    else:
        if len(actual) > 1:
            orange(
                f"Multiple metric options found ({', '.join(actual)}). Which did you mean?",
                ts=False,
            )
        elif len(actual) == 0:
            red("Metric value seems to be incorrect, try again", ts=False)
        print("")
        metric = str(input("seconds, minutes or hours? "))
        actual = difflib.get_close_matches(metric.lower(), opts, cutoff=0.7)
        if len(actual) == 1:
            metric = actual[0]
        else:
            red("Having trouble recognizing metric")
            return None
    if stop is not None:
        stop = todt(str(stop))
    else:
        stop = todt(now())
    diff = (stop - todt(str(start))).total_seconds()
    if full:
        hours, leftover = divmod(diff, 3600)
        minutes, seconds = divmod(leftover, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        seconds = round(diff)
        minutes = round(diff / 60)
        hours = round(diff / 3600)
        if metric == "seconds":
            return seconds
        elif metric == "minutes":
            return minutes
        elif metric == "hours":
            return hours


def filldates(start, end=None, as_str=False, weekends=True):
    """
    Returns a list of filled in dates between start and end. When
    weekends=False no weekend dates are included.
    """
    start = todt(str(start), as_date=True)
    if end is None:
        end = todt(now(), as_date=True)
    else:
        end = todt(str(end), as_date=True)
    drange = range((end - start).days + 1)
    if not weekends:
        dd = [
            start + timedelta(days=x)
            for x in drange
            if (start + timedelta(days=x)).weekday() not in [5, 6]
        ]
    else:
        dd = [start + timedelta(days=x) for x in drange]
    if as_str:
        try:
            return [tformat(i) for i in dd]
        except:
            red("Problem formatting as strings, returning dates as-is", False)
            return dd
    else:
        return dd


def nullstr(x):
    return bool(
        pd.isnull(x) or x in ["", None, "nan", "NaN", "None", "NONE", "N/A", "#N/A"]
    )


def blanknull(x):
    """Returns '' if passed string is null, otherwise string is returned"""
    if nullstr(x) or not x:
        return ""
    else:
        return x


def is_float(string):
    if str(string).replace(".", "").isnumeric():
        return True
    else:
        return False


def isodd(num):
    """Checks if num is odd"""
    if type(num) != int:
        num = int(num.replace(",", ""))
    return (num % 2) != 0


def iseven(num):
    """Checks if num is even"""
    if type(num) != int:
        num = int(num.replace(",", ""))
    return (num % 2) == 0


def regex(string, pattern):
    """Returns a regex extration of a string. A compiled object can be passed as the pattern."""
    try:
        if type(pattern) == str:
            return re.search(pattern, string).group(1)
        else:
            return pattern.search(string).group(1)
    except:
        pass


def remove(txt, rplc_strs):
    """Removes all rplc_strs from txt"""
    if type(rplc_strs) != list:
        rplc_strs = [r.strip() for r in rplc_strs.split(",")]
    ntxt = txt
    for i in rplc_strs:
        ntxt = ntxt.replace(i, "")
    return ntxt


def replace(txt_str, **rplc_map):
    """Loops through rplc_map (dict) and replaces all keys with values in passed txt_str"""
    out = txt_str
    for k, v in rplc_map.items():
        out = out.replace(k, v)
    return out


def match(rinput, opts):
    """Shortcut to difflib.get_close_matches(rinput,opts). rinput must be string, not list."""
    if type(opts) == str:
        split_str = bool(contains(",", opts) is not None and opts.strip() != ",")
        if split_str:
            opts = [i.strip() for i in opts.split(",")]
        else:
            opts = [opts]
    if type(rinput) == list:
        red("<b>rinput must be a string</b>", ts=False)
        return None
    z = 1
    for i in range(4):
        z += -0.1
        temp = difflib.get_close_matches(rinput, opts, cutoff=round(z, 1))
        if not empty(temp):
            break
    if empty(temp):
        return None
    if len(temp) > 1:
        temp = numdict(temp)
        popts = "\n".join([f"{k}: {v}" for k, v in temp.items()])
        pmsg = "Do any of these match (give index)? {0}".format(popts)
        raw_inp = str(input(pink(pmsg, ts=False, r=True)))
        if raw_inp == "":
            return None
        try:
            ix = int(raw_inp.strip())
            return temp[ix]
        except (ValueError, KeyError):
            return None
    else:
        return temp[0]


def contains(items, to_check, exact=True, _all=True):
    """
    Iterates through passed items and checks if they exist in to_check (list).
    When exact=False to_check list will be lowercased to find matches regardless
    of captilization/trailing spaces. When _all=False only the first matching item
    is returned (as a list object).
    """
    if type(to_check) in [pd.Series, pd.core.indexes.base.Index]:
        to_check = list(to_check)
    if not exact:
        to_check = [str(i).lower().strip() for i in to_check]
    if type(items) == str:
        if "," in items and items.strip() != ",":
            items = [i.strip() for i in items.split(",")]
        else:
            items = [items]
    dd = []
    if exact:
        for i in items:
            if i in to_check:
                dd.append(i)
    else:
        for i in items:
            if str(i).lower().strip() in to_check:
                dd.append(i)
    if len(dd) == 0:
        pink("None of the items passed were found in given list", ts=False)
    else:
        if _all or len(dd) == 1:
            out = dd
        else:
            out = [dd[0]]
        return out


def empty(obj):
    """Return True if obj is either null, blank or len(obj) == 0"""
    if obj is None:
        return True
    elif type(obj) in (pd.DataFrame, pd.Series):
        if len(list(obj.columns)) > 1:
            return bool(
                len(obj) == 0
                or (
                    obj[list(obj.columns)[0]].values[0] == ""
                    and obj[list(obj.columns)[1]].values[0] == ""
                )
            )
        else:
            return bool(len(obj) == 0 or obj[list(obj.columns)[0]].values[0] == "")
    elif type(obj) == list:
        return bool(obj == [])
    elif type(obj) == str:
        return bool(obj == "")
    elif type(obj) == dict:
        return bool(len(keys(obj)) == 0)


def numdict(input_list, rtype=dict):
    """
    Makes dict out of input_list where the keys are the order of the item in the list.
    When rtype=list a list of dicts is returned, otherwise a single dict is returned.
    If input_list is a series, it will automatically be converted to a list.
    """
    input_list = list(filter(None, input_list))
    out = dict(zip(range(1, len(input_list) + 1), input_list))
    if rtype in [dict, "dict"]:
        return out
    elif rtype in [list, "list"]:
        return [{k: v} for k, v in out.items()]


def reverse_dict(mydict, vals_as_list=False):
    reversed_dict = {}
    for key, val in mydict.items():
        reversed_dict.setdefault(val, [])
        reversed_dict[val].append(key)

    if not vals_as_list:
        # all values will be lists, otherwise only
        # duplicate values are lists
        for key, val in reversed_dict.items():
            if len(val) == 1:
                reversed_dict[key] = val[0]

    return reversed_dict


def keys(d, _all=True):
    """Shortcut to getting keys of a dict. If
    _all is False only the first key is returned."""
    key_list = list(d.keys())
    if _all:
        out = key_list
    else:
        out = key_list[:1]
    if type(out) != list:
        out = [out]
    return out


def keepkeys(dic, keys, exact=True):
    """
    Basically returns {k:v for k,v in dic.items() if k in keys} When exact=False keys
    becomes [i for i in dic if key in i] (loop).
    """
    if type(keys) == str:
        if "," in keys:
            keys = [i.strip() for i in keys.split(",")]
        else:
            keys = [keys]
    if not exact:
        keys = [i for i in dic for k in keys if k in i]
    return {k: v for k, v in dic.items() if k in keys}


def find_common(t1, t2, keep_order=True):
    """Returns common items between two lists. When keep_order=True, the order of t1 is kept."""
    if type(t1) == pd.core.indexes.base.Index:
        t1 = list(t1)
    elif type(t1) == pd.DataFrame:
        t1 = list(t1.columns)
    if type(t2) == pd.core.indexes.base.Index:
        t2 = list(t2)
    elif type(t2) == pd.DataFrame:
        t2 = list(t2.columns)
    items = set(t1) & set(t2)
    if keep_order:
        return sorted(items, key=lambda x: t1.index(x))
    else:
        return list(items)


def find_uncommon(t1, t2, keep_order=True):
    """Returns items found in t1 that do NOT exist in t2. When keep_order=True, the order of t1 is kept."""
    if type(t1) == pd.core.indexes.base.Index:
        t1 = list(t1)
    elif type(t1) == pd.DataFrame:
        t1 = list(t1.columns)
    if type(t2) == pd.core.indexes.base.Index:
        t2 = list(t2)
    elif type(t2) == pd.DataFrame:
        t2 = list(t2.columns)
    items = set(t1) - set(t2)
    if keep_order:
        return sorted(items, key=lambda x: t1.index(x))
    else:
        return list(items)


def comma_and(x, sep=", ", last_sep="and"):
    """Takes a list and adds last_sep (default: 'and') before last item in comma separated string."""
    if type(x) == str:
        x = [i.strip() for i in x.split(",")]
    if len(x) >= 3:
        return sep.join(x[:-1]) + f" {last_sep} " + x[-1]
    elif len(x) == 2:
        return f" {last_sep} ".join(x)
    else:
        return "".join(x)


def quotify(a_list, single=True):
    if single:
        return ", ".join([f"'{i}'" for i in a_list])
    else:
        return ", ".join([f'"{i}"' for i in a_list])


def chunkify(_list, num):
    return [_list[i : i + num] for i in range(0, len(_list), num)]


def ordinal(n):
    """Convert an num to ordinal (1st, 2nd, etc) representation"""
    n = int(n)
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    return f"{n}{suffix}"


def dget(dict_obj, key, val=None):
    """More secure version of dict.get(key, val)"""
    if key in dict_obj:
        if not dict_obj[key] or (
            isinstance(dict_obj[key], str) and nullstr(dict_obj[key])
        ):
            return val
    return dict_obj.get(key, val)


def filelist(dirpath, raise_err=False):
    """Returns [i for i in os.listdir(dirpath) if i[0].isalnum()] (must pass full path to folder). When raise_err=False no error is raised, otherwise FileNotFoundError is raised."""
    try:
        return [i for i in os.listdir(dirpath) if i[0].isalnum()]
    except FileNotFoundError:
        if raise_err:
            raise FileNotFoundError
        else:
            red("<b>Can't locate directory</b>")
            return None
