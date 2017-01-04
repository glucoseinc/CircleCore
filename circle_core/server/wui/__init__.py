# -*- coding: utf-8 -*-
"""WebUI."""


def create_app(metadata=None):
    """App factory.

    :param Optional[Union[MetadataIniFile, MetadataRedis]] metadata: Metadata
    :rtype: Flask
    """
    from .app import CCWebApp
    app = CCWebApp(metadata)
    return app
