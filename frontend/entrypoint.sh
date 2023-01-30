#!/bin/sh
JSON_STRING='window.configs = { \
  "ENV":"'"${ENV}"'", \
}'
sed -i "s@// CONFIGURATIONS_PLACEHOLDER@${JSON_STRING}@" /usr/share/nginx/html/index.html
exec "$@"