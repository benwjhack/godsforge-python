#! /bin/bash

echo "Killing server..."
kill -SIGTERM $(cat serverPID.txt)
rm serverPID.txt
