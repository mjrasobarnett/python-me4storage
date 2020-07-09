import locale
from datetime import datetime

size_units = {
    # 2-based sizes.
    'bytes': ('%d', 1),
    'k':  ('%.1fKiB', 1024),
    'm':  ('%.1fMiB', 1024**2),
    'g':  ('%.2fGiB', 1024**3),
    't':  ('%.2fTiB', 1024**4),
    'p':  ('%.2fPiB', 1024**5),

    # 10-based sizes.
    'kb':  ('%.1fKB', 1000),
    'mb':  ('%.1fMB', 1000**2),
    'gb':  ('%.2fGB', 1000**3),
    'tb':  ('%.2fTB', 1000**4),
    'pb':  ('%.2fPB', 1000**5),
}

def disk_size_formatter(x, units=None):
    """ Convert integer number of bytes to size string with units suffix in base-2 """
    if units is None:
        if x < 1024**2:
            units = 'k'
        elif x < 1024**3:
            units = 'm'
        elif x < 1024**4:
            units = 'g'
        elif x < 1024**5:
            units = 't'
        else:
            units = 'p'
    t = size_units[units.lower()]
    return t[0] % (x / t[1])

def disk_size_metric_formatter(x, units=None):
    """ Convert integer number of bytes to size string with units suffix in base-10 """
    if units is None:
        if x < 1000**2:
            units = 'kb'
        elif x < 1000**3:
            units = 'mb'
        elif x < 1000**4:
            units = 'gb'
        elif x < 1000**5:
            units = 'tb'
        else:
            units = 'pb'
    t = size_units[units.lower()]
    return t[0] % (x / t[1])


def bytes_rate_formatter(x, units=None):
    """Transform rate in bytes/sec to size string with units suffix """
    """ Convert integer number of bytes/sec to size string with units suffix in base-2 """
    s = disk_size_formatter(x, units)
    return s + '/s'

def disk_size_parser(x):
    """Transform size with unit suffix to integer
    :param x:
    """
    if x.isdigit():
        return int(x)

    # Make sure suffix is valid.
    if len(x) >= 3 and not x[-3].isdigit() and x[-3] != '.':
        raise ValueError(_('Invalid unit suffix: %s') % x)

    if len(x) == 1:
        raise ValueError(_('Invalid disk size: %s') % x)

    # Check 2-based units.
    if x[-2].isdigit():
        if x[:-1] == '':
            raise ValueError(_('Invalid disk size: %s') % x)

        unit = x[-1:].upper()
        x = int(float(x[:-1]))
        if unit == 'K':
            return x * 1024
        elif unit == 'M':
            return x * (1024**2)
        elif unit == 'G':
            return x * (1024**3)
        elif unit == 'T':
            return x * (1024**4)
        else:
            raise ValueError(_('Invalid unit suffix: %s') % unit)
    else:
        # Check 10-based units.
        if x[:-2] == '':
            raise ValueError(_('Invalid disk size: %s') % x)

        unit = x[-2:].upper()
        x = int(float(x[:-2]))
        if unit == 'KB':
            return x * 1000
        elif unit == 'MB':
            return x * (1000**2)

        elif unit == 'GB':
            return x * (1000**3)
        elif unit == 'TB':
            return x * (1000**4)
        else:
            raise ValueError(_('Invalid unit suffix: %s') % unit)

def time_duration_formatter(x):
    """Format time duration in seconds
    """
    mm, ss = divmod(x, 60)
    hh, mm = divmod(mm, 60)
    dd, hh = divmod(hh, 24)

    res = ''
    if dd:
        res += '%dd ' % dd
    if dd or hh:
        res += '%dh ' % hh
    if dd or hh or mm:
        res += '%dm ' % mm
    res += '%ds' % ss

    return res

def epoch_formatter(x, date_format=None):
    """Convert epoch timestamp into date-time string.
       However to conserve space in output leave out name of the day in week
       and year information if the date belongs to current year.
    """
    if date_format is None:
        date_format = 'short'
    assert date_format in ['short', 'long'], 'Invalid format of date-time ' \
                                             'requested'
    if x == '':
        return None

    dt = datetime.fromtimestamp(x)
    dt_fmt = locale.nl_langinfo(locale.D_T_FMT)

    if date_format == 'short':
        dt_fmt = dt_fmt.replace('%a', '').strip()  # remove day of the week
        if dt.year == datetime.now().year:
            dt_fmt = dt_fmt.replace('%Y', '').strip()  # remove current year

    return dt.astimezone().strftime(dt_fmt)

def date_time_formatter(x, date_format=None):
    """Convert ISO date-time to format dictated by locales.
       However to conserve space in output leave out name of the day in week
       and year information if the date belongs to current year.
    """
    if date_format is None:
        date_format = 'short'
    assert date_format in ['short', 'long'], 'Invalid format of date-time ' \
                                             'requested'
    if x == '':
        return None

    time_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt = datetime.strptime(x, time_fmt)
    dt_fmt = locale.nl_langinfo(locale.D_T_FMT)

    if date_format == 'short':
        dt_fmt = dt_fmt.replace('%a', '').strip()  # remove day of the week
        if dt.year == datetime.now().year:
            dt_fmt = dt_fmt.replace('%Y', '').strip()  # remove current year

    return dt.astimezone().strftime(dt_fmt)
