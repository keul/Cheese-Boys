# -*- coding: utf-8 -*-


def timestamp_sort(x):
    """Service method for sort by timestamp a list"""
    t1 = x["timestamp"]
    return t1


def timestampValueToString(value):
    """Given a millisecond amount, format it in a timestamp format"""
    hh = mm = ss = ml = ""
    mmInHour = 1000 * 60 * 60
    mmInMinute = 1000 * 60
    hh = "%02d" % (value / mmInHour)
    value = value % mmInHour
    mm = "%02d" % (value / mmInMinute)
    value = value % mmInMinute
    ss = "%02d" % (value / 1000)
    ml = "%03d" % (value % 1000)
    return "%s:%s:%s %s" % (hh, mm, ss, ml)


def timestampStringToValue(timestamp):
    """Given a timestamp, return the relative millisecond amount"""
    hh = int(timestamp[:2])
    mm = int(timestamp[3:5])
    ss = int(timestamp[6:8])
    ml = int(timestamp[9:12])
    return ml + ss * 1000 + mm * 1000 * 60 + hh * 1000 * 60 * 60
