# -*- coding: utf-8 -*-
"""WebUI."""


def create_app(core, base_url=None, ws_port=None, is_https=False):
    """App factory.

    :param Optional[Union[MetadataIniFile, MetadataRedis]] metadata: Metadata
    :rtype: Flask
    """
    from .app import CCWebApp
    app = CCWebApp(core, base_url, ws_port, is_https=is_https)
    return app
