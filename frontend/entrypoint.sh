#!/bin/sh
JSON_STRING='window.configs = { \
  "ENV":"'"${ENV}"'", \
  "SLACK_FEEDBACK_CHANNEL":"'"${SLACK_FEEDBACK_CHANNEL}"'", \
}'
sed -i "s@// CONFIGURATIONS_PLACEHOLDER@${JSON_STRING}@" /usr/share/nginx/html/index.html
exec "$@"