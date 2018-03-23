#! /bin/bash

cd server
./startServer.sh
sleep 0.5
cd ../client
python init.py
cd ../server
./killServer.sh
cd ..
