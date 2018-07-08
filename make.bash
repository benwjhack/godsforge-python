#! /bin/bash

# rm does not follow symlinks, just to reassure anyone who sees this.

mkdir .temp

cp -r server .temp
cp -r client .temp

rm .temp/server/util
rm .temp/client/util

cp -r util .temp/server
cp -r util .temp/client


zip -r build/server.zip .temp/server
zip -r build/client.zip .temp/client

rm -r .temp
