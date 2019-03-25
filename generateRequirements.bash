pipreqs --force server
sed -i '/^util==/ d' server/requirements.txt

pipreqs --force client
sed -i '/^util==/ d' client/requirements.txt

pipreqs --force bridge
sed -i '/^util==/ d' bridge/requirements.txt

