# -*- coding: utf-8 -*-
"""WebUI."""

# type annotation
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from circle_core.core import CircleCore
except ImportError:
    pass


def create_app(core, base_url=None, ws_port=None, is_https=False):
    """App factory.

    :param CircleCore core: CircleCore Core
    :param str base_url: ベースURL
    :param int ws_port: Websocket Port Number
    :return: WebUI App
    :rtype: CCWebApp
    """
    from .app import CCWebApp
    app = CCWebApp(core, base_url, ws_port, is_https=is_https)
    return app
