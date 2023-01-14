#!/bin/bash
docker compose up
docker run -p 5008:5008 --network backend --name software-containerization-api software-containerization