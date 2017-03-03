# -*- coding: utf-8 -*-
"""WebUI."""


def create_app(core, base_url=None, ws_port=None):
    """App factory.

    :param Optional[Union[MetadataIniFile, MetadataRedis]] metadata: Metadata
    :rtype: Flask
    """
    from .app import CCWebApp
    app = CCWebApp(core, base_url, ws_port)
    return app
