import calendar
import difflib
import os
from datetime import datetime, date, timedelta

import pandas as pd
import pyperclip
from dateutil.parser import parse
from dotenv import load_dotenv, dotenv_values

from .colors import *


def clipboard(string):
    """Copies text to clipboard so it can be pasted anywhere.

    Args:
        string (str): String to copy

    Returns:
        Nothing"""
    pyperclip.copy(string)
    green("Copied to clipboard", ts=False)


def tformat(date_obj, style=None):
    """Formats a date or datetime object as a string with the given style.
    When style=None default datetime format is %Y-%m-%d %H:%M:%S and default date format is %Y-%m-%d.

    Args:
        date_obj (date, datetime): Date or datetime object to format
        style (str): Desired datetime format (i.e. %Y-%m-%d)

    Returns:
        A string representation of the passed date_obj in the given style."""
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
    """Takes a datetime string and converts it to an actual datetime object.
    When as_date=True a date object is returned instead of a datetime object.

    Args:
        dt_str (str): Date or datetime string
        as_date (bool): Whether or not to return the value as a date not datetime object

    Returns:
        A date or datetime objects of the passed string.
    """
    if dt_str is None:
        dt_str = now()
    elif "_" in dt_str:
        dt_str = dt_str.replace("_", "-")

    if as_date:
        return parse(dt_str).date()
    else:
        return parse(dt_str)


def now(style="%Y-%m-%d %H:%M:%S", dt=True):
    """Returns the current date and time.

    Args:
        style (str): Datetime format to use (default is %Y-%m-%d %H:%M:%S)
        dt (bool): If True a datetime object is returned instead of a string

    Returns:
        Either a string or datetime object of the current date and time"""
    if dt:
        return datetime.now()
    else:
        return datetime.now().strftime(style)


def monthdays(month, year=todt(now()).year):
    """Returns the total number of days in a given month.

    Args:
        month (int): Integer representation of a given month
        year (int): Year to reference

    Returns:
        A integer representing the number of days in a given month.
    """
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
    """Returns the 1st of the given month (current month is default).

    Args:
        month (int): Month to reference
        year (int): Year to reference
        offset (int): Number of months to offset by
        style (str): Desired datetime format

    Returns:
        A date string of the 1st of the given month."""
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
    """Returns the last date of the given month (current month is default).

    Args:
        month (int): Month to reference
        year (int): Year to reference
        offset (int): Number of months to offset by
        style (str): Desired datetime format

    Returns:
        A date string of the last date of the given month."""
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


def dt_int(num, start=None, metric="days", style="%Y-%m-%d", dt=True):
    """Adds/subtracts days, minutes or hours from a given date or datetime.

    Args:
        num (int): Number to offset by
        start (date, datetime, str): Starting date to offset
        metric (str): The metric to use for calculation (days, minutes or hours)
        style (str): Desired datetime format (ignored when dt=True)
        dt (bool): If True a datetime object is returned instead of a string

    Returns:
        A formatted date string of the calculated date."""
    input_type = "date"
    out = None
    if start is None:
        start = datetime.now()
        input_type = "datetime"
    elif isinstance(start, str):
        if " " in start:
            start = todt(start)
            input_type = "datetime"
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

    if dt:
        if input_type == "datetime":
            return todt(out)
        else:
            return todt(out, as_date=True)
    else:
        return out


def daydiff(start, stop=None):
    """Calculates the number of days between two dates.

    Args:
        start (date, datetime, str): Date to subtract from
        stop (None, date, datetime, str): Date to subtract (default is the current day)

    Returns:
        A integer representing the number of days in between the given dates"""
    start = todt(str(start))
    if stop is None:
        stop = todt(now())
    else:
        stop = todt(str(stop))
    return (stop - start).days


def elapsed(start, stop=None, metric="minutes", full=False):
    """Pass a datetime.datetime object and return elapsed time from then to now. Metric opts:
    seconds, minutes, hours. When full=True elapsed time is returned as H:M:S.

    Args:
        start (datetime, str): The datetime value to subtract from
        stop (None, datetime, str): The datetime value to subtract with (current day by default)
        metric (str): The metric to calculate the elapsed time by (seconds, minutes, hours)
        full (bool): If True metric is overridden and elapsed time is returned in H:M:S format

    Returns:
        Either an integer representing the elapsed seconds, minutes or hours between two dates or a
        string representation of the elapsed time in H:M:S format."""
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
    """Calculates the dates in between two dates.

    Args:
        start (date, str): Start of the desired date range
        end (None, date, str): End of the desired date range (current day by default)
        as_str (bool): If True dates are returned as strings instead of date objects
        weekends (bool): If False weekend dates are excluded from the final output

    Returns:
        A list of dates in between two given dates."""
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


