#! /bin/bash

if [ -f serverPID.txt ]; then
	echo "Killing previous server..."
	./killServer.sh
fi

echo "Starting server"...
stdbuf -o0 python init.py &> logs/log.txt &
echo "$!" > serverPID.txt
