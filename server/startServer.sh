#! /bin/bash

if [ -f serverPID.txt ]; then
	echo "Killing previous server..."
	./killServer.sh
fi

echo "Starting server"...
python init.py > /dev/null 2>&1 &
echo "$!" > serverPID.txt
