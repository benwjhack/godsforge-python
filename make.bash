#! /bin/bash
# Generate the build files, and build them in the build directory
# Requires .temp not to be a directory in use already

# Generate the requirement files
./generateRequirements.bash


# rm does not follow symlinks, just to reassure anyone who sees this.

mkdir .temp
rm build/*.zip

cp -Lr server .temp
cp -Lr client .temp

# For some reason, zip insists on including a full relative path structure to the file you're zipping in the zip file- so to exclude .temp as a directory from the .zip, we move into it.
cd .temp

zip -r ../build/server.zip server --exclude **/*.pyc
zip -r ../build/client.zip client --exclude **/*.pyc

cd ..

rm -r .temp

# Remove the requirements files
rm server/requirements.txt
rm client/requirements.txt
