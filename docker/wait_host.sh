#!/bin/sh

set -e

host="$1"
port="$2"

until nc ${host} ${port} -z ; do
  >&2 echo "${host}:${port} is unavailable - sleeping"
  sleep 1
done

>&2 echo "${host}:${port} is up"
