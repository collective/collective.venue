# -*- coding: utf-8 -*-


def join_nonempty(items, sep=u'/'):
    return sep.join([it for it in items if it])
