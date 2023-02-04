#! /bin/sh

./shutdown.sh

./scripts/build-api-container.sh
./scripts/build-frontend-container.sh

./startup.sh