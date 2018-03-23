#! /bin/bash

echo "Killing server..."
kill -9 $(cat serverPID.txt)
rm serverPID.txt
