#!/bin/bash

# just for example purposes

curl -X "GET" "http://localhost:5008/api/" -H "Authorization: Bearer <token>"
curl -X "GET" "http://localhost:5008/api/<id>" -H "Authorization: Bearer <token>"
curl -X "POST" "http://localhost:5008/api/" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title": "SOMETHING", "description": "ELSE"}'
curl -X "PUT" "http://localhost:5008/api/<id>" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title": "ELSE", "description": "SOMETHING"}'
curl -X "DELETE" "http://localhost:5008/api/<id>" -H "Authorization: Bearer <token>"