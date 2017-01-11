# -*- coding: utf-8 -*-
from click import get_current_context


def metadata():
    """metadata getter."""
    try:
        return get_current_context().obj.metadata
    except RuntimeError:
        # raise from 使いたいがPython2がサポートしていない
        raise NotImplementedError('Click context not found. You must set some mock metadata in the tests.')
