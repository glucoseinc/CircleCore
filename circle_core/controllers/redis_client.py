#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Redisクライアント"""

# system module
import re

# community module
from redis import Redis
from six import PY2


class RedisClient(Redis):
    """Redisクライアント"""
    def parse_response(self, connection, command_name, **options):
        """Parses a response from the Redis server."""
        def decoded(word):
            """bytesはstrに変換する."""
            return word.decode('utf-8') if isinstance(word, bytes) else word

        response = super(RedisClient, self).parse_response(connection, command_name, **options)

        if PY2:
            return response

        if isinstance(response, bytes):
            return decoded(response)
        elif isinstance(response, list):
            return [decoded(resp) for resp in response]
        elif isinstance(response, dict):
            return {decoded(k): decoded(v) for k, v in response.items()}
        return response
