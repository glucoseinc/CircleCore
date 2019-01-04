#!/bin/sh
set -e

envsubst '$BASE_URL $DB_URL $HTTP_PORT' < circle_core.ini.template > circle_core.ini

./wait_host.sh mysql 3306
exec crcr "$@"
