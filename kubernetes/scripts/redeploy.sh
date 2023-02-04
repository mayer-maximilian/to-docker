#! /bin/sh

./shutdown.sh

./build-api-container.sh
./build-frontend-container.sh

./startup.sh