def nullstr(string):
    """More robust way of checking if a string is null even in cases where things like '#N/A'
    are present.

    Args:
        string (str): String to check

    Returns:
        A boolean dictating whether or not the passed string is truly null."""
    return bool(
        pd.isnull(string) or string in ["", None, "nan", "NaN", "None", "NONE", "N/A", "#N/A"]
    )


def blanknull(string):
    """Converts any null values to a blank string.

    Args:
        string (str): String to check

    Returns:
        '' if the passed string is null otherwise the string is returned."""
    if nullstr(string) or not string:
        return ""
    else:
        return string


def is_float(string):
    """Checks if a string is meant to be a float.

    Args:
        string (str): String to check

    Returns:
        True if the string is a float, False if not."""
    if str(string).replace(".", "").isnumeric():
        return True
    else:
        return False


def isodd(num):
    """Checks if a given number is odd.

    Args:
        num (int): Number to check

    Returns:
        True if the given number is odd, False if it's even."""
    if not isinstance(num, int):
        num = int(num.replace(",", ""))
    return (num % 2) != 0


def iseven(num):
    """Checks if a given number is even.

    Args:
        num (int): Number to check

    Returns:
        True if the given number is even, False if it's odd."""
    if not isinstance(num, int):
        num = int(num.replace(",", ""))
    return (num % 2) == 0


def regex(string, pattern):
    """Performs a regex extration of a given string.

    Args:
        string (str, re.compile): String or compiled re object to reference
        pattern (str): Regex pattern to search the string with

    Returns:
        A string of the output of the passed regex."""
    if type(pattern) == str:
        return re.search(pattern, string).group(1)
    else:
        return pattern.search(string).group(1)


def str_remove(txt, rplc_strs):
    """Removes passed strings from a string.

    Args:
        txt (str): String to clean
        rplc_strs (list): Strings to remove from the passed txt string

    Returns:
        The passed string with the strings passed in rplc_strs removed from it."""
    if not isinstance(rplc_strs, list):
        rplc_strs = [r.strip() for r in rplc_strs.split(",")]
    ntxt = txt
    for i in rplc_strs:
        ntxt = ntxt.replace(i, "")
    return ntxt


def str_replace(txt, **rplc_map):
    """Replaces things in a string.

    Args:
        txt (str): String to clean
        rplc_map (dict): Dict where the keys are what to replace and the values are what to replace it with

    Returns:
        The passed string with the desired replacements."""
    out = txt
    for k, v in rplc_map.items():
        out = out.replace(k, v)
    return out


def is_empty(obj):
    """Checks if a given obj is either null, blank or len(obj) == 0.

    Args:
        obj (DataFrame, Series, list, dict, str): Object to check

    Returns:
        True if the object is empty, False if not."""
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
    elif isinstance(obj, list):
        return bool(obj == [])
    elif isinstance(obj, str):
        return bool(obj == "")
    elif isinstance(obj, dict):
        return bool(len(keys(obj)) == 0)


def numdict(input_list):
    """Creates a dictionary from a list where the keys are an item's index and the values are the list's items.

    Args:
        input_list (list): List of items

    Returns:
        A dictionary where the keys are the index of each item in a given list and the values are the lists's items."""
    input_list = list(filter(None, input_list))
    return dict(zip(range(1, len(input_list) + 1), input_list))


def reverse_dict(mydict, vals_as_list=False):
    """Reverses a dictionary by swapping its keys with its values. In cases where this causes duplicate keys,
    rather than overwriting the values all values of duplicate keys are merged into lists.

    Args:
        mydict (dict): Dictionary to reverse
        vals_as_list (bool): If True all values are returned as lists, not just values of duplicate keys

    Returns:
        A reversed dictionary."""
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


def keepkeys(mydict, keys):
    """Creates a dictionary from the passed dictionary containing only the given keys.

    Args:
        mydict (dict): Dictionary to filter
        keys (list): List of keys you want to keep from the passed dictionary

    Returns:
        The passed dictionary containing only the desired keys."""
    if isinstance(keys, str):
        if "," in keys:
            keys = [i.strip() for i in keys.split(",")]
        else:
            keys = [keys]

    return {k: v for k, v in mydict.items() if k in keys}


def find_common(list1, list2):
    """Finds common values between two lists.
    
    Args:
        list1 (Series, list): List to check against
        list2 (Series, list): List to check
    
    Returns:
        A list of items that appear in both list1 and list2."""
    if isinstance(list1, pd.Series):
        list1 = list(list1)
    if isinstance(list1, str):
        list1 = [t.strip() for t in list1.split(",")]
    
    if isinstance(list2, pd.Series):
        list2 = list(list2)
    if isinstance(list2, str):
        list2 = [t.strip() for t in list2.split(",")]

    items = set(list1) & set(list2)
    # keep original order of list1
    return sorted(items, key=lambda x: list1.index(x))


def find_uncommon(list1, list2):
    """Compares two lists and finds values that appear in the first list but not the second.

    Args:
        list1 (Series, list): List to check against
        list2 (Series, list): List to check

    Returns:
        A list of items that appear in list1 that don't appear in list2."""
    if isinstance(list1, pd.Series):
        list1 = list(list1)
    if isinstance(list1, str):
        list1 = [t.strip() for t in list1.split(",")]

    if isinstance(list2, pd.Series):
        list2 = list(list2)
    if isinstance(list2, str):
        list2 = [t.strip() for t in list2.split(",")]

    items = set(list1) - set(list2)
    # keep original order of list1
    return sorted(items, key=lambda x: list1.index(x))


def comma_and(input_list, sep=", ", last_sep="and"):
    """Joins a list of strings together joined by the given separators.
    e.g. comma_and(['dog', 'cat', 'rat'], sep=', ', last_sep='&') would return 'dog, cat & rat'
    
    Args:
        input_list (list): A list of strings to join and parse
        sep (str): The separator to be used to join the strings in the list (', ' by default)
        last_sep (str): The separator for the last string in the list ('and' by default)

    Returns:
        A string of the passed list joined by the given separators."""
    if type(input_list) == str:
        input_list = [i.strip() for i in input_list.split(",")]

    if len(input_list) >= 3:
        return sep.join(input_list[:-1]) + f" {last_sep} " + input_list[-1]
    elif len(input_list) == 2:
        return f" {last_sep} ".join(input_list)
    else:
        return "".join(input_list)


def quotify(input_list, single=True):
    """Joins a list of strings together commas and places each string inside quotes.

    Args:
        input_list (list): A list of strings to join and parse
        single (bool): If True single quotes are used otherwise double quotes are used

    Returns:
        A string of the passed list joined together by commas with each string inside quotes."""
    if single:
        return ", ".join([f"'{i}'" for i in input_list])
    else:
        return ", ".join([f'"{i}"' for i in input_list])


def chunkify(input_list, num):
    """Divides a list into a given number of chunks.

        Args:
            input_list (list): A list to divide
            num (int): The number of items each chunk should contain

        Returns:
            A list of lists where each list contains the passed number of items from the given list."""
    return [input_list[i: i + num] for i in range(0, len(input_list), num)]


def ordinal(n):
    """Converts a number into its ordinal representation (e.g. 1st, 2nd, etc).

    Args:
        n (int, str): The string or integer to convert

    Returns:
        An ordinal string representation of the given number."""
    n = int(str(n))
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]

    if 11 <= (n % 100) <= 13:
        suffix = "th"

    return f"{n}{suffix}"


def dget(dict_obj, key, val=None):
    """More secure version of dict.get(key, val). This accounts for edge cases where a key exists and the
    value is a blank string and returns None (or whatever you pass as val) instead of the blank string.

    Args:
        dict_obj (dict): Dictionary to reference
        key (str): Target key to grab from the dictionary
        val (str, None): Default value to return if the target key isn't in the dictionary

    Returns:
        The value of the key of the passed dictionary (or the value of val if the key doesn't exist)."""
    if key in dict_obj:
        if not dict_obj[key] or (
            isinstance(dict_obj[key], str) and nullstr(dict_obj[key])
        ):
            return val

    return dict_obj.get(key, val)


def filelist(dirpath, raise_err=False):
    """Lists the filenames in the passed directory.

    Args:
        dirpath (str): Directory path to reference
        raise_err (bool): If False FileNotFoundErrors will fail silently

    Returns:
        A list containing all the filenames in the given directory."""
    try:
        return [i for i in os.listdir(dirpath) if i[0].isalnum()]
    except FileNotFoundError:
        if raise_err:
            raise FileNotFoundError
        else:
            red("<b>Can't locate directory</b>")
            return None
