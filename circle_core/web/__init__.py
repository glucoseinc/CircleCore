# -*- coding: utf-8 -*-
"""WebUI."""

from typing import TYPE_CHECKING

# type annotation
if TYPE_CHECKING:
    from typing import Optional

    from circle_core.core import CircleCore

    from .app import CCWebApp


def create_app(
    core: 'CircleCore', base_url: 'Optional[str]' = None, ws_port: 'Optional[int]' = None, is_https: 'bool' = False
) -> 'CCWebApp':
    """App factory.

    Args:
        core: CircleCore Core
        base_url: ベースURL
        ws_port: Websocket Port Number

    Return:
        WebApp
    :rtype: CCWebApp
    """
    from .app import CCWebApp
    app = CCWebApp(core, base_url, ws_port, is_https=is_https)
    return app
