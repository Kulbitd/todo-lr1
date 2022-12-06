#!/bin/bash
for ((i =0;i < 20;i++));
do
  test=$($RANDOM | md5sum | head -c 20)
  curl -X 'POST' \
  'http://127.0.0.1:8000/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "title=$test"
done