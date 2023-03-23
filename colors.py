from sty import fg, bg, ef, rs
from datetime import datetime
import re


def color_opts(x=None):
    """
    When nothing is passed entire list of sty's color options with their corresponding numbers are returned.
    Alternatively you can pass a specific number to see what color it corresponds to in sty.
    """
    if x is None:
        for i in range(256):
            print(fg(i) + "fg({0})".format(i) + rs.all)
        return None
    else:
        print(fg(int(x)) + "fg({0})".format(x) + rs.all)


def blue(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(33)
        + und_rgx2.sub(
            rs.all + fg(33),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(33), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def light_blue(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(39)
        + und_rgx2.sub(
            rs.all + fg(39),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(39), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def teal(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(30)
        + und_rgx2.sub(
            rs.all + fg(30),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(30), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def light_teal(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(32)
        + und_rgx2.sub(
            rs.all + fg(32),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(32), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def gray(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(246)
        + und_rgx2.sub(
            rs.all + fg(246),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(246), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def red(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(196)
        + und_rgx2.sub(
            rs.all + fg(196),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(196), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def dark_red(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(160)
        + und_rgx2.sub(
            rs.all + fg(160),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(160), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def green(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(40)
        + und_rgx2.sub(
            rs.all + fg(40),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(40), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def light_green(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(30)
        + und_rgx2.sub(
            rs.all + fg(30),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(30), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def purple(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(57)
        + und_rgx2.sub(
            rs.all + fg(57),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(57), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def violet(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(63)
        + und_rgx2.sub(
            rs.all + fg(63),
            und_rgx.sub(ef.u, bold_rgx2.sub(rs.all + fg(63), bold_rgx.sub(ef.bold, x))),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def magenta(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(198)
        + und_rgx2.sub(
            rs.all + fg(198),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(198), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def pink(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(200)
        + und_rgx2.sub(
            rs.all + fg(200),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(200), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def light_pink(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(205)
        + und_rgx2.sub(
            rs.all + fg(205),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(205), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def orange(x, ts=True, r=False):
    """
    x: input text
    ts: whether or not to include current timestamp (default True)
    r: when True returns actual compiled object, when False (default) nothing is returned only printed
    """
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(202)
        + und_rgx2.sub(
            rs.all + fg(202),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(202), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def pcolor(x, cid, ts=True, r=False):
    """Same as all color printing functions, just lets you pass specific color ID (from color_opts())."""
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        x = f'{x} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
    out = (
        fg(cid)
        + und_rgx2.sub(
            rs.all + fg(cid),
            und_rgx.sub(
                ef.u, bold_rgx2.sub(rs.all + fg(cid), bold_rgx.sub(ef.bold, x))
            ),
        )
        + rs.all
    )
    if r:
        return out
    else:
        print(out)


def pprint(x, ts=True, r=False):
    """
    Identical to other color functions, except you have more control over the string color(s).
    Example: '<33>Hello world!</33>' would print the string 'Hello world!' in the corresponding sty color value (blue)
    """
    color_rgx1 = re.compile("<([\d{,2}]*)>")
    color_rgx2 = re.compile("<\/([\d{,2]*)>")
    bold_rgx = re.compile("(<b>)", re.IGNORECASE)
    bold_rgx2 = re.compile("(<\/b>)", re.IGNORECASE)
    und_rgx = re.compile("(<u>)", re.IGNORECASE)
    und_rgx2 = re.compile("(<\/u>)", re.IGNORECASE)
    if ts:
        tstmp = (
            fg(246) + "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + rs.fg
        )
        x = f"{x} {tstmp}"
    out = color_rgx2.sub(
        rs.fg,
        color_rgx1.sub(
            lambda x: fg(int(x.group(1))),
            bold_rgx2.sub(
                rs.bold_dim,
                bold_rgx.sub(ef.bold, und_rgx2.sub(rs.all, und_rgx.sub(ef.u, x))),
            ),
        ),
    )
    if r:
        return out
    else:
        print(out)
