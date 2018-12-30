#!/bin/sh
set -e

envsubst '$DB_URL $HTTP_PORT' < circle_core.ini.template > circle_core.ini
exec crcr "$@"