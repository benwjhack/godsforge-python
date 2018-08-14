#! /bin/bash

if [ -f serverPID.txt ]; then
	echo "Killing previous server..."
	./killServer.sh > /dev/null
fi

echo "Starting server"...
stdbuf -o0 python init.py &>> logs/log.txt &
echo "$!" > serverPID.txt
