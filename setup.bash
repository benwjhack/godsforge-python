sudo apt install python-pip
sudo pip install pipreqs
./generateRequirements.bash
cd server
pip install -r requirements.txt
cd ../client
pip install -r requirements.txt
cd ../bridge
pip install -r requirements.txt
cd ..
rm **/requirements.txt
