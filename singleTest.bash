#! /bin/bash

cd server
./startServer.bash
sleep 0.5 # To allow server time to spin up
cd ../client
python init.py
cd ../server
./killServer.bash
cd ..

echo ""
echo ""
echo "----SERVER OUTPUT----"
echo ""
tail -n 10 server/logs/log.txt
