#! /bin/bash

cd server
./startServer.sh
sleep 0.5 # To allow server time to spin up
cd ../client
python init.py
cd ../server
./killServer.sh
cd ..

echo ""
echo ""
echo "----SERVER OUTPUT----"
echo ""
tail -n 10 server/logs/log.txt